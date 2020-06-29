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

class LeetCodeCrawler:

    def getContestDetails(self, uri):
        res, text = PageSniffer.getPageText(uri)

        if not res:
            return False, []

        contest = json.loads(text)['contest']
        return True, contest

    def getContestRankPage(self, uri, page):
        fullUri = '{}/{}{}{}'.format(uri, '?pagination=', page, '&region=global')
        print(fullUri)
        res, text = PageSniffer.getPageText(fullUri)

        if not res:
            return False, []

        rank = json.loads(text)
        return True, rank['total_rank']

    def getContestRankFull(self, uri):
        page = 1
        fullRank = []
        res = True

        while res:
            res, rank = self.getContestRankPage(uri, page)
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
