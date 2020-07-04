from configparser import ConfigParser
import sys
import requests

config = ConfigParser()
config.read('../config.ini')

def populate(type: str, startId: int, endId: int):
    for id in range(startId, endId + 1):
        print('Requesting push for contest {} of type {}...'.format(id, type))
        res = False
        payload = {'type': type, 'id': str(id)}
        basicAuth = requests.auth.HTTPBasicAuth(config['WebApp']['AdminUsername'], config['WebApp']['AdminPassword'])
        response = requests.get("{}/addContest".format(config['WebApp']['URL']), params=payload, auth=basicAuth)
        print('Push completed: {}'.format(response.status_code))

if __name__ == '__main__':
    if (len(sys.argv) < 4):
        print('Arguments error. Usage: {} <contest type> <start id> <end id>'.format(sys.argv[0]))
        sys.exit(0)

    type = sys.argv[1]
    startId = int(sys.argv[2])
    endId = int(sys.argv[3])

    populate(type, startId, endId)
