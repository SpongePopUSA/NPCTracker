# primary.py
# This program keeps track of NPC's in the Elcria Campaign

from decorator import *
from id import IDTracker
from npc import NPC
from event import Event, Date, Month
from openpyxl import *
from openpyxl.worksheet.worksheet import Worksheet
import time

# Initialize workbook and worksheet
wb:Workbook = load_workbook("TestSheet.xlsx")
ws:Worksheet = wb.active
# Bounds of npc table
npcBounds = {
    "topRow"    : 4,
    "leftCol"   : 2,
    "rightCol"  : 3
}
# Bounds of event table
eventBounds = {
    "topRow"    : 4,
    "leftCol"   : 5,
    "rightCol"  : 11
}
# Create npc and event lists
eventsList:list[Event] = []
npcList:list[NPC] = []

# Load workbook and pull data on NPC's and Events
def initializeData ():
    print("Initializing NPC's...\n")
    # Iterate across NPC table
    for val in ws.iter_rows(min_row = npcBounds["topRow"], min_col = npcBounds["leftCol"], max_col = npcBounds["rightCol"], values_only = True):
        if (val[0] != None):
            # Store name
            name = str(val[0])
            # Add NPC to list
            new_NPC = NPC(name = name)
            npcList.append(new_NPC)
            # Display progress with time delay for aesthetics
            print("Initialized: {0}".format(new_NPC))
            time.sleep(.03)
        else:
            continue
    print("\nDone.\n")

    print("Initializing events...\n")
    # Iterate across event table
    for val in ws.iter_rows(min_row = eventBounds["topRow"], min_col = eventBounds["leftCol"], max_col = eventBounds["rightCol"], values_only = True):
        if val[0] != None:
            # Store title
            title = val[0]
            # Store day
            d = int(val[1])
            # Store month
            m = int(val[2])
            # Store year
            y = int(val[3])

            # Store list of affected/delta pairs
            ad_pairs:list[str] = str(val[4]).split(",")
            # List of (affected, delta) tuples
            ad_tuples:list[tuple[str, int]] = []
            # Populate ad_tuples
            for p in ad_pairs:
                if p != "None":
                    # String
                    split_pair = p.split("/")
                    # String representation of character's ID
                    id_string = split_pair[0] + 'n'
                    # Integer representing the change in character's reputation score
                    delta = int(split_pair[1])
                    ad_tuples.append((id_string, delta))

            # List of id_strings of killed NPC's
            killed_list:list[str] = []
            for i in str(val[5]).split(','):
                if i != "None":
                    killed_list.append(i + 'n')
            # Add event to list
            new_event = Event(title = title, date = Date(d, m, y), involved = ad_tuples, killed = killed_list)
            eventsList.append(new_event)
            # Display progress with time delay for aesthetics
            print("Initialized: {0}".format(new_event))
            time.sleep(.03)

        else:
            break
    print("\nDone.")
        
# Display naviagation options
def displayMainMenu ():
    # Gap
    print("\n")
    menu_message = """ 
Welcome to Elcria's NPC Tracker! 

Please select from the following:

     1  :  Get NPC info
     2  :  Get event nfo
     3  :  Add NPC
     4  :  Add event
           
    -1  :  Exit

    """

    choice = None
    while choice == None:
        print(menu_message)
        choice = input("Selection: ")
        if choice.lstrip('-').isnumeric():    
            match int(choice):
                case 1:
                    decorate(showNPCInfo, item = '#')
                    choice = None
                case 2:
                    decorate(showEventInfo, item = '#')
                    choice = None
                case 3:
                    decorate(addNewNPC, item = '#')
                    choice = None
                case 4:
                    decorate(addNewEvent, item = '#')
                    choice = None
                case -1:
                    return
                case _:
                    print("Please input a valid choice.")
                    choice = None
                    continue
        else:
            print("Please input a number.")
            choice = None
            continue

    # Gap
    print("\n")

# Search for an NPC and display its info to the user           
def showNPCInfo ():
    # Intro message
    print("Welcome to the NPC search!\nType <EXIT> at any time to return to the main menu.\n")

    choice = None
    while choice == None:
        choice = input("\nPlease input the NPC's ID without holder tag (or <EXIT> to quit): ").strip()
        if (choice == "<EXIT>"):
            return
        elif IDTracker.checkId(choice + 'n'):
            character:NPC = IDTracker.findByID(choice + 'n')
            print(character.getSummary())
            choice = None
        else:
            print("No NPC was found with that ID.")
            choice = None
