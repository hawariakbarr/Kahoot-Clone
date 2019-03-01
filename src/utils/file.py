from flask import json
import os

def writeFile(fileLocation, data):
    theFile = open(fileLocation, 'w')
    theFile.write(str(json.dumps(data)))

def readFile(fileLocation):
    theFile = open(fileLocation)
    data = json.load(theFile)
    return data

def checkFile(fileLocation):
    if os.path.exists(fileLocation):
        theFile = open(fileLocation, 'r')
        return json.load(theFile)    