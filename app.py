from flask import Flask, request, json, jsonify, render_template
from random import randint
import requests 
import os

from src.routes import router

app = Flask(__name__)   
app.register_blueprint(router)       


@app.route('/game', methods = ['POST'])
def createGame():
    body = request.json

    # dapetin info quiz
    quizzesFile = open('./quizzes-file.json')
    quizzesData = json.load(quizzesFile)

    for quiz in quizzesData["quizzes"]:
        quiz = json.loads(quiz)

        if quiz["quiz-id"] == int(body["quiz-id"]):
            gameInfo = quiz

    gameInfo["game-pin"] = randint(100000, 999999)
    gameInfo["user-list"] = []
    gameInfo["leaderboard"] = []

    # create skeleton for list of game buat nulis 
    # kalau belum pernah main game sama sekali
    gamesData = {
        "game-list": []
    }

    # simpen data game nya
    if os.path.exists('./games-file.json'):
        gamesFile = open('./games-file.json', 'r')
        gamesData = json.load(gamesFile)
    else:
        gamesFile = open('./games-file.json', 'x')

    with open('./games-file.json', 'w') as gamesFile:
        gamesData["game-list"].append(gameInfo)
        gamesFile.write(str(json.dumps(gamesData)))

    return jsonify(gameInfo)

#join kedalam game sebagai user
@app.route('/game/join', methods=['POST'])
def joinGame():
    body = request.json

    # open game data information
    gamesFile = open('./games-file.json')
    gamesData = json.load(gamesFile)

    position = 0
    for i in range(len(gamesData["game-list"])):
        game = gamesData["game-list"][i]

        if game["game-pin"] == int(body["game-pin"]):
            if body["username"] not in game["user-list"]:
                game["user-list"].append(body["username"])
                game["leaderboard"].append({
                    "username": body["username"],
                    "score": 0
                    })

                gameInfo = game
                position = i
                break
            # TODO: error kalau usernya udah dipake

    with open('./games-file.json', 'w') as gamesFile:
        gamesData["game-list"][position] = gameInfo
        gamesFile.write(str(json.dumps(gamesData)))
        
    return jsonify(request.json)
    
#cek leaderboard
@app.route('/game/leaderboard', methods = ["POST"])
def getLeaderboard():
    body = request.json

    gamesFile = open('./games-file.json')
    gamesData = json.load(gamesFile)

    for game in gamesData["game-list"]:
        if game["game-pin"] == body["game-pin"]:
            leaderboard = game["leaderboard"]            

    for _ in range(len(leaderboard)):
        index = 0
        while index < len(leaderboard)-1:
            if leaderboard[index]["score"] < leaderboard[index+1]["score"]:
                leaderboard[index], leaderboard[index+1] = leaderboard[index+1], leaderboard[index]

            index += 1                        
    return jsonify(leaderboard)

#jawab soal 
@app.route('/game/answer', methods=['POST'])
def submitAnswer():
    isTrue = False
    body = request.json

    # buka file question
    questionsFile = open('./question-file.json')
    questionsData = json.load(questionsFile)

    for question in questionsData["question"]:
        question = json.loads(question)

        if question["quiz-id"] == int(body["quiz-id"]) and question["question-number"] == int(body["question-number"]):
            if question["answer"] == body["answer"]:
                isTrue = True

    # TODO: update skor/leaderboard
    gamesFile = open('./games-file.json')
    gamesData = json.load(gamesFile)

    gamePosition = 0
    for i in range(len(gamesData["game-list"])):
        game = gamesData["game-list"][i]

        if game["game-pin"] == body["game-pin"]:
            if isTrue:
                userPosition = 0
                for j in range(len(game["leaderboard"])):
                    userData = game["leaderboard"][j]

                    if userData["username"] == body["username"]:
                        userData["score"] += 100

                        userInfo = userData
                        userPosition = j
                        break

                game["leaderboard"][userPosition]
                gameInfo = game
                gamePosition = i
                break

    with open('./games-file.json', 'w') as gamesFile:
        gamesData["game-list"][gamePosition] = gameInfo
        gamesFile.write(str(json.dumps(gamesData)))

    return jsonify(request.json)