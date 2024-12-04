from enum import IntEnum
from id import ID, IDTracker
from npc import NPC

# An enumeration representing the different months in Elcria
class Month(IntEnum):
    VOST = 1
    CONTEMPLATION = 2
    PROMISE = 3
    SIGHT = 4
    BLOOMING = 5
    FLOURISHING = 6
    GRAZING = 7
    SKAIRN = 8
    SUNSGLOW = 9
    HEFT = 10
    RISING = 11
    MELLOWING = 12
    WITHERING = 13
    EARLY_BLIGHT = 14
    FULL_BLIGHT = 15
    FINUS = 16
# An enumeration representing days of the week
class WeekDay(IntEnum):
    GODSDAY = 1
    IGDAY = 2
    HILTSDAY = 3
    RESTDAY = 4
    STAINDAY = 5
    RENDSDAY = 6
    LUXDAY = 7
    FOGDAY = 8
    ORDAY = 9
                    
# Represents a date in Elcria
class Date:
    # Constructor
    def __init__ (self, day_num:int, month:Month, year:int):
        # Current day of the month
        self.day_num = day_num
        # Current month of the year
        self.month = Month(month)
        # Current year
        self.year = year
        # Days since 1/1/0
        self.absolute_day_num = self.day_num + 27 * (self.month - 1) + 432 * (self.year - 1)
        # Day of the week
        self.weekday = WeekDay(self.absolute_day_num % 9 + 1)

        return
    # String representation of the date
    def __str__(self):
        return "{wd}, {d} of {m}, year {y}, Age of the First Pantheon".format(wd = self.weekday.name.capitalize(), m = self.month.name.capitalize(), d = Date.stringify(self.day_num), y = self.year)
    
    @staticmethod
    # Return the string representation of an int with the appropriate suffix
    def stringify (num:int):
        last_digit = num % 10
        suffix = None

        if (last_digit == 0 or last_digit == 4 or last_digit == 5 or last_digit == 6 or last_digit == 7 or last_digit == 8 or last_digit == 9 or num == 11 or num == 12 or num == 13):
            suffix = "th"
        else:
            match last_digit:
                case 1:
                    suffix = "st"
                case 2:
                    suffix = "nd"
                case 3:
                    suffix = "rd"

        return str(num) + suffix

class Event:
    # Constructor
    def __init__ (self, title:str, date:Date, involved:list[tuple[str, int]] = [], killed:list[str] = []):
        # Event ID
        self.ident = ID(self, 2)
        # Title of the event
        self.title = title
        # Date of the event
        self.date = date
        # A list of tuples where tuple[0] = Involved NPC ID as string, tuple[1] = Reputation score delta
        self.involved = involved
        # A list of ID's of NPC's killed in the event
        self.killed = killed

        # Update reputation scores of NPC(s) involved
        for i in self.involved:
            character = IDTracker.findByID(i[0])
            character.changeRepScore(i[1])
        # Update status of NPC's killed in event
        for n in self.killed:
            character = IDTracker.findByID(n)
            character.changeDeathStatus(killed = True)
    # String representation of object
    def __str__ (self):
        return self.title
    
    # Returns a summary of Event
    def getSummary (self) -> str:
        killed_string = ""
        for k in self.killed:
            character:NPC = IDTracker.findByID(k)
            killed_string = killed_string + character.name + ", "
        killed_string = killed_string.rstrip(", " )
        involved_string = ""
        for i in self.involved:
            character:NPC = IDTracker.findByID(i[0])
            delta_string:str = ""
            if i[1] >= 0:
                delta_string = '+' + str(i[1])
            else:
                delta_string = str(i[1])
            involved_string = involved_string + character.name + ' (' + delta_string + ')' + ", "
        involved_string = involved_string.rstrip(", ")
        
        result = """
        Summary of {0}:

                 Title  :  {1}

        NPC's Involved  :  {2}
        
          NPC's Killed  :  {3}""".format(str(self.ident), self.title, involved_string, killed_string)

        return result