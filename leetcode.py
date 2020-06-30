from configparser import ConfigParser
from enum import Enum
import json
import requests
import time

class PageSniffer:

    @staticmethod
    def getPageText(uri):
        response = requests.get(uri)
        if response.status_code != 200:
            return False, ""

        return True, response.text

class Contest(Enum):
    STANDARD = 1
    BIWEEKLY = 2

class LeetCodeCrawler:

    def __init__(self, config: ConfigParser):
        self.config = config
        self.contestInfoUri = "https://leetcode.com/contest/api/info/"
        self.contestRankingUri = "https://leetcode.com/contest/api/ranking/"

    def getContestDetails(self, contestId):
        uri = self.contestInfoUri + contestId
        res, text = PageSniffer.getPageText(uri)

        if not res:
            return False, []

        contest = json.loads(text)['contest']
        return True, contest

    def getContestRankPage(self, contestId, page):
        fullUri = '{}{}/{}{}{}'.format(self.contestRankingUri, contestId, '?pagination=', page, '&region=global')
        print(fullUri)
        res, text = PageSniffer.getPageText(fullUri)

        if not res:
            return False, []

        rank = json.loads(text)
        return True, rank['total_rank']

    def getContestRankFull(self, contestId, startPage = 1):
        page = startPage
        fullRank = []
        res = True

        while res:
            res, rank = self.getContestRankPage(contestId, page)
            if not res or len(rank) == 0:
                break

            fullRank.extend(rank)
            page += 1
            time.sleep(0.001)

        return fullRank

    def contestToJson(self, contestData):
        pyData = {}
        pyData['t'] = contestData['title']
        pyData['st'] = contestData['start_time']

        jsonData = json.dumps(pyData)
        return jsonData

    def resultToJson(self, contestId, result):
        username = result['username']

        pyResult = {}
        pyResult['id'] = contestId
        pyResult['r'] = result['rank']
        pyResult['s'] = result['score']
        pyResult['ft'] = result['finish_time']

        jsonResult = json.dumps(pyResult)
        return username, jsonResult

    def generateContestId(self, type: Contest, id: int):
        if type == Contest.STANDARD:
            return 'weekly-contest-{}'.format(id)
        elif type == Contest.BIWEEKLY:
            return 'biweekly-contest-{}'.format(id)

        return str(id)
