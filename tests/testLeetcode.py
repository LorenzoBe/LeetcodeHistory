import sys
import time
import unittest

sys.path.append('../')
from leetcode import Contest
from leetcode import PageSniffer
from leetcode import LeetCodeCrawler

class TestLeetcode(unittest.TestCase):
    # test PageSniffer
    def test_page_sniffer(self):
        res, text = PageSniffer.getPageText("https://leetcode.com/contest/biweekly-contest-29/ranking/1/")
        self.assertTrue(res)
        self.assertGreater(len(text), 0)

    def test_generate_contest_id(self):
        lcc = LeetCodeCrawler()
        self.assertEqual(lcc.generateContestId(Contest.STANDARD, 123), "weekly-contest-123")
        self.assertEqual(lcc.generateContestId(Contest.BIWEEKLY, 456), "biweekly-contest-456")

    # test to get context details
    def test_get_contest_details(self):
        lcc = LeetCodeCrawler()
        contestId = lcc.generateContestId(Contest.BIWEEKLY, 29)
        res, contest = lcc.getContestDetails(contestId)
        self.assertTrue(res)

        # later use: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(contest['start_time']
        results = contest['title'] + " -> " + lcc.contestToJson(contest) + "\n"
        print(results)

    # test the get and parse of context results
    def test_get_contest_results(self):
        page = 1
        lcc = LeetCodeCrawler()
        contestId = lcc.generateContestId(Contest.BIWEEKLY, 29)
        res, rank = lcc.getContestRankPage(contestId, page)
        self.assertTrue(res)

        results = ""
        for user in rank:
            username, result = lcc.resultToJson(contestId, user)
            results += username + " -> " + result + "\n"
        print(results)
        self.assertEqual(25, len(rank))

    # test the get and parse all context results
    def test_get_all_contest_results(self):
        lcc = LeetCodeCrawler()
        contestId = lcc.generateContestId(Contest.BIWEEKLY, 29)

        fullRank = lcc.getContestRankFull(contestId, 310)
        print(len(fullRank))

if __name__ == '__main__':
    unittest.main()

