import configparser
import json
import pickle
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

        # delete any previous record
        redis.deleteContests()

        # store the contest
        redis.addContest(json.dumps(contestDetails))
        redis.addContest(json.dumps(contestDetails))

        # download and compare
        contests = redis.getContests()
        for contest in contests:
            recreatedData = json.loads(contest.decode())
            self.assertEqual(contestDetails, recreatedData)

        # delete the record
        self.assertTrue(redis.deleteContests())

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

    @unittest.skip
    def test_export_data(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        redis = RedisStorage(config)

        redisClient = redis.getClient()

        cursor = 0
        count = 10000
        size = -1
        totalSize = 0
        backupContent = ""
        binaryContent = {}

        while True:
            cursor, keys = redisClient.scan(cursor, 'userId:*', count)
            size = len(keys)
            totalSize += size
            print('Got {} keys of {}. Cursor: {}'.format(len(keys), totalSize, cursor))
            pipe = redisClient.pipeline()
            pipe.multi()
            for key in keys:
                pipe.lrange(key, 0, -1)
            values = pipe.execute()

            for i, key in enumerate(keys):
                decodedValues = [value.decode() for value in values[i]]
                decodedKey = key.decode()
                backupContent += '{} {}{}\n'.format(len(decodedKey), decodedKey, decodedValues)
                binaryContent[key] = values[i]

            if cursor == 0:
                break

        f = open("backup.txt", "w")
        f.write(backupContent)
        f.close()

        f = open("binaryBackup.p", "wb")
        pickle.dump( binaryContent, f)
        f.close()

        f = open("binaryBackup.p", "rb")
        binaryContentReloaded = pickle.load(f)
        f.close()

        self.assertEqual(binaryContent, binaryContentReloaded)

    @unittest.skip
    def test_import_data(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        redis = RedisStorage(config)

        redisClient = redis.getClient()
        f = open("binaryBackup.p", "rb")
        binaryContentReloaded = pickle.load(f)
        f.close()

        pipe = redisClient.pipeline()
        pipe.multi()

        for key in binaryContentReloaded:
            pipe.rpush(key, *binaryContentReloaded[key])

        pipe.execute()

if __name__ == '__main__':
    unittest.main()
