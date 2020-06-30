import json
import requests
import time
import unittest

class TestHTTPRequests(unittest.TestCase):
    # test get HTML page
    def test_get_request(self):
        response = requests.get("https://leetcode.com/contest/biweekly-contest-29/ranking/1/")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.text), 0)
    
    # test the get and parse of context details
    def test_get_contest_details(self):
        response = requests.get("https://leetcode.com/contest/api/info/biweekly-contest-29/")
        self.assertEqual(response.status_code, 200)
        responseJson = json.loads(response.text)
        
        contest = responseJson['contest']
        results = '{} {}\n'.format(contest['title'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(contest['start_time'])))
        print(results)

    # test the get and parse of context results
    def test_get_contest_results(self):
        response = requests.get("https://leetcode.com/contest/api/ranking/biweekly-contest-29/?pagination=1&region=global")
        self.assertEqual(response.status_code, 200)
        responseText = response.text
        responseJson = json.loads(responseText)
        results = ""

        for user in responseJson['total_rank']:
            results += '{} {} {} {}\n'.format(user['rank'], user['username'], user['score'], user['finish_time'])
        print(results)
        self.assertEqual(25, len(responseJson['total_rank']))

if __name__ == '__main__':
    unittest.main()

