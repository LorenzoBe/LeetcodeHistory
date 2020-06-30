import json

from leetcode import Contest
from leetcode import PageSniffer
from leetcode import LeetCodeCrawler
from redisStorage import RedisStorage

class DataPusher():

    def __init__(self):
        self.leetcode = LeetCodeCrawler()
        self.redis = RedisStorage()

    def pushContest(self, type: Contest, id: int) -> bool:
        contestId = self.leetcode.generateContestId(type, id)

        # get and store the contest details
        res, contest = self.leetcode.getContestDetails(contestId)
        if not res: return False
        self.redis.addContest(contestId, self.leetcode.contestToJson(contest))

        # get and store the contest rank
        ranks = self.leetcode.getContestRankFull(contestId, 315)
        
        for userRank in ranks:
            username, result = self.leetcode.resultToJson(contestId, userRank)
            self.redis.addContestResult(username, json.dumps(result))
        
        return True
