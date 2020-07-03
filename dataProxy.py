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
        self.redis = RedisStorage(config)

    def pushContest(self, type: Contest, id: int) -> bool:
        contestId = self.leetcode.generateContestId(type, id)

        # get and store the contest details
        res, contest = self.leetcode.getContestDetails(contestId)
        if not res: return False
        self.redis.addContest(contestId, self.leetcode.contestToJson(contest))

        # get and store the contest rank
        ranks = self.leetcode.getContestRankFull(contestId)

        for userRank in ranks:
            username, result = self.leetcode.resultToJson(contestId, userRank, contest['start_time'])
            self.redis.addContestResult(username, result)

        return True

    def getUser(self, username: str) -> list:
        return self.redis.getAllContestsResults(username)
