#!/usr/bin/python3
# -*- Coding: utf-8 -*-

from flask import Flask,request,abort,jsonify ,render_template
from flask_api import status
from SmartHome import app
import SmartHome.api

@app.route('/')
def home():
    #特に何もしない
    return "Hello!", status.HTTP_200_OK

@app.route('/iot',methods=["POST"])
def endpoint():
    try:
        dic = request.json
        target = dic['target'] if 'target' in dic else ''
        switch = dic['switch'] if 'switch' in dic else ''
        color = dic['color'] if 'color' in dic else ''
        return api.callAPI(target, switch, color)
    except:
        return "ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    pass