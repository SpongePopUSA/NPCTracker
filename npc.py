from enum import Enum
from id import ID

# An enumeration of the different reputation categories that 
class Reputation(Enum):
    _DEFAULT = -1
    TERRIBLE = 1
    BAD = 2
    INDIFFERENT = 3
    GOOD = 4
    GREAT = 5

# Represents a Nonplayer Character
class NPC:
    # Constructor
    def __init__(self, name:str, rep_score:int = 0, is_alive = True):
        # NPC ID
        self.ident = ID(self, 1)
        # NPC name
        self.name = name
        # NPC reputation score
        self.rep_score = rep_score
        # NPC reputation category
        self.rep_category = self.evaluateRepCategory()
        # NPC death status
        self.is_alive = is_alive
    # String representation of object
    def __str__(self):
        return self.name
    
    # Returns the current reputation category of NPC
    def evaluateRepCategory(self):
        # If num < -10
        if (self.rep_score < -10):
            self.rep_score = -10
            return self.evaluateRepCategory()
        # If -10 < num <= -6
        elif (self.rep_score <= -6):
            return Reputation.TERRIBLE
        # If -6 < num <= -1
        elif (self.rep_score <= -1):
            return Reputation.BAD
        # If num 0 == 0
        elif (self.rep_score == 0):
            return Reputation.INDIFFERENT
        # If 0 < num <= 5
        elif (self.rep_score <= 5):
            return Reputation.GOOD
        # If 5 < num <= 10
        elif (self.rep_score <= 10):
            return Reputation.GREAT
        # If 10 < num
        else:
            self.rep_score = 10
            return self.evaluateRepCategory()
        
    # Changes reputation score of NPC by delta and updates reputation category
    def changeRepScore (self, delta:int):
        # Change reputation score
        self.rep_score = self.rep_score + delta
        # Change reputation category
        self.rep_category = self.evaluateRepCategory()
        return
    def changeDeathStatus (self, killed = True):
        self.is_alive = not killed
        return
    # Returns a summary of NPC
    def getSummary (self) -> str:
        result = """
        Summary of {0}:

      Reputation Score  :  {1}

   Reputation Category  :  {2}
        
                Alive?  :  {3}
                """.format(self.name, self.rep_score, self.rep_category.name.capitalize(), self.is_alive)

        return result