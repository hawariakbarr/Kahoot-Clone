from flask import request, json, jsonify, g
import os

from . import router, baseLocation, quizzesFileLocation, questionsFileLocation
from pathlib import Path
from ..utils.file import readFile, checkFile, writeFile
from ..utils.authorization import verifyLogin

@router.route('/quizzes', methods=["POST"])
@verifyLogin
def createQuiz():
    body = request.json
    idUsed = False
    quizData = {
        "total-quiz-available": 0,
        "quizzes": []
    }
    
    response = {}
    
    try:
        quizData = readFile(quizzesFileLocation)
    except:
        print("No Quiz for Load")

    for quiz in quizData["quizzes"]:
        if quiz["quiz-id"] == body["quiz-id"]:
            idUsed = True
            break
        
    if idUsed == True:           
        response["error"] = True
        response["message"] = "Quiz Id is Used"
        return jsonify(response)

    else:
        quizData["total-quiz-available"] += 1
        quizData["quizzes"].append(body)
        response["data"] = quizData
        response["error"] = False
        writeFile(quizzesFileLocation, quizData)        

    return jsonify(response)

@router.route('/quizzes/all-quizzes')
@verifyLogin
def allQuiz():
    
    response = {}
    try:
        quizzesData = readFile(quizzesFileLocation)
    except:
        response["error"] = True
        response["message"] = "Quiz File cannot load"

    else:
        response["error"] = False
        response["data"] = quizzesData

    return jsonify(response)



@router.route('/quizzes/<quizId>', methods = ["PUT", "GET", "DELETE"])
@verifyLogin
def function(quizId):
    if request.method == "DELETE":
        return deleteQuiz(quizId)
    elif request.method == "GET":
        return getQuiz(quizId)
    elif request.method == "PUT":
        return updateQuiz(quizId)        

def getQuiz(quizId):
    quizFound = False
    response = {
        "error": True
    }
    try:
        quizzesData = readFile(quizzesFileLocation)
    except:
        response["message"] = "error while load quiz data"
        return jsonify(response)
    else:       
        for quiz in quizzesData["quizzes"]:
            if quiz["quiz-id"] == int(quizId):
                quizData = quiz            
                quizFound = True

                response["error"] = False
                response["data"] = quizData
                break

    if quizFound:
        try:
            questionData = readFile(questionsFileLocation)
        except:
            print("no file question")
        else:        
            for question in questionData["question"]:
                if question["quiz-id"] == int(quizId):
                    quizData["question-list"].append(question)
    else:
        response["message"] = "quiz is not found"

    return jsonify(response)

def deleteQuiz(quizId):
    body = request.json
    
    response = {}
    try:
        questionData = readFile(questionsFileLocation)
    except:
        response["message"] = "Error while load question data"
        return jsonify(response)

    LquestionList = 0
    questionList = []
    for question in questionData["question"]:
        index = questionData["question"].index(question)
        if question["quiz-id"] == int(quizId):
            LquestionList += 1
            questionList.append(index)

    deletingIndex = 0
    indexDeleted = 0
    for i in range(LquestionList):
        deletingIndex = questionList[i] - indexDeleted
        del questionData["question"][deletingIndex]
        indexDeleted += 1        
    
    writeFile(questionsFileLocation, questionData)
    
    try:
        quizData = readFile(quizzesFileLocation)
    except:
        response["message"] = "Error while load quiz data"
        return jsonify(response)
    idMatch = False
    for i in range(len(quizData["quizzes"])):
        quiz = quizData["quizzes"][i]

        if quiz["quiz-id"] == (int(quizId)): 
            idMatch = True
            break
        else:
            idMatch == False
    if idMatch == True:
        del quizData["quizzes"][i] 
        quizData["total-quiz-available"] -= 1 
        response["message"] = "Delete Success"            
    else:
        response["message"] = "Quiz Id is not Match, try again"
        return jsonify(response)
    writeFile(quizzesFileLocation, quizData)
    return jsonify(response)

def updateQuiz(quizId):
    body = request.json
    idMatch = False
    response = {}
    try:
        quizData = readFile(quizzesFileLocation)
    except:
        response["message"] = "Error while load quiz data"
        return jsonify(response)
    for i in range(len(quizData["quizzes"])):
        quiz = quizData["quizzes"][i]

        if quiz["quiz-id"] == (int(quizId)):  
            idMatch = True
            break

    if idMatch == True:
        quiz["quiz-id"] = body["quiz-id"]
        quiz["quiz-name"] = body["quiz-name"]
        quiz["quiz-category"] = body["quiz-category"]
        quizData["quizzes"][i] = quiz
        response["data"] = quizData
            
    else:
        response["message"] = "Quiz Id is not match, Try again"
        
    writeFile(quizzesFileLocation, quizData)

    return jsonify(response)