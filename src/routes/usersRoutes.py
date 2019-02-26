from flask import request, json, jsonify
import os
from . import router, baseLocation
from .. utils.crypt import forEncrypt, forDecrypt
from pathlib import Path

userFileLocation = baseLocation / "data" / "user-register.json"

@router.route('/users', methods=["POST"])
def userRegister():
    print(os.getenv("API_KEY"))
    body = request.json

    body["password"] = forEncrypt(body["password"])

    registerData = {
        "user-data": []
    }

    if os.path.exists(userFileLocation):
        registerFile = open(userFileLocation, 'r')
        registerData = json.load(registerFile)
    else:
        registerFile = open(userFileLocation, 'x')

    with open(userFileLocation, 'w') as registerFile:
        registerData["user-data"].append(body)
        registerFile.write(str(json.dumps(registerData)))

    return jsonify(registerData)


@router.route('/users/login', methods=["POST"])
def loginUser():
    body = request.json
    
        
    registerFile = open(userFileLocation)
    registerData = json.load(registerFile)

    for data in registerData["user-data"]:
        if data["user-id"] == int(body["user-id"]) and data["username"] == body["username"] and forDecrypt(data["password"]) == body["password"]:
            statusLogin = "Login mantap cuyyy"
        else:
            statusLogin = "Aduh ada yg salah, cek lagi punten"

    return statusLogin                       