# Search for an event and display its info to the user           
def showEventInfo ():
    # Intro message
    print("Welcome to the event search!\nType <EXIT> at any time to return to the main menu.\n")

    choice = None
    while choice == None:
        choice = input("\nPlease input the event's ID without holder tag: ").strip()
        if (choice == "<EXIT>"):
            return
        elif IDTracker.checkId(choice + 'e'):
            event:NPC = IDTracker.findByID(choice + 'e')
            print(event.getSummary())
        else:
            print("No event was found with that ID.")
            choice = None
# Create a new NPC
def addNewNPC ():
    # Intro message
    print("Welcome to the NPC creation wizard!\nType <EXIT> at any time to return to the main menu.\n")

    # Prompt for NPC name
    character_name = None
    while character_name == None:
        character_name = input("Please input the NPC's name : ").strip()
        if character_name.lstrip(" ") == "":
            print("Please input a name.")
            character_name = None
        elif character_name == "<EXIT>":
            return
    # Prompt for starting reputation score
    reputation = None
    while reputation == None:
        reputation = input("Please input the character's starting reputation (-10 : 10): ").strip()
        
        if reputation.lstrip('-').isnumeric():
            reputation = int(reputation)
        elif reputation == "<EXIT>":
            return
        else:
            print("Please input a number.")
            reputation = None
    
    new_npc = NPC(name = character_name, rep_score = reputation, is_alive = True)
    npcList.append(new_npc)

    update(update_npcs = True)
    print("Saving...")
    # wb.save("TestSheet.xlsx")

# Create a new NPC
def addNewEvent ():
    # Prompt the user to generate a list of NPC/delta pairs
    def promptInvolvedList () -> list[tuple[str, int]]:
        involved_list:list[tuple[str, int]] = []

        adding_pair:bool = True
        while adding_pair:
            character_id_string = ""
            delta:int = None

            involved_string = ""
            for i in involved_list:
                character:NPC = IDTracker.findByID(i[0])
                delta_string:str = ""
                if i[1] >= 0:
                    delta_string = '+' + str(i[1])
                else:
                    delta_string = str(i[1])
                involved_string = involved_string + character.name + ' (' + delta_string + ')' + ", "
            involved_string = involved_string.rstrip(", ")
            if len(involved_list) == 0:
                print("\nNo involved NPC's.\n")
            else:
                print("\nInvolved: " + involved_string + "\n")
            
            choice = 'Y'
            while choice == 'Y':
                choice = input("Add involved NPC? (Y/N) ").strip().upper()
                match choice:
                    case 'Y':
                        character_name = None
                        while character_name == None:
                            character_name = input("Please input the name of the involved NPC: ").strip()
                            character:NPC = None
                            if character_name == "<EXIT>":
                                return -1
                            character_name = character_name.lower()
                            for n in npcList:
                                if n.name.lower() == character_name:
                                    character = n
                                else:
                                    continue
                            if character != None:
                                character_id_string = str(character.ident)
                            else:
                                print("Please input a valid NPC name.")
                                character_name = None
                        while delta == None:
                            delta_input = input("Please input the change in reputation score for this NPC: ").strip()
                            if delta_input.lstrip('-').isnumeric():
                                delta = int(delta_input)
                            else:
                                print("Please input a valid integer.")
                                delta = None
                        break
                    case 'N':
                        adding_pair = False
                        break
                    case "<EXIT>":
                        return -1
                    case _:
                        print("Please input a valid option")
                        choice = 'Y'
            
            if character_id_string != '' and delta != None:
                involved_list.append((character_id_string, delta))

        return involved_list
    # Prompt the user to generate a list of killed NPC's
    def promptKilledList () -> list[str]:
        killed_list:list[str] = []

        adding_npc:bool = True
        while adding_npc:
            character_id_string = ""

            killed_string = ""
            for k in killed_list:
                character:NPC = IDTracker.findByID(k)
                killed_string = killed_string + character.name + ", "
            killed_string = killed_string.rstrip(", ")
            if len(killed_list) == 0:
                print("\nNo killed NPC's.\n")
            else:
                print("\nKilled: " + killed_string + "\n")
            
            choice = 'Y'
            while choice == 'Y':
                choice = input("Add killed NPC? (Y/N) ").strip().upper()
                match choice:
                    case 'Y':
                        character_name = None
                        while character_name == None:
                            character_name = input("Please input the name of the killed NPC: ").strip().lower()
                            character:NPC = None
                            for n in npcList:
                                if n.name.lower() == character_name:
                                    character = n
                                else:
                                    continue
                            if character != None:
                                character_id_string = str(character.ident)
                            else:
                                print("Please input a valid NPC name.")
                                character_name = None
                        break
                    case 'N':
                        adding_npc = False
                        break
                    case "<EXIT>":
                        return -1
                    case _:
                        print("Please input a valid option")
                        choice = 'Y'
            
            if (character_id_string != ''):
                killed_list.append(character_id_string)

        return killed_list
    
        
    # Intro message
    print("Welcome to the event creation wizard!\nType <EXIT> at any time to return to the main menu.\n")

    # Prompt for event title/description
    event_title = None
    while event_title == None:
        event_title = input("Please input a single-sentence description of the event: ")
        if event_title.strip() == "":
            print("Please input a description.")
            event_title = None
        elif event_title == "<EXIT>":
            return
    # Prompt for event date
    event_day = None
    while event_day == None:
        event_day = input("Please input the day of the month: ")
        if event_day.lstrip('-').isnumeric() and 1 <= int(event_day) <= 27:
            event_day = int(event_day)
        elif event_day== "<EXIT>":
            return
        else:
            print("Please input a valid day.")
            event_day = None
    event_month = None
    while event_month == None:
        event_month = input("Please input the month: ")
        if event_month.isnumeric():
            if 1 <= int(event_month) <= 16:
                event_month = Month(int(event_month))
            else:
                print("Please input a valid month.")
                event_month = None
        elif event_month.strip().upper() in Month.__members__:
            event_month = Month[event_month.strip().upper()]
        elif event_title == "<EXIT>":
            return
        else:
            print("Please input a valid month.")
            event_month = None
    event_year = None
    while event_year == None:
        event_year = input("Please input the year: ")
        if event_year.lstrip('-').isnumeric() and 1 <= int(event_day) <= 27:
            event_year = int(event_year)
        elif event_year == "<EXIT>":
            return
        else:
            print("Please input a valid year.")
            event_year = None
    
    event_date = Date(event_day, event_month, event_year)
    # Prompt for list of NPC/delta pairs
    delta_pairs = promptInvolvedList()
    if delta_pairs == -1:
        return
    # Prompt for list of killed NPC's
    killed_npcs = promptKilledList()
    if killed_npcs == -1:
        return

    new_event = Event(event_title, event_date, delta_pairs, killed_npcs)
    eventsList.append(new_event)
    print("\nAdded event: " + str(new_event)+ " (ID Number " + str(new_event.ident) + ")")

    update(update_events = True)
    print("Saving...")
    # wb.save("TestSheet.xlsx")

