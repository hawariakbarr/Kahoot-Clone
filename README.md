# Kahoot Clone 
This project was created to clone the kahoot game with the backend section.

---
## Prerequisites
There is somethings and tools that must be prepared and installed before starting the project.
```
1. Python
2. Visual Studio Code
3. Insomnia
4. Flask / Django
```

## Installations
### Flask 
#### Create environment
  Create a project folder and a `venv` folder within:
  ```
  mkdir myproject
  cd myproject
  python3 -m venv venv
  ```
  On Windows:
  ```
    py -3 -m venv venv
  ```
If you needed to install virtualenv because you are on an older version of Python, use the following command instead:
```
virtualenv venv
```

#### Activate the Environment
Before you work on your project, activate the corresponding environment:
On Windows:
```
venv\Scripts\activate
```
#### Install FLASK
Within the activated environment, use the following command to install Flask:
```
pip install Flask
```
---
## Feature from Kahoot Clone
- Able to register and login data for creator quiz
  ```python
    @app.route('/register', methods=["POST"])
    def userRegister():
    @app.route('/login', methods=["POST"])
    def loginUser():
  ```
  Password encode and decode for secure
  ```python
    def enkrip(string,move):
    def dekrip(string,move):
  ```

- Able to create, delete and update Quiz.
  ```python
  @app.route('/quiz', methods=["POST"])
  def createQuiz():
  @app.route('/quizzes/<quizId>', methods = ["PUT", "GET", "DELETE"])
  def deleteQuiz(quizId):
  @app.route('/quizzes/<quizId>', methods = ["PUT", "GET", "DELETE"])
  def updateQuiz(quizId):
  ```
  Insomnia JSON for new quiz
  ```json
    {
	"quiz-id": 123,
	"quiz-name": "makers batch IV",
	"quiz-category": "fun fact",
	"question-list": []
    }
  ```

- Able to create. delete and update Question in Quiz

- Join the game with username and game pin
  ```python
  @app.route('/game/join', methods=['POST'])
  def joinGame():
  ```
  Insomnia JSON for join the game
  ```json
    {
	"game-pin": 568929,
	"username": "clover"
    }
  ```

- Submit answer for question 
  ```python
  @app.route('/game/answer', methods=['POST'])
  def submitAnswer():
  ```
  Insomnia JSON for submit answer
  ```json
    {
	"answer": "C",
	"quiz-id": 123,
	"question-number": 1,
	"username": "aduh",
	"game-pin": 568929
    }
  ```
- View leader board for the Winner
  ```python
  @app.route('/game/leaderboard', methods = ["POST"])
  def getLeaderboard():
  ```
  Insomnia JSON for get leaderboard
  ```json
  {
	"game-pin": 568929
  }   
  ```


## License  
__Nur Imam Hawari Akbar__ 
![makers institute](data:image/png;base64,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)



