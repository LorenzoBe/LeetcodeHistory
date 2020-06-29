import time
import unittest

from leetcode import PageSniffer
from leetcode import LeetCodeCrawler

class TestLeetcode(unittest.TestCase):
    # test PageSniffer
    def test_page_sniffer(self):
        res, text = PageSniffer.getPageText("https://leetcode.com/contest/biweekly-contest-29/ranking/1/")
        self.assertTrue(res)
        self.assertGreater(len(text), 0)

    # test to get context details
    def test_get_contest_details(self):
        contestUri = "https://leetcode.com/contest/api/info/biweekly-contest-29"
        lcc = LeetCodeCrawler()
        res, contest = lcc.getContestDetails(contestUri)
        self.assertTrue(res)

        results = '{} {}\n'.format(contest['title'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(contest['start_time'])))
        print(results)

    # test the get and parse of context results
    def test_get_contest_results(self):
        contestUri = "https://leetcode.com/contest/api/ranking/biweekly-contest-29"
        page = 1
        lcc = LeetCodeCrawler()
        res, rank = lcc.getContestRankPage(contestUri, page)
        self.assertTrue(res)

        results = ""
        for user in rank:
            results += '{} {} {} {}\n'.format(user['rank'], user['username'], user['score'], user['finish_time'])
        print(results)
        self.assertEqual(25, len(rank))

    # test the get and parse all context results
    def test_get_all_contest_results(self):
        contestUri = "https://leetcode.com/contest/api/ranking/biweekly-contest-29"
        lcc = LeetCodeCrawler()

        fullRank = lcc.getContestRankFull(contestUri)
        print(len(fullRank))

if __name__ == '__main__':
    unittest.main()

