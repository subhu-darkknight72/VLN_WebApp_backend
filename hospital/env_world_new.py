#### IMPORTS ####
import re
import random
import json
import openai

import os
from dotenv import load_dotenv
load_dotenv()

openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")


#### JSON FILE APPEND FUNCTION ####
file1 = 'play_s3.json'
# check if file exists. If not, create a new file.
try:
    with open(file1) as file:
        pass
except IOError:
    with open(file1, 'w') as file:
        file.write('[]\n')


def write_json(action,obs,num):
    d2 = {   "ACTION" : action, 
             "OBSERVATION" : obs,
            "#Actions Used" : num  }
    with open(file1, 'a') as file:
        file.write(json.dumps(d2) + '\n')


### Language Model ####

def llm(observation, stop=["\n"]):
    response = openai.ChatCompletion.create(
        engine="GPT-4-France",
        messages = [{"role":"user", "content":observation}],
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=stop)
    return response["choices"][0]["message"]["content"]




###########################################################     CLASSES      ###############################################################

####-------- ROOM CLASS -----------####
class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connected_rooms = []
        self.items = []
        self.actions = []
        

    def connect_room(self, room):
        if room not in self.connected_rooms:
            self.connected_rooms.append(room)
            room.connected_rooms.append(self)  # Bidirectional connection

    def get_details(self):
        obs = self.description
        rooms = [i.name for i in self.connected_rooms]
        obs += f"\nThe rooms that we can go from here are : {', '.join(rooms)}. "
        items = [item.name for item in self.items]
        obs += f"\nThe room contains : {', '.join(items)}."
        return obs
    
    def remove_item(self, item_name):
        for item in self.items:
            if item.name == item_name:  # First, try to remove the item directly from the room
                self.items.remove(item)
            
            elif item.contains:
                for i in item.contains:
                    if i.name == item_name:
                        item.contains.remove(i)        # If not found, check if the item is nested within another item

    def add_item(self, item):
        self.items.append(item)

    def add_action(self, action_name):
        self.actions.append(action_name)

    def get_actions(self):
        action_space = ["inventory"]
        for action in self.actions:
            if action == "examine":
                for item in self.items:
                    action_space.append(f"examine {item.name}")
            elif action == "go to":
                for room in self.connected_rooms:
                    action_space.append(f"go to {room.name}")
            elif action == "collect":
                for item in self.items:
                    if item.is_static==False:  # Check for movable objects
                        action_space.append(f"collect {item.name}")
            else:
                action_space.append(action)
        
        return action_space
        
        

    def perform_action(self, action_name, game):
        if action_name in self.actions:
            self.actions[action_name](game)
        else:
            print("Action not available.")


####------------ ITEM CLASS ---------####
class Item:
    def __init__(self, name, description, action=None, is_static=True):
        self.name = name
        self.description = description
        self.action = action
        self.is_static = is_static
        self.contains = []  # List of items contained by this item

    def add_desc(self, desc):
        self.description += desc

    def describe(self):
        obs = f"{self.description} "
        items = [i.name for i in self.contains]
        if self.contains:
            obs += f"It contains: {', '.join(items)}. "
        return obs

    def add_item(self, item):
        self.contains.append(item)

    def remove_item(self, item_name):
        for item in self.contains:
            if item.name == item_name:
                self.contains.remove(item)
                return item
        return None



