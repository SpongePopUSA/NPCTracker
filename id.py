class ID:
    _next_npc = 1
    _next_event = 1
    _next_other = 1

    # Constructor, t = int representing type of holder (1= NPC, 2 = Event, Other = Other)
    def __init__ (self, holder, t:int = 3):
        self.holder = holder
        self.num:int = None
        self.tag:chr = None
        match (t):
            case 1:
                self.num = ID._next_npc
                ID._next_npc += 1
                self.tag = 'n'
            case 2:
                self.num = ID._next_event
                ID._next_event += 1
                self.tag = 'e'
            case _:
                self.num = ID._next_other
                ID._next_other += 1
                self.tag = 'o'
        IDTracker.usedIDs.append(self)

    def __str__ (self):
        return str(self.num) + self.tag
# Tracks used ID's
class IDTracker:
    usedIDs:list[ID] = []
    
    @staticmethod
    # Returns the ID object represented by id_string
    def idFromString (id_string:str) -> ID:
        clean_id = id_string.replace(" ", "")
        
        for i in IDTracker.usedIDs:
            if (str(i) == clean_id):
                return i
            else:
                continue
    # Returns the holder of the id represented by id_string
    def findByID (id_string:str) -> ID:
        true_id = IDTracker.idFromString(id_string)

        return true_id.holder
    # Returns true if the string represents a known ID
    def checkId (id_string:str) -> bool:
        result = False
        
        if IDTracker.idFromString(id_string) in IDTracker.usedIDs:
            result = True
        else:
            result = False

        return result
    # Returns usedIDs as a string
    def getUsedIDString () -> str:
        result = ""
        for id in IDTracker.usedIDs:
            result = result + str(id) + ','
        result = result.rstrip(',')

        return result
