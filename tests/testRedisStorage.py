import configparser
import json
import sys
import unittest

sys.path.append('../')
from redisStorage import RedisStorage

class TestRedisStorage(unittest.TestCase):

    def test_insert_contest(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        redis = RedisStorage(config)

        contestDetails = {
            'title': 'Biweekly Contest 29',
            'start_time': '1593268200'
        }
        contestTitle = contestDetails['title']

        # delete any previous record
        redis.deleteContest(contestTitle)

        # store the contest
        redis.addContest(contestTitle, json.dumps(contestDetails))

        # download and compare
        recreatedData =  json.loads(redis.getContest(contestTitle).decode())
        self.assertEqual(contestDetails, recreatedData)

        # delete the record
        self.assertTrue(redis.deleteContest(contestTitle))


    def test_insert_user_contests(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        redis = RedisStorage(config)

        username = 'terence'
        contestsData = [
            {
                'contestId': '1',
                'timestamp': '1111111111',
                'finishTime': '666',
                'score': '12',
                'rank': '888'
            },
            {
                'contestId': '2',
                'timestamp': '2222222222',
                'finishTime': '777',
                'score': '23',
                'rank': '999'
            }
        ]

        # delete any previous record
        redis.deleteUser(username)

        # send all entries
        for data in contestsData:
            jsonData = json.dumps(data)
            redis.addContestResult(username, jsonData)

        # download and compare all entries
        for idx, e in enumerate(redis.getAllContestsResults(username)):
            recreatedData =  json.loads(e.decode())
            self.assertEqual(contestsData[idx], recreatedData)

        # delete the record
        self.assertTrue(redis.deleteUser(username))

if __name__ == '__main__':
    unittest.main()
