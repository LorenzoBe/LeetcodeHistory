import configparser
import json
import redis

from storage import StorageInterface

class RedisStorage(StorageInterface):

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        redisHostname = self.config['Azure']['RedisHostname']
        redisKey = self.config['Azure']['RedisKey']

        self.redisClient = redis.StrictRedis(host=redisHostname, port=6380, password=redisKey, ssl=True)

        self.contestKeyPrefix = 'contestId:'
        self.userKeyPrefix = 'userId:'

    def addContest(self, contestTitle: str, details: str) -> bool:
        self.redisClient.set(self.contestKeyPrefix + contestTitle, details)
        return True

    def getContest(self, contestTitle: str) -> list:
        return self.redisClient.get(self.contestKeyPrefix + contestTitle)

    def deleteContest(self, contestTitle: str) -> list:
        return self.redisClient.delete(self.contestKeyPrefix + contestTitle)

    def addContestResult(self, username: str, result: str) -> bool:
        self.redisClient.rpush(self.userKeyPrefix + username, result)
        return True

    def getAllContestsResults(self, username: str) -> list:
        return self.redisClient.lrange(self.userKeyPrefix + username, 0, -1)

    def deleteUser(self, username: str) -> bool:
        return self.redisClient.delete(self.userKeyPrefix + username)
