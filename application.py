from configparser import ConfigParser
from flask import Flask
from flask import render_template
from flask import request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json
import operator
import time

from dataProxy import DataProxy
from leetcode import Contest

app = Flask(__name__)
auth = HTTPBasicAuth()
config = ConfigParser()
config.read('config.ini')
dataProxy = DataProxy(config)

users = {
    config['WebApp']['AdminUsername']: generate_password_hash(config['WebApp']['AdminPassword']),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/addContest')
@auth.login_required
def addContest():
    contestType = request.args.get('type', default = 'standard', type = str)
    contestId = request.args.get('id', type = int)

    if (contestType == None or contestId == None):
        return "Errors in GET arguments. Required: 'type' and 'id'"

    res = False

    if contestType == 'standard':
        res = dataProxy.pushContest(Contest.STANDARD, contestId)
    elif contestType == 'biweekly':
        res = dataProxy.pushContest(Contest.BIWEEKLY, contestId)

    return "Function executed: " + str(res)

@app.route('/export')
@auth.login_required
def exportStorage():
    exportFileName = request.args.get('filename', default = 'backup-{}.p'.format(int(time.time())), type = str)

    res = dataProxy.exportStorage(exportFileName)

    return "Function executed: " + str(res)

@app.route('/import')
@auth.login_required
def importStorage():
    importFileName = request.args.get('filename', default = '', type = str)
    res = False

    res = dataProxy.importStorage(importFileName)

    return "Function executed: " + str(res)

@app.route('/getUser')
@auth.login_required
def getUser():
    username = request.args.get('username', type = str)

    if (username == None):
        "Errors in GET arguments. Required: 'username'"

    userRanks = dataProxy.getUser(username)
    result = {}
    result['ranks'] = []
    for rank in  userRanks:
        result['ranks'].append(json.loads(rank.decode()))

    return json.dumps(result)

@app.route('/')
def root():
    username = request.args.get('username', type = str)
    contestBlacklist = request.args.get('blacklist', default = '', type = str)
    contestBlacklistSet = set(contestBlacklist.split(';'))

    if (username == None):
        username = 'bertelli'

    userRanks = dataProxy.getUser(username)
    result = {}
    result['ranks'] = []
    for rank in  userRanks:
        rankData = json.loads(rank.decode())
        if rankData['id'] not in contestBlacklistSet:
            result['ranks'].append(rankData)
    # sort by contest timestamp
    result['ranks'].sort(key = operator.itemgetter('ts'))
    jsonData = json.dumps(result)

    return render_template('index.html', ranksPlaceholder = jsonData, usernamePlaceholder = username)
