import sys
import unittest

sys.path.append('../')
from dataProxy import DataProxy
from leetcode import Contest

class TestDataPusher(unittest.TestCase):

    def test_contest_upload(self):
        dataProxy = DataProxy()

        res = dataProxy.pushContest(Contest.BIWEEKLY, 29)
        self.assertTrue(res)

if __name__ == '__main__':
    unittest.main()
