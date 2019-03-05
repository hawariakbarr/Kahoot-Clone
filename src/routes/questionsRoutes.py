from flask import request, json, jsonify, abort
import os

from . import router, baseLocation, questionsFileLocation
from pathlib import Path
from .quizzesRoutes import *
from ..utils.file import readFile, writeFile, checkFile
from ..utils.authorization import verifyLogin

@router.route('/quizzes/question', methods=["POST"])
@verifyLogin
def createQuestion():
    body = request.json
    numberIsUsed = False    
    questionData = {
        "question":[]
    }
    response = {}

    try:
        questionData = readFile(questionsFileLocation)
    except:
        print("No File question For Load")

    for question in questionData["question"]:
        if question["question-number"] == body["question-number"]:
            numberIsUsed = True
            break

    if numberIsUsed == True:
        response["error"] = True
        response["message"] = "Question Number is Used"

    else:
        questionData["question"].append(body)
        response["data"] = questionData
        response["error"] = False
        writeFile(questionsFileLocation, questionData)

    return jsonify(response)

@router.route('/quizzes/all-questions')
@verifyLogin
def getAllQuestion():
    response = {}

    try:
        questionData = readFile(questionsFileLocation)
    except:
        response["error"] = True
        response["message"] = "Question file cannot load"

    else:
        response["error"] = False
        response["data"] = questionData

    return jsonify(response)        

@router.route('/quizzes/<quizId>/questions/<questionNumber>')
@verifyLogin
def getThatQuestion(quizId, questionNumber):
    questionFound = False

    response = {
        "error": False
    }
    try:
        questionData = readFile(questionsFileLocation)
    except:
        response["message"] = "error while load question data"
        return jsonify(response)
    else:
        for question in questionData["question"]:
            if question["question-number"] == int(questionNumber):
                dataQuestion = question
                questionFound = True

                response["error"] = False
                response["data"] = dataQuestion
                break
    
    if not questionFound:    
        response["error"] = True
        response["message"] = "question not found"
    return jsonify(response)        

@router.route('/quizzes/<quizId>/questions/<questionNumber>', methods=["PUT","DELETE"])
def updateDelete(quizId,questionNumber):
    if request.method == "DELETE":
        return deleteQuestion(quizId, questionNumber)
    elif request.method == "PUT":
        return updateQuestion(quizId, questionNumber)

def deleteQuestion(quizId,questionNumber):
    allMatch = False
    response = {}

    try:
        questionData = readFile(questionsFileLocation)
    except:
        response["message"] = "error while load question data"
        return jsonify(response)
    
    for i in range(len(questionData["question"])):
        question = questionData["question"][i]
        if question["quiz-id"] == (int(quizId)) and question["question-number"] == (int(questionNumber)):
            allMatch = True
            break
        else:
            allMatch == False

    if allMatch == True:
        del questionData["question"][i]
        response["message"] = "Delete question success"
    else:
        response["message"] = "Quiz id or Number Question is not match"
        return jsonify(response)
        
    writeFile(questionsFileLocation, questionData)
    return jsonify(response)

def updateQuestion(quizId, questionNumber):
    body = request.json
    questionData = readFile(questionsFileLocation)
    allMatch = False

    response = {}
    
    for i in range(len(questionData["question"])):
        question = questionData["question"][i]
        if question["quiz-id"] == (int(quizId)) and question["question-number"] == (int(questionNumber)):
            allMatch = True
            break
        else:
            allMatch = False             
    
    if allMatch == True:
        questionData["question"][i] = {**questionData["question"][i], **body}       
        response["data"] = questionData["question"][i]
    else:
        response["message"] = "Update Failed, quiz id or question number not match"
        return jsonify(response)

    writeFile(questionsFileLocation, questionData)
    return jsonify(response)    