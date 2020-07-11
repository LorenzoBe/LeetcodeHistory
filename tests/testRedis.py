import configparser
import json
import redis
import unittest

config = configparser.ConfigParser()
config.read('../config.ini')
redisHostname = config['Redis']['Hostname']
redisKey = config['Redis']['Key']
redisPort = int(self.config['Redis']['Port'])
redisSSL = self.config['Redis']['SSL'] == 'True'

r = redis.StrictRedis(host=redisHostname, port=redisPort, password=redisKey, ssl=redisSSL)

class TestRedisConnectivity(unittest.TestCase):

    # test if redis ping is working, so if we have an active connection
    def test_ping(self):
        result = r.ping()
        self.assertTrue(result)

    # test basig set and get redis operations
    def test_set_get(self):
        key = 'key'
        value = 'value12345'

        r.delete(key)
        self.assertTrue(r.set(key, value))
        result = r.get(key)
        self.assertEqual(value, result.decode())
        self.assertTrue(r.delete(key))

    # test the upload of collections as JSON elements of a list
    def test_json(self):
        userId = 'user:1'
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
        r.delete(userId)

        # send all entries
        for data in contestsData:
            jsonData = json.dumps(data)
            r.rpush(userId, jsonData)

        # download and compare all entries
        for idx, e in enumerate(r.lrange( userId, 0, -1 )):
            recreatedData =  json.loads(e.decode())
            self.assertEqual(contestsData[idx], recreatedData)

        # delete the record
        self.assertTrue(r.delete(userId))

if __name__ == '__main__':
    unittest.main()
