import datetime
from app import db

class User(db.Model):
    __tablename__ = 'user_data'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    full_name = db.Column(db.String())
    password = db.Column(db.String())
    email = db.Column(db.String())
    created_on = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, username, full_name, password, email):
        self.username = username
        self.full_name = full_name
        self.password = password
        self.email = email
    
    def __repr__(self):
        return '<user_id()>'.format(self.user_id)

    def serialize(self):
        return{
            'user-id': self.user_id,
            'username': self.username,
            'full_name': self.full_name,
            'password': self.password,
            
            'email': self.email,
            'created_on': self.created_on
        }

class Quiz(db.Model):
    __tablename__ = 'quiz'        

    quiz_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.user_id'),foreign_key=True)
    quiz_category = db.Column(db.String())
    quiz_name = db.Column(db.String())    
    quiz_desc = db.Column(db.String())
    question = db.relationship('Question', backref='quiz', lazy = True)
    created_on = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self,  user_id, quiz_category, quiz_name, quiz_desc):
        self.user_id = user_id
        self.quiz_category = quiz_category
        self.quiz_name = quiz_name
        self.quiz_desc = quiz_desc


    def __repr__(self):
        return '<quiz_id()>'.format(self.quiz_id)

    def serialize(self):
        user_data = User.query.filter(User.user_id==self.user_id).first()
        return{            
            'creator_id': self.user_id,
            'creator_quiz': user_data.full_name,
            'quiz_id': self.quiz_id,
            'quiz_category': self.quiz_category,
            'quiz_name': self.quiz_name,
            'quiz_description': self.quiz_desc,
            'question_list': [{'question-number':item.question_id,'question':item.the_question} for item in self.question]
        }

class Question(db.Model):
    __tablename__ = 'question'        

    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), foreign_key=True)
    the_question = db.Column(db.String())
    correct_answer = db.Column(db.String())
    answer_option = db.relationship('Option', backref='question', lazy = True)
    created_on = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, quiz_id, the_question, correct_answer):
        self.quiz_id = quiz_id
        self.the_question = the_question
        self.correct_answer = correct_answer

    def __repr__(self):
        return '<question_id()>'.format(self.question_id)

    def serialize(self):
        return{
            'quiz-id': self.quiz_id,
            'question-number': self.question_id,
            'question': self.the_question,
            'option': [{'A':item.a, 'B':item.b, 'C':item.c, 'D':item.d } for item in self.answer_option],
            'correct-answer': self.correct_answer
        }

class Option(db.Model):
    __tablename__ = "answer_option"

    option_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer,db.ForeignKey('question.question_id'),foreign_key=True)
    quiz_id = db.Column(db.Integer,db.ForeignKey('quiz.quiz_id'), foreign_key=True)
    a = db.Column(db.String())
    b = db.Column(db.String())
    c = db.Column(db.String())
    d = db.Column(db.String())
    created_on = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, question_id, quiz_id, a, b, c, d):
        
        self.question_id = question_id
        self.quiz_id = quiz_id
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __repr__(self):
        return '<option_id()>'.format(self.option_id)

    def serialize(self):
        return{
            'quiz-id': self.quiz_id,
            'question-number': self.question_id,
            'option-id': self.option_id,
            'a': self.a,
            'b': self.b,
            'c': self.c,
            'd': self.d
        }

class Game(db.Model):
    __tablename__ = 'game'        

    game_pin = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, foreign_key=True)
    created_on = db.Column(db.DateTime, default = datetime.datetime.now)
    leaderboard =  db.relationship('Leaderboard', backref='game', lazy=True)
    # question = db.relationship('Question', backref='game', lazy = True)

    def __init__(self, game_pin, quiz_id):
        self.game_pin = game_pin
        self.quiz_id = quiz_id

    def serialize(self):
        quiz = Quiz.query.filter(Quiz.quiz_id==self.quiz_id).first()
        return{
            'game-pin': self.game_pin,
            'quiz-id': self.quiz_id,
            'quiz-name': quiz.quiz_name,
            'player-list': [{'player-id':item.player_id,'player-name':item.player_name} for item in self.leaderboard]
        }

class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'

    player_id = db.Column(db.Integer())
    game_pin = db.Column(db.Integer, db.ForeignKey('game.game_pin'), foreign_key=True)
    player_name = db.Column(db.String())
    score = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default = datetime.datetime.now)
    
    def __init__(self, player_id, game_pin, player_name, score):
        self.player_id = player_id
        self.game_pin = game_pin
        self.player_name = player_name
        self.score = score
        
    def serialize(self):
        return{
            'game-pin': self.game_pin,
            'player-id': self.player_id,
            'player-name': self.player_name,
            'score': self.score
        }
