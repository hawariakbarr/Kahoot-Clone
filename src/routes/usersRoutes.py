from flask import request, json, jsonify
import os
from . import router, baseLocation
from .. utils.crypt import forEncrypt, forDecrypt
from pathlib import Path
from ..utils.file import readFile, writeFile, checkFile
from .. utils.authorization import generateToken

userFileLocation = baseLocation / "data" / "user-register.json"

@router.route('/users', methods=["POST"])
def userRegister():
    # print(os.getenv("API_KEY"))
    body = request.json
    userNameAndEmailUsed = False

    registerData = {
        "total-user-register": 0,
        "user-data": []
        
    }

    response = {
        "error": False
    }
    try: 
        registerData = readFile(userFileLocation)
    except : 
        print("no users file")
    else:        
        body["username"]
        body["email"]
        
        for data in registerData["user-data"]:
            if data["username"] == body["username"] or data["email"] == body["email"]:
                userNameAndEmailUsed = True

                response["error"] = True
                break
                
    if not userNameAndEmailUsed:        
        registerData["total-user-register"] += 1
        body["password"] = forEncrypt(body["password"])
        registerData["user-data"].append(body)

        writeFile(userFileLocation, registerData)
        
        del body["password"]

        response["data"] = body
    else:
        del body["password"]        
        response["message"] = "email or username is used"
    return jsonify(registerData)


@router.route('/users/login', methods=["POST"])
def loginUser():
    body = request.json

    registerData = readFile(userFileLocation)

    for data in registerData["user-data"]:
        if data["user-id"] == int(body["user-id"]) and data["username"] == body["username"] and forDecrypt(data["password"]) == body["password"]:
            statusLogin = "Login mantap cuyyy"
            body["token"] = generateToken(body["username"])
        else:
            statusLogin = "Aduh ada yg salah, cek lagi punten"

    return jsonify(body)                      
