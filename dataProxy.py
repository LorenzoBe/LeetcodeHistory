from configparser import ConfigParser
import json

from leetcode import Contest
from leetcode import PageSniffer
from leetcode import LeetCodeCrawler
from redisStorage import RedisStorage

class DataProxy():

    def __init__(self, config: ConfigParser):
        self.config = config
        self.leetcode = LeetCodeCrawler(config)
        self.storage = RedisStorage(config)

    def pushContest(self, type: Contest, id: int) -> bool:
        contestId = self.leetcode.generateContestId(type, id)

        # get the contest details
        res, contest = self.leetcode.getContestDetails(contestId)
        if not res: return False

        # get the contest rank
        ranks = self.leetcode.getContestRankFull(contestId)

        # try to acquire the lock and  store the new data
        res, token = self.storage.acquireLock(600)
        if not res: return False

        self.storage.addContest(self.leetcode.contestToJson(contest))

        for userRank in ranks:
            username, result = self.leetcode.resultToJson(contestId, userRank, contest['start_time'])
            self.storage.addContestResult(username, result)

        self.storage.releaseLock(token)

        return True

    def getUser(self, username: str) -> list:
        # if the storage is empty, try to recover it from the last backup
        if self.storage.isEmpty():
            res, token = self.storage.acquireLock(240)
            if not res:
                return False

            self.storage.importStorage('')
            self.storage.releaseLock(token)

        return self.storage.getAllContestsResults(username)

    def exportStorage(self, fileName: str) -> bool:
        return self.storage.exportStorage(fileName)

    def importStorage(self, fileName: str) -> bool:
        return self.storage.importStorage(fileName)