####-------------- GAME CLASS -----------####
class Game:
    def __init__(self):
        self.current_room = self.create_world()
        self.inventory = []
        self.waste_info = ["used plastic bottle"]
        self.flag=False
        self.num_actions=0

        self.task = "Your task is to dispose waste products inside the doctor chambers. Take actions to first go to each of the doctor chambers and explore the rooms to find waste products. Collect waste items and dispose them to dustbin."
        self.obs = self.current_room.get_details()
        print(self.task)
        print(self.obs)
        
        # Initialize the JSON file
        d1 = {  "TASK" : self.task,
                "OBSERVATION" : self.current_room.get_details()   }
        with open(file1, 'w') as file:
            file.write(json.dumps(d1) + '\n')

    ### Create the World ###
    def create_world(self):
        ###########################################################    ROOMS     ###############################################################
        if True:
            ### ROOMS ###
            hall = Room("hallway", "You are in the hallway. This is the main corridor in the ground floor from which we can go to other rooms. ")
            ch = Room("doctor chamber", "You are in the doctor chamber. Doctors in OPD diagnose patients here. ")
            gen_ward = Room("general ward", "You are in the general ward. There are a total of 5 beds with a nurse station who carries the information of the patients. ")
            comm_toilet = Room("common toilet", "You are in the common toilet. This has a single occupancy. ")
            hall_nurse_st = Room("hallway nurse station", "You are in the nurse station. Nurses are stationed here. ")
            
            ### CONNECT ROOMS ###
            hall.connect_room(ch)
            hall.connect_room(gen_ward)
            hall.connect_room(comm_toilet)
            hall.connect_room(hall_nurse_st)
            
            #### Adding Actions to Rooms ####
            hall.add_action("go to")
            ch.add_action("go to")
            gen_ward.add_action("go to")
            comm_toilet.add_action("go to")
            hall_nurse_st.add_action("go to")

        ###########################################################     ITEMS     ###############################################################
        if True:
            #### --------- HALLWAY ----------- ####
            poster = Item("wall poster", "This is a poster comprising a picture of a baby boy smiling. ")
            doctor1 = Item("doctor #1", "He is doctor Ram specializes in orthopedics. ")
            
            hall.add_item(poster)
            hall.add_item(doctor1)
            hall.add_action("examine")
            
            #### -------------------- DOCTOR CHAMBER ----------------------- ####
            doc_table = Item("doctor table", "This table belongs to the doctor who keeps his belongings. ")
            doc_chair = Item("doctor chair", "This chair belongs to the doctor. It is near the doctor table. ")
            doc_bed = Item("patient bed", "This bed in the doctor chamber is used to diagnose OPD patients by the doctor. ")
            doc_bedtable = Item("patient bed table", "This bed table is beside the patient bed. ")
            bin = Item("dustbin", "A dustbin for disposing waste materials")
            
            book = Item("book", "This is an old leather-bound book.", is_static=False)
            lamp = Item("lamp", "This is a small electric lamp.", is_static=False)
            note_pad = Item("note pad", "This is a notebook for the doctor to write notes", is_static=False)
            bottle = Item("used plastic bottle", "This is an used plastic bottle", is_static=False)
            
            doc_table.add_item(book)
            doc_table.add_item(lamp)
            doc_table.add_item(bottle)
            doc_table.add_item(note_pad)
            
            ch.add_item(doc_table)
            ch.add_item(doc_chair)
            ch.add_item(doc_bed)
            ch.add_item(doc_bedtable)
            ch.add_item(bin)
            ch.add_action("examine")
            ch.add_action("collect")
            
            ####-------------------- GENERAL WARD ------------------####
            nurse1 = Item("nurse", "This is a nurse. This nurse have information about where to collect waste information. ")
            pat_bed1 = Item("patient bed-1", "This bed belongs to patient #1. ")
            pat_bed2 = Item("patient bed-2", "This bed belongs to patient #2. ")
            
            gen_ward.add_item(pat_bed1)
            gen_ward.add_item(pat_bed2)
            gen_ward.add_item(nurse1)
            gen_ward.add_action("examine")
            
            ####------------------------- NURSE STATION (HALLWAY) ------------------------####
            comp_station = Item("computer station", "This is a computer station comprising of 3 computers. These are used for extracting information and registration. Can only be accessed by the nurses. ")
            files = Item("filing cabinet", "This is the filing cabinet comprising of different patient files used during treatment by the doctors and nurses. ")
            
            hall_nurse_st.add_item(comp_station)
            hall_nurse_st.add_item(files)
            hall_nurse_st.add_action("examine")

        return hall
    #### Action Functions ####
    
    def add_to_inventory(self, item_name):
        for i in self.current_room.items:
            if i.name == item_name:         # Find item from current room items
                item = i
            elif i.contains:
                for a in i.contains:
                    if a.name == item_name:     # Find item from nested items.
                        item = a
            else:
                obs = f"{item_name} not found in the room. "
        if item:
            if item.is_static==True:
                obs = f"{item_name} cannot be collected. "
            elif item.is_static == False:
                self.inventory.append(item)
                obs = f"{item_name} added to inventory. "
        return obs

    def put_item(self, item_name, target_name):
        # Use an item from the inventory on a target item in the room
        if item_name in [item.name for item in self.inventory]:
            for item in self.current_room.items:
                if item.name == target_name:
                    target_item = item
            if target_item:
                target_item.add_item(self.remove_from_inventory(item_name))
                obs = f"{item_name} placed on {target_name}."
            else:
                obs = f"{target_name} not found in the room."
        else:
            obs = f"{item_name} is not in your inventory."
        return obs

    def remove_from_inventory(self, item_name):
        # Remove and return an item from the inventory
        item = next(item for item in self.inventory if item.name == item_name)
        self.inventory.remove(item)
        return item
    
    def put_actspace(self, act_space):
        for item in self.inventory:
            for i in self.current_room.items:
                if i.is_static==True:
                    act_space.append(f"put {item.name} on {i.name}")                   # Put on items in the current room
                if i.contains:
                    for a in i.contains:
                        if a.is_static==True:
                            act_space.append(f"put {item.name} on {a.name}")           # Put on nested items
        return act_space

    #### Game Loop ####
    
    def start(self):
        current_location = self.current_room.name
        action_space = self.current_room.get_actions()

        while self.num_actions!=50:
            
            act_space = []
            # To include putting items action in the action space
            if self.inventory:
                act_space = self.put_actspace(act_space)
            # To include other actions in the action space
            act_space += list(set(self.current_room.get_actions()))
            print(f"ACTION SPACE : {act_space}")

            choice = input("ACTION : ").lower()
            if choice == "r":
                command = random.choice(act_space)
            else : 
                command = choice
            
            self.num_actions+=1

            if command.startswith("go to"):
                room_name = command[len("go to "):]
                for room in self.current_room.connected_rooms:
                    if room.name == room_name:
                        self.current_room = room
                        self.obs = self.current_room.get_details()
                        break
                    else:
                        self.obs = "Invalid Room!"
            
            elif command.startswith("collect"):
                item_name = command[len("collect "):]
                self.obs = self.add_to_inventory(item_name)
                self.current_room.remove_item(item_name)

            elif command.startswith("put"):
                pattern = r"^put\s+(.*?)\s+on\s+(.*)$"
                match = re.search(pattern, command)
                if match:
                    item_name = match.group(1)  # The first capturing group (item name)
                    target_name = match.group(2)
                self.obs = self.put_item(item_name, target_name)

                # Check for dustbin status
                if bin.contains:
                    items = [i.name for i in bin.contains]
                    if(all(x in items for x in self.waste_info)):
                        self.flag = True
                        self.obs = "You have put waste products in the dustbin and have successfully completed the task!"
                        write_json(command, self.obs, self.num_actions)
                        break
            
            elif command.startswith("examine"):
                item_name = command[len("examine "):]
                for item in self.current_room.items:
                    if item.name == item_name:      # check if the item belongs in the current room.
                        self.obs = item.describe()
                        if item.contains:
                            for i in item.contains:     # if the item belongs to the current room, add its nested items also in the list of items in the current room.
                                self.current_room.add_item(i)
                        break
                    else:
                        self.obs = "Invalid Item"

            elif command == "inventory":
                items = [i.name for i in self.inventory]
                if items:
                    self.obs = f"Your inventory includes : {','.join(items)}. "
                else:
                    self.obs = "Your inventory is empty!"
            
            else:
                self.obs = "Invalid action. Try again!"

            print(f"ACTION : {command}\nOBSERVATION : {self.obs}")
            #write_json(command, self.obs, self.num_actions)






###########################################################     GAMEPLAY     ###############################################################

####-------------- Initialize game with the starting room ----------####
game = Game()

####----------------- Start the game ----------------####
game.start()
print(f"Status : {game.flag} with Number of actions taken : {game.num_actions}")

####----------------- Write the success label to the JSON file ------------------####
if game.flag == True:
    label = 1
elif game.flag == False:
    label = 0
res = {
        "success" : label,
        "Number of actions taken" : game.num_actions
    }
with open(file1, 'a') as file:
    file.write(json.dumps(res) + '\n')