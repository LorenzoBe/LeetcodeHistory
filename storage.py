class StorageInterface:
    def addContest(self, details: str) -> bool:
        """Add a contest."""
        pass

    def getContests(self) -> list:
        """Return all the contest details."""
        pass

    def deleteContests(self) -> bool:
        """Delete all the contests"""
        pass

    def addContestResult(self, username: str, result: str) -> bool:
        """Add a single contest result."""
        pass

    def getAllContestsResults(self, username: str) -> list:
        """Return all the contests results."""
        pass

    def deleteUser(self, username: str) -> bool:
        """Delete the user key."""
        pass
