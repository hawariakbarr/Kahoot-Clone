from flask import Flask, request, json, jsonify, render_template
from random import randint
import requests 
import os

app = Flask(__name__)   
app.config['DEBUG'] = True

alfabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
number = ['0','1','2','3','4','5','6','7','8','9']
extend = alfabet + number


def enkrip(string,move):
    encodeString = ""
    for x in range(len(string)):
        tempString = extend.index(string[x]) + int(move)
        encodeString = encodeString + extend[tempString % len(extend)]
    return encodeString

def dekrip(string,move):

    decodeString = ""
    for x in range(len(string)):
        tempString = extend.index(string[x]) - int(move)
        decodeString = decodeString + extend[tempString % len(extend)]

    return decodeString        
       

######register data creator quiz#######
@app.route('/register', methods=["POST"])
def userRegister():
    body = request.json
    
    if body["method"] == "encrypt":
        body["password"] = enkrip(body["password"], int(body["move"]))        
    elif body["method"] == "decrypt":
        body["password"] = dekrip(body["password"], int(body["move"]))        

    registerData = {
        "user-data": []
    }

    if os.path.exists('./user-register.json'):
        registerFile = open('./user-register.json', 'r')
        registerData = json.load(registerFile)
    else:
        registerFile = open('./user-register.json', 'x')

    with open('./user-register.json', 'w') as registerFile:
        registerData["user-data"].append(body)

        registerFile.write(str(json.dumps(registerData)))

    return jsonify(registerData)



#######login creator quiz##########
@app.route('/login', methods=["POST"])
def loginUser():
    body = request.json
    statusLogin = False
        
    registerFile = open('./user-register.json')
    registerData = json.load(registerFile)

    for data in registerData["user-data"]:
        # data = json.loads(data)
        if body["method"] == "decrypt":
            
            if data["user-id"] == int(body["user-id"]) and data["username"] == body["username"] and dekrip(data["password"], int(body["move"])) == body["password"]:
                statusLogin = True
            else:
                statusLogin = False
    return str(statusLogin)                        
        
#bikin quiz baru  nomer1
@app.route('/quiz', methods=["POST"])
def createQuiz():
    body = json.dumps(request.json)
    quizData = {
        "totalQuizAvailable": 0,
        "quizzes": []
    }
    if os.path.exists('./quizzes-file.json'):
        quizzesFile = open("quizzes-file.json", "r")
        quizData = json.load(quizzesFile)
    else:
        quizzesFile = open('./quizzes-file.json','x')
        print("no file quizzes")

    quizData["totalQuizAvailable"] += 1
    quizData["quizzes"].append(body)

    quizzesFile = open('./quizzes-file.json','w')        
    quizzesFile.write(str(json.dumps(quizData))) #

    return str(quizData)

############################ kirim soal ke quiz / bikin soal ke quiz nomer 2####################################
@app.route('/question', methods=["POST"])
def createQuestion():
    body = json.dumps(request.json)

    questionData = {
        "question":[]
    }

    if os.path.exists('./question-file.json'):
        questionFile = open("question-file.json", "r")
        questionData = json.load(questionFile)
    else:
        questionFile = open('./question-file.json','x')
        print("no file question")

    questionFile = open('./question-file.json','w')        
    questionData["question"].append(body)
    questionFile.write(str(json.dumps(questionData))) #

    return str(questionData)

data = []

@app.route('/', methods=["POST"])
def tryAja():
    body = request.json
    data.append(body["name"])

    return jsonify(data)

@app.route('/<name>', methods=["DELETE", "PUT"])
def modifyData(name):
    body = request.json

    if request.method == "DELETE":        
        data.remove(name)
    elif request.method == "PUT":
        index = data.index(name)
        data[index] = body["new-name"]

    return jsonify(data)

def encrypt(string):
    return string + "encrypted"

def decrypt(string):
    return string + "decrypted"

#############################ambil data keseluruahn quiz / minta data kesluruhan dari quiz nomer3##########
@app.route('/quizzes/<quizId>', methods=["GET", "DELETE", "PUT"])
def getQuiz(quizId):
    body = request.json

    quizzesFile = open('./quizzes-file.json')
    quizzesData = json.load(quizzesFile) 

    for quiz in quizzesData["quizzes"]:
        quiz = json.loads(quiz)

        if quiz["quiz-id"] == int(quizId):
            quizData = quiz
            break

    questionFile = open('./question-file.json')            
    questionData = json.load(questionFile)

    for question in questionData["question"]:
        question = json.loads(question)
        if question["quiz-id"] == int(quizId):
            quizData["question-list"].append(question)

    return jsonify(quizData)

#######################ambil pertanyaan tertentu dari sebuah quiz nomer4############################
@app.route('/quizzes/<quizId>/questions/<questionNumber>')
def getThatQuestion(quizId, questionNumber):
    quizData = getQuiz(int(quizId)).json
    
    for question in quizData["question-list"]:
        if question["question-number"] == int(questionNumber):
            return jsonify(question)

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

########################################join kedalam game sebagai user nomer5##############################
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
    
####################################cek leaderboard nomer6##############################################
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

#############################################nomerjawab soal nomer7############################################    
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
    
# if __name__ == "__main__":
#     app.run(debug=True)