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
    body = request.json
    userNameOrEmailUsed = False

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
                userNameOrEmailUsed = True
                response["error"] = True
                break
                
    if not userNameOrEmailUsed:        
        registerData["total-user-register"] += 1
        body["password"] = forEncrypt(body["password"])
        registerData["user-data"].append(body)

        writeFile(userFileLocation, registerData)
        
        del body["password"]
        response["data"] = body
    else:      
        response["message"] = "email or username is used"
    return jsonify(response)


@router.route('/users/login', methods=["POST"])
def loginUser():
    body = request.json
    response = {
        "error": False
    }
    try: 
        registerData = readFile(userFileLocation)

    except:
        response["error"] = True
        response["message"] = ""

        return jsonify(response)
    else:
        for data in registerData["user-data"]:
            if data["username"] == body["username"] and forDecrypt(data["password"]) == body["password"]:
                userData = body
                body["token"] = generateToken(body["username"])
                body.pop("password")
                response["error"] = False
                response["message"] = "Login Success"
                response["data"] = body
                break
            else:
                response["error"] = True
                response["message"] = "login failed, username and email is wrong. Try again"
            
    return jsonify(response)                      