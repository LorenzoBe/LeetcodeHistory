from configparser import ConfigParser
from flask import Flask
from flask import request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json

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

    if (contestType != None and contestId != None):
        res = False

        if contestType == 'standard':
            res = dataProxy.pushContest(Contest.STANDARD, contestId)
        elif contestType == 'biweekly':
            res = dataProxy.pushContest(Contest.BIWEEKLY, contestId)

        return "Function executed: " + str(res)

    return "Errors in GET arguments. Required: 'type' and 'id'"

@app.route('/getUser')
@auth.login_required
def getUser():
    username = request.args.get('username', type = str)

    if (username != None):
        userRanks = dataProxy.getUser(username)

        result = {}
        result['ranks'] = []
        for rank in  userRanks:
            result['ranks'].append(json.loads(rank.decode()))
        return json.dumps(result)

    return "Errors in GET arguments. Required: 'username'"

@app.route('/')
@auth.login_required
def root():
    return app.send_static_file('index.html')