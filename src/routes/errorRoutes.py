from flask import json, jsonify, abort
from . import router

@router.errorhandler(403)
def error403(e):
    messages = {
        "status-code": 403,
        "message" : "you are not login yet"
    }

    return jsonify(messages)

@router.errorhandler(404)        
def error404(e):
    messages = {
        "status-code": 404,
        "message" : "no resource"
    }

@router.errorhandler(500)    
def error500(e):
    messages = {
        "status-code": 403,
        "message" : "internal server"
    }