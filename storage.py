class StorageInterface:
    def addContest(self, contestTitle: str, details: str) -> bool:
        """Add a contest."""
        pass

    def getContest(self, contestTitle: str) -> str:
        """Return the contest details."""
        pass

    def deleteContest(self, contestTitle: str) -> bool:
        """Delete the contest"""
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
