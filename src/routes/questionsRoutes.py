from flask import request, json, jsonify
import os

from . import router, baseLocation
from pathlib import Path
from .quizzesRoutes import *
from ..utils.file import readFile, writeFile, checkFile
from ..utils.authorization import verifyLogin

questionsFileLocation = baseLocation / "data" / "questions-file.json" 

@router.route('/quizzes/question', methods=["POST"])
@verifyLogin
def createQuestion():
    body = request.json

    questionData = {
        "question":[]
    }

    if os.path.exists(questionsFileLocation):
        questionData = readFile(questionsFileLocation)

    questionData["question"].append(body)
    writeFile(questionsFileLocation, questionData)

    return jsonify(questionData)

@router.route('/quizzes/<quizId>/questions/<questionNumber>')
@verifyLogin
def getThatQuestion(quizId, questionNumber):
    quizData = getQuiz(int(quizId)).json
    quizzesData = readFile(quizzesFileLocation)
    
    for question in quizData["question-list"]:
        if question["question-number"] == int(questionNumber):
            return jsonify(question)


@router.route('/quizzes/<quizId>/questions/<questionNumber>', methods=["PUT","DELETE"])
def updateDelete(quizId,questionNumber):
    if request.method == "DELETE":
        return deleteQuestion(quizId, questionNumber)
    elif request.method == "PUT":
        return updateQuestion(quizId, questionNumber)

def deleteQuestion(quizId,questionNumber):
    questionData = readFile(questionsFileLocation)

    questionToBeDeleted = getThatQuestion(int(quizId), int(questionNumber)).json 

    for i in range(len(questionData["question"])):
        if questionData["question"][i] == questionToBeDeleted:
            del questionData["question"][i]
            # message = "Berhasil menghapus question Number " + questionNumber + " dari quiz id " + quizId
            break
        # else:
        #     message = "Gagal menghapus. Tidak ada quiz-id " + quizId + " atau question Number " + questionNumber

    writeFile(questionsFileLocation, questionData)
    return jsonify(questionData)