from flask import request, json, jsonify, g
import os

from . import router, baseLocation
from pathlib import Path
from ..utils.file import readFile
from ..utils.authorization import verifyLogin

quizzesFileLocation = baseLocation / "data" / "quizzes-file.json" 
questionFileLocation = baseLocation / "data" / "questions-file.json" 

@router.route('/quizzes', methods=["POST"])
@verifyLogin
def createQuiz():
    body = request.json
    print("username:",g.username)

    quizData = {
        "total-quiz-available": 0,
        "quizzes": []
    }
    if os.path.exists(quizzesFileLocation) and os.path.getsize(quizzesFileLocation) > 0:
        quizzesFile = open(quizzesFileLocation, "r")
        quizData = json.load(quizzesFile)

    quizData["total-quiz-available"] += 1
    quizData["quizzes"].append(body)

    quizzesFile = open(quizzesFileLocation,'w')        
    quizzesFile.write(str(json.dumps(quizData))) #

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
    quizzesFile = open(quizzesFileLocation)
    quizzesData = json.load(quizzesFile) 

    for quiz in quizzesData["quizzes"]:
        # quiz = json.loads(quiz)

        if quiz["quiz-id"] == int(quizId):
            quizData = quiz            
            break

    questionFile = open(questionFileLocation)            
    questionData = json.load(questionFile)

    for question in questionData["question"]:
        # question = json.loads(question)
        if question["quiz-id"] == int(quizId):
            quizData["question-list"].append(question)

    return jsonify(quizData)

def deleteQuiz(quizId):
    quizzesFile = open(quizzesFileLocation)
    quizData = json.load(quizzesFile)

    for i in range(len(quizData["quizzes"])):
        quiz = quizData["quizzes"][i]
        # quiz = json.loads(quiz)


        if quiz["quiz-id"] == (int(quizId)): 
            del quizData["quizzes"][i] 
            quizData["total-quiz-available"] -= 1 
            break

    quizzesFile = open(quizzesFileLocation, 'w')
    quizzesFile.write(str(json.dumps(quizData)))

    return jsonify(quizData)

def updateQuiz(quizId):
    body = request.json

    quizzesFile = open(quizzesFileLocation)
    quizData = json.load(quizzesFile)

    for i in range(len(quizData["quizzes"])):
        quiz = quizData["quizzes"][i]
        # quiz = json.loads(quiz)

        if quiz["quiz-id"] == (int(quizId)):  
            quiz["quiz-id"] = body["quiz-id"]
            quiz["quiz-name"] = body["quiz-name"]
            quiz["quiz-category"] = body["quiz-category"]
            quizData["quizzes"][i] = quiz
        break        

    quizzesFile = open(quizzesFileLocation, 'w')
    quizzesFile.write(str(json.dumps(quizData)))

    return jsonify(quizData)
