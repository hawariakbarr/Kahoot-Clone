from flask import request, json, jsonify, g
import os

from . import router, baseLocation
from pathlib import Path
from ..utils.file import readFile, checkFile, writeFile
from ..utils.authorization import verifyLogin

quizzesFileLocation = baseLocation / "data" / "quizzes-file.json" 
questionsFileLocation = baseLocation / "data" / "questions-file.json" 

@router.route('/quizzes', methods=["POST"])
@verifyLogin
def createQuiz():
    body = request.json
    print("username:",g.username)

    quizData = {
        "total-quiz-available": 0,
        "quizzes": []
    }

    checkFile(quizzesFileLocation)        

    quizData["total-quiz-available"] += 1
    quizData["quizzes"].append(body)

    writeFile(quizzesFileLocation, quizData)
    return jsonify(quizData)

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
    quizzesData = readFile(quizzesFileLocation)
    thereIsQuiz = False

    for quiz in quizzesData["quizzes"]:
        if quiz["quiz-id"] == int(quizId):
            quizData = quiz            
            thereIsQuiz = True
            break

    if not thereIsQuiz:
        return jsonify("quiz-id " + "not found")

    questionData = readFile(questionsFileLocation)

    for question in questionData["question"]:
        if question["quiz-id"] == int(quizId):
            quizData["question-list"].append(question)

    return jsonify(quizData)

def deleteQuiz(quizId):
    questionData = readFile(questionsFileLocation)
    
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
    
    quizData = readFile(quizzesFileLocation)

    for i in range(len(quizData["quizzes"])):
        quiz = quizData["quizzes"][i]

        if quiz["quiz-id"] == (int(quizId)): 
            del quizData["quizzes"][i] 
            quizData["total-quiz-available"] -= 1 
            break

    writeFile(quizzesFileLocation, quizData)
    
    return jsonify(quizData)

def updateQuiz(quizId):
    body = request.json

    quizData = readFile(quizzesFileLocation)

    for i in range(len(quizData["quizzes"])):
        quiz = quizData["quizzes"][i]

        if quiz["quiz-id"] == (int(quizId)):  
            quiz["quiz-id"] = body["quiz-id"]
            quiz["quiz-name"] = body["quiz-name"]
            quiz["quiz-category"] = body["quiz-category"]
            quizData["quizzes"][i] = quiz
        break                

    writeFile(quizzesFileLocation, quizData)

    return jsonify(quizData)