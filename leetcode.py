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
