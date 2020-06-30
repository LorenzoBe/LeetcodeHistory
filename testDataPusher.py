import unittest

from dataPusher import DataPusher
from leetcode import Contest

class TestDataPusher(unittest.TestCase):

    def test_contest_upload(self):
        dataPusher = DataPusher()

        res = dataPusher.pushContest(Contest.BIWEEKLY, 29)
        self.assertTrue(res)

if __name__ == '__main__':
    unittest.main()
