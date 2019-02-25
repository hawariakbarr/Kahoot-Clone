from flask import request, json, jsonify
import os

from . import router, baseLocation
from pathlib import Path
from .quizzesRoutes import *

questionsFileLocation = baseLocation / "data" / "questions-file.json" 

@router.route('/quizzes/question', methods=["POST"])
def createQuestion():
    body = request.json

    questionData = {
        "question":[]
    }

    if os.path.exists(questionsFileLocation) and os.path.getsize(questionsFileLocation) > 0:
        questionFile = open(questionsFileLocation, "r")
        questionData = json.load(questionFile)

    questionFile = open(questionsFileLocation,'w')        
    questionData["question"].append(body)
    questionFile.write(str(json.dumps(questionData))) #

    return jsonify(questionData)

@router.route('/quizzes/<quizId>/questions/<questionNumber>', methods = ["PUT", "GET", "DELETE"])
def getThatQuestion(quizId, questionNumber):
    quizData = getQuiz(int(quizId)).json

    # quizzesFile = open(quizzesFileLocation)
    # quizzesData = json.load(quizzesFile)
    
    for question in quizData["question-list"]:
        if question["question-number"] == int(questionNumber):
            return jsonify(question)
