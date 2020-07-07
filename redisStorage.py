from configparser import ConfigParser
import json
import pickle
import redis
import sys

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

    def exportStorage(self, fileName: str) -> bool:
        cursor = 0
        count = 10000
        size = -1
        totalSize = 0
        binaryContent = {}

        while True:
            cursor, keys = self.redisClient.scan(cursor, '{}*'.format(self.userKeyPrefix), count)
            size = len(keys)
            totalSize += size
            print('Got {} keys of {}. Cursor: {}'.format(len(keys), totalSize, cursor))
            # get all the lists of the received keys
            pipe = self.redisClient.pipeline()
            pipe.multi()
            for key in keys:
                pipe.lrange(key, 0, -1)
            values = pipe.execute()

            # store the binary representation
            for i, key in enumerate(keys):
                binaryContent[key] = values[i]

            if cursor == 0:
                break

        f = open(fileName, "wb")
        pickle.dump(binaryContent, f)
        f.close()

        return True

    def importStorage(self, fileName: str) -> bool:

        f = open(fileName, "rb")
        binaryContentReloaded = pickle.load(f)
        f.close()

        pipe = self.redisClient.pipeline()
        pipe.multi()

        for key in binaryContentReloaded:
            pipe.rpush(key, *binaryContentReloaded[key])

        pipe.execute()

        return True
