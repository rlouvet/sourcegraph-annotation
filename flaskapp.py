import logging
from logging.handlers import RotatingFileHandler
import json
import re

from flask import Flask
from flask import request

from collections import OrderedDict


#Preparing logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('flaskapp.log', 'a', 1000000, 1)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#steam_handler = logging.StreamHandler()
#steam_handler.setLevel(logging.DEBUG)
#logger.addHandler(steam_handler)

#Setting flask app up
app = Flask(__name__)

#In memory data
data = {"alex" : "http://alex.com"}



@app.route('/', methods = ['GET'])
@app.route('/names', methods = ['GET'])
def main():
    logger.info("Received GET on /")
    return "Hello world!"


@app.route('/names', methods = ['DELETE'])
def drop():
    logger.info("Received DELETE on /names")
    global data
    data = {}
    return "Name data has been dropped!"

@app.route('/names/<name>', methods = ['GET'])
def getName(name):
    logger.info("Received GET on /names/%s", name)

    if not data.has_key(name):
        return "Name is not in database"
    else:
        gen = (('name', name), ('url', data[name]))
        newDict = OrderedDict(gen)
        outBuffer = json.dumps(newDict) + '\n'
        return outBuffer

@app.route('/names/<name>', methods = ['PUT'])
def update(name):
    logger.info("Received PUT on /names/%s", name)
    global data
    req = request.data
    dataDict = json.loads(req)
    logger.info("json content: %s", dataDict)

    data[name] = dataDict['url']

    rtnMessage = "%s has correctly been updated" % name
    return rtnMessage

@app.route('/annotate', methods = ['POST'])
def annotate():
    global data

    def replFunc(stringObj):
        global data
        if data.has_key(stringObj):
            return '<a href=' + data[stringObj] + '>' + stringObj + '</a>'
        else:
            return stringObj

    inputString = request.data
    outputString = re.sub(r'(?![^<]*(</a>|>))\b([A-Za-z0-9]+)\b', lambda m: replFunc(m.group()), inputString)

    return outputString



if __name__ == '__main__':
    app.run(host = "127.0.0.1",
            port = int(3001))