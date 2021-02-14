from configparser import ConfigParser
import glob
import json
import pickle
import sys
import time

from storage import StorageInterface

class PyDictStorage(StorageInterface):

    def __init__(self, config: ConfigParser):
        self.config = config
        self.data = {}

        self.contestKey = 'contests'
        self.userKeyPrefix = 'userId:'
        self.lockKeyName = 'lock'

    def addContest(self, details: str) -> bool:
        if self.contestKey not in self.data:
            self.data[self.contestKey] = []

        self.data[self.contestKey].append(details)
        return True

    def getContests(self) -> list:
        return self.data.get(self.contestKey, [])

    def deleteContests(self) -> bool:
        return self.data.pop(self.contestKey, None)

    def addContestResult(self, username: str, result: str) -> bool:
        userKey = self.userKeyPrefix + username
        if userKey not in self.data:
            self.data[userKey] = []

        self.data[userKey].append(result)
        return True

    def getAllContestsResults(self, username: str) -> list:
        username = self.userKeyPrefix + username
        return self.data.get(username.encode('ascii'), [])

    def deleteUser(self, username: str) -> bool:
        self.data.pop(self.userKeyPrefix + username, None)
        return True

    def exportStorage(self, fileName: str) -> bool:
        f = open(fileName, "wb")
        pickle.dump(self.data, f)
        f.close()

        return True

    def importStorage(self, fileName: str) -> bool:
        print(f"Importing...")
        if fileName == '':
            backupFiles = sorted(glob.glob('backup-*.p'))
            if len(backupFiles) > 0:
                fileName = backupFiles[-1]
            else:
                return False

        print(f"Going to import: {fileName}")
        f = open(fileName, "rb")
        self.data = pickle.load(f)
        f.close()

        return True

    def isEmpty(self) -> bool:
        return len(self.data) == 0
