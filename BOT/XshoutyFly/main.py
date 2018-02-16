from flask import Flask, jsonify,request
import os.path
import sys
import json
import requests
from ciscosparkapi import CiscoSparkAPI
from utils.Compute import Compute
from XshoutyFly import XshoutyFly
from ngrok import NgrokAPI

botToken = "ZGU0Y2RkYmYtMTM5Mi00ZGQ3LWFmMWQtOGQ4NzE0ZjcwZWQxZTdmZWIxY2EtYTk3"
name="XshoutyFly"

app = Flask(__name__)
api = CiscoSparkAPI(botToken)

#Logger
import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler(name+'/utils/'+name.lower()+'.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


#Shutdown function (do not touch):
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running')
    func()
@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

#Create a MyBot instance when receiving a post request and call run() method
@app.route('/',methods=['POST'])
def Main():
    bot = XshoutyFly(request.json,api)
    ans = bot.run()
    return (ans)

#Webhook method enable you to receive data from third part services
@app.route('/webhook',methods=['POST','GET','PUT','DELETE'])
def Webhook():
    bot = XshoutyFly()
    bot.Webhook(request.json,api)
    return ("")

#Launching the server
if __name__ == '__main__':
    with open('.config.txt') as json_file:
        data = json.load(json_file)
        bots = data['bots']
        for bot in bots:
            if (bot["name"] == name):
                port = bot['Port']

    try:
        app.run(
            host="localhost",
            port=int(port),
            debug=True
        )
    except:
        pass