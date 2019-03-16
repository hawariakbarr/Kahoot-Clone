@app.route('/create-game', methods=["POST"])
def createGame():
    body = request.json

    try:
        game = Game(
            game_pin=body["game_pin"],
            quiz_id=body["quiz_id"],
            question_id=body["question_id"],
            nickname=body["nickname"]
            )

        db.session.add(game)
        db.session.commit()
        return "Game has created. Game pin={}".format(game.game_pin)
    except Exception as e:
        return(str(e))
        
@app.route('/get-all-question', methods=["GET"])
def getAllQuestion():
    try:
        question = Question.query.order_by(Question.question_id).all()
        return jsonify([emstr.serialize()for emstr in question])

    except Exception as e:
        return(str(e))

@app.route('/get-question/<id_>', methods=["GET"])
def getQuestionById(id_):
    try:
        question = Question.query.filter_by(question_id = id_).first()
        return jsonify(question.serialize())
    except Exception as e:
        return(str(e))

@app.route('/delete-question-by-id/<id_>', methods=["DELETE"])
def deleteQuestionById(id_):
    try:
        question = Question.query.filter_by(question_id = id_).delete()
        db.session.commit()
        
        return "Question has deleted"
    except Exception as e:
        return(str(e))

@app.route('/update-question/<id_>', methods=["PUT"])
def updateQuestionById(id_):    
    body = request.json
    try:
        question = Question.query.filter_by(question_id = id_).first()
        for key, value in body.items():
            if key == "the_question":
                question.the_question = value
            elif key == "correct_answer":
                question.correct_answer = value

    except Exception as e:
        return (str(e))
    
    db.session.commit()
    return "Question data has updated. question id={}".format(question.question_id)

    