# Update workbook with current NPC's and Events
def update(update_npcs:bool = True, update_events:bool = True):
    # wb.save("PartyStatus_Backup.xlsx")

    if update_npcs:
        print("\nUpdating NPC's...\n")
    
        r:int = None
        # Fill NPC data
        for character in npcList:
            # Get appropriate row from id
            r = character.ident.num + 3

            # Update npc cells
            ws.cell(r, 2).value = character.name
            ws.cell(r, 3).value = character.ident.num
            ws.cell(r, 4).value = character.rep_score
            ws.cell(r, 5).value = character.rep_category.name
            ws.cell(r, 6).value = character.is_alive
        
        print("\nDone.\n")
    
    if update_events:
        print("Updating Events...\n")

        # Update event cells
        for event in eventsList:
            # Get appropriate row from id
            r = event.ident.num + 3

            ws.cell(r, 8).value = event.title
            ws.cell(r, 9).value = event.date.day_num
            ws.cell(r, 10).value = event.date.month
            ws.cell(r, 11).value = event.date.year
            ws.cell(r, 12).value = "Age of the First Pantheon"
            # Update affected/delta cell
            if len(event.involved) == 0:
                ws.cell(r, 13).value = "None"
            else:
                ad_string = ""
                for ad_tuple in event.involved:
                    character:NPC = IDTracker.findByID(ad_tuple[0])
                    id_num = str(character.ident.num)
                    delta = str(ad_tuple[1])
                    ad_string = ad_string + id_num + "/" + delta + ","
                # Remove comma at the end of ad_string
                ad_string = ad_string[:-1]
                ws.cell(r, 13).value = ad_string
            # Update killed cell
            if len(event.killed) == 0:
                ws.cell(r, 14).value = "None"
            else:
                killed_string = ""
                for id_string in event.killed:
                    character:NPC = IDTracker.findByID(id_string)
                    id_num = str(character.ident.num)
                    killed_string = killed_string + id_num + ","
                # Remove comma at the end of killed_string
                killed_string = killed_string[:-1]
                ws.cell(r, 14).value = killed_string
            # Update the id cell
            ws.cell(r, 15).value = event.ident.num
        
        print("\nDone.\n")

# Save changes to workbook and close
def saveAndClose ():
    print("Saving...")
    # wb.save("TestSheet.xlsx")
    wb.close()

def main():
    initializeData()
    displayMainMenu()
    update()
    saveAndClose()

decorate(main)