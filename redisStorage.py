from configparser import ConfigParser
import json
import redis

from storage import StorageInterface

class RedisStorage(StorageInterface):

    def __init__(self, config: ConfigParser):
        self.config = config
        redisHostname = self.config['Azure']['RedisHostname']
        redisKey = self.config['Azure']['RedisKey']

        self.redisClient = redis.StrictRedis(host=redisHostname, port=6380, password=redisKey, ssl=True)

        self.contestKey = 'contests'
        self.userKeyPrefix = 'userId:'

    def getClient(self):
        return self.redisClient

    def addContest(self, details: str) -> bool:
        self.redisClient.rpush(self.contestKey, details)
        return True

    def getContests(self) -> list:
        return self.redisClient.lrange(self.contestKey, 0, -1)

    def deleteContests(self) -> bool:
        return self.redisClient.delete(self.contestKey)

    def addContestResult(self, username: str, result: str) -> bool:
        self.redisClient.rpush(self.userKeyPrefix + username, result)
        return True

    def getAllContestsResults(self, username: str) -> list:
        return self.redisClient.lrange(self.userKeyPrefix + username, 0, -1)

    def deleteUser(self, username: str) -> bool:
        return self.redisClient.delete(self.userKeyPrefix + username)
