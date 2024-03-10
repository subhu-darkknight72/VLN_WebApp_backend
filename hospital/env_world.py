#### IMPORTS ####
import re
import random

###########################################################     CLASSES      ###############################################################

#### ROOM CLASS ####
class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connected_rooms = []
        self.items = []
        self.item_names = {}
        self.actions = []
        self.connected_room_names = {}
        self.act_space = ["inventory"]

    def connect_room(self, room):
        if room not in self.connected_rooms:
            self.connected_rooms.append(room)
            room.connected_rooms.append(self)  # Bidirectional connection
            self.connected_room_names[room.name] = room

    def get_details(self):
        obs = self.description
        rooms = [i.name for i in self.connected_rooms]
        obs += f"The rooms that we can go from here are : {', '.join(rooms)}. "
        items = [i.name for i in self.items]
        obs += f"The room contains : {', '.join(items)}."
        return obs
    
    def remove_item(self, item_name):
        # First, try to remove the item directly from the room
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                return item
            # If not found, check if the item is nested within another item
            else:
                nested_item = item.remove_item(item_name)
                if nested_item:
                    return nested_item
        return None

    def add_item(self, item):
        self.items.append(item)
        self.item_names[item.name] = item

    def add_action(self, action_name):
        self.actions.append(action_name)

    def get_actions(self):
        for action in self.actions:
            if action == "examine":
                for item in self.items:
                    self.act_space.append(f"examine {item.name}")
            elif action == "go to":
                for room in self.connected_rooms:
                    self.act_space.append(f"go to {room.name}")
            elif action == "collect":
                for item in self.items:
                    if item.is_static==False:  # Check for movable objects
                        self.act_space.append(f"collect {item.name}")
            else:
                self.act_space.append(action)
        return self.act_space
        
        

    def perform_action(self, action_name, game):
        if action_name in self.actions:
            self.actions[action_name](game)
        else:
            print("Action not available.")

#### ITEM CLASS ####
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
        obs = f"{self.description}. "
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

#### GAME CLASS ####
class Game:
    def __init__(self):
        starting_room = self.create_world()        

        self.current_room = starting_room
        obs = f"You are in the {self.current_room.name}. "
        obs += self.current_room.get_details()
        # print(f"ACTION : initialize and OBSERVATION : {obs}")
        self.inventory = []
    
    ### Create the World ###
    def create_world(self):
        ###########################################################    ROOMS     ###############################################################
        if True:
            ### ROOMS ###
            hall = Room("hallway", "This room is called the hallway. This is the main corridor in the ground floor from which we can go to other rooms. ")
            ch1 = Room("doctor chamber #1", "This is the doctor chamber #1. Doctors in OPD diagnose patients here. ")
            ch2 = Room("doctor chamber #2", "This is the doctor chamber #2. Doctors in OPD diagnose patients here. ")
            gen_ward = Room("general ward", "This is the general ward. There are a total of 5 beds with a nurse station who carries the information of the patients. ")
            icu_ward = Room("icu ward", "This is the general ward. There are a total of 5 beds with a common toilet and a nurse station who carries the information of the patients. ")
            comm_toilet = Room("common toilet", "This is the common toilet in the hallway. This has single occupancy. ")
            nurse_station1 = Room("Nurse Station", "This is the nurse station. You see nurses at work here. You can get information from the nurse station.")
            nurse_station2 = Room("Nurse Station", "This is the nurse station. You see nurses at work here. You can get information from the nurse station.")

            ### CONNECT ROOMS ###
            hall.connect_room(ch1)
            hall.connect_room(ch2)
            hall.connect_room(gen_ward)
            hall.connect_room(icu_ward)
            hall.connect_room(comm_toilet)
            hall.connect_room(nurse_station1)
            ch2.connect_room(nurse_station2)

            #### Adding Actions to Rooms ####
            hall.add_action("go to")
            ch1.add_action("go to")
            ch2.add_action("go to")
            gen_ward.add_action("go to")
            icu_ward.add_action("go to")
            comm_toilet.add_action("go to")
            nurse_station1.add_action("go to")
            nurse_station2.add_action("go to")


        ###########################################################     ITEMS     ###############################################################
        if True:
            #### HALLWAY ITEMS ####
            poster = Item("wall poster", "This is a poster comprising a picture of a baby boy smiling. ")
            doctor1 = Item("doctor #1", "He is doctor Ram specializes in orthopedics. ")
            agent = Item("agent", "You are the agent. Your job is to complete the tasks. ")

            hall.add_item(poster)
            hall.add_item(doctor1)
            hall.add_item(agent)

            hall.add_action("examine")
            hall.get_actions()  # Create the Action-Observation Space

            ### CHAMBER-1 ITEMS ###
            doc_table1 = Item("doctor table", "This table belongs to the doctor who keeps his belongings. ")
            doc_chair1 = Item("doctor chair", "This chair belongs to the doctor. It is near the doctor table. ")
            doc_bed1 = Item("patient bed", "This bed in the doctor chamber is used to diagnose OPD patients by the doctor. ")
            doc_bedtable1 = Item("patient bed table", "This bed table is beside the patient bed. ")
            bin1 = Item("dustbin", "A dustbin for disposing waste materials")

            book1 = Item("book", "An old leather-bound book.", is_static=False)
            lamp1 = Item("lamp", "A small electric lamp.", is_static=False)
            waste_paper1 = Item("waste paper", "A paper to be thrown", is_static=False)
            note_pad1 = Item("note pad", "A notebook for the doctor to write notes", is_static=False)

            doc_table1.add_item(book1)
            doc_table1.add_item(lamp1)
            doc_table1.add_item(waste_paper1)
            doc_table1.add_item(note_pad1)

            ch1.add_item(doc_table1)
            ch1.add_item(doc_chair1)
            ch1.add_item(doc_bed1)
            ch1.add_item(doc_bedtable1)
            ch1.add_item(bin1)

            ch1.add_action("examine")
            ch1.add_action("collect")
            ch1.get_actions()

            #### CHAMBER-2 ITEMS ####
            doc_table2 = Item("doctor table", "This table belongs to the doctor who keeps his belongings. ")
            doc_chair2 = Item("doctor chair", "This chair belongs to the doctor. It is near the doctor table. ")
            doc_bed2 = Item("patient bed", "This bed in the doctor chamber is used to diagnose OPD patients by the doctor. ")
            doc_bedtable2 = Item("patient bed table", "This bed table is beside the patient bed. ")
            peel = Item("banana peel", "A banana peel is lying on the ground of the room", is_static=False)
            bin2 = Item("dustbin", "A dustbin for disposing waste materials")

            book2 = Item("book", "An old leather-bound book.", is_static=False)
            lamp2 = Item("lamp", "A small electric lamp.", is_static=False)
            note_pad2 = Item("note pad", "A notebook for the doctor to write notes", is_static=False)

            doc_table2.add_item(book2)
            doc_table2.add_item(lamp2)
            doc_table2.add_item(note_pad2)

            ch2.add_item(doc_table2)
            ch2.add_item(doc_chair2)
            ch2.add_item(doc_bed2)
            ch2.add_item(doc_bedtable2)
            ch2.add_item(peel)
            ch2.add_item(bin2)

            ch2.add_action("examine")
            ch2.add_action("collect")
            ch2.get_actions()

            #### GENERAL WARD ITEMS ####
            nurse1 = Item("Nurse", "This is a nurse. This nurse have information about where to collect waste information. ")
            pat_bed1 = Item("Patient bed", "This bed belongs to patient #1. ")
            pat_bed2 = Item("Patient bed", "This bed belongs to patient #2. ")
            pat_bed3 = Item("Patient bed", "This bed belongs to patient #3. ")
            pat_bed4 = Item("Patient bed", "This bed belongs to patient #4. ")
            pat_bed5 = Item("Patient bed", "This bed belongs to patient #5. ")

            gen_ward.add_item(pat_bed1)
            gen_ward.add_item(pat_bed2)
            gen_ward.add_item(pat_bed3)
            gen_ward.add_item(pat_bed4)
            gen_ward.add_item(pat_bed5)
            gen_ward.add_item(nurse1)

            gen_ward.add_action("examine")
            gen_ward.get_actions()

            #### NURSE STATION (HALLWAY) ITEMS ###
            comp_station = Item("Computer Station", "This is a computer station comprising of 3 computers. These are used for extracting information and registration. Can only be accessed by the nurses. ")
            files = Item("Filing cabinet", "This is the filing cabinet comprising of different patient files used during treatment by the doctors and nurses. ")

            nurse_station1.add_item(comp_station)
            nurse_station1.add_item(files)

            nurse_station1.add_action("examine")
            nurse_station1.get_actions()

        return hall

    #### Action Functions ####    
    def add_to_inventory(self, item_name):
        # Attempt to add an item to the inventory from the current room
        item = self.current_room.remove_item(item_name)
        if item:
            if item.is_static==True:
                obs = f"{item_name} cannot be collected. "
            elif item.is_static == False:
                self.inventory.append(item)
                obs = f"{item_name} added to inventory. "
        else:
            obs = f"{item_name} not found in the room. "
        return obs

    def put_item(self, item_name, target_name):
        # Use an item from the inventory on a target item in the room
        if item_name in [item.name for item in self.inventory]:
            for item in self.current_room.items:
                if item.name == target_name:
                    target_item = item
            if target_item:
                target_item.add_item(self.remove_from_inventory(item_name))
                self.current_room.add_item(target_item)
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

    #### Game Loop ####
    def start(self, cmd_list=[]):
        current_location = self.current_room.name
        action_space = self.current_room.get_actions()
        obs = "You are in the hallway. This room is called the hallway. This is the main corridor in the ground floor from which we can go to other rooms. The rooms that we can go from here are : doctor chamber #1, doctor chamber #2, general ward, icu ward, common toilet, Nurse Station. The room contains : wall poster, doctor #1, agent."
        for command in cmd_list:
            if command.startswith("go to"):
                room_name = command[len("go to "):]
                self.current_room = self.current_room.connected_room_names[room_name]
                obs = self.current_room.get_details()
            
            elif command.startswith("collect"):
                item_name = command[len("collect "):]
                obs = self.add_to_inventory(item_name) 
                self.current_room.act_space.remove(f"collect {item_name}")
            
            elif command.startswith("put"):
                pattern = r"^put\s+(.*?)\s+on\s+(.*)$"
                match = re.search(pattern, command)
                if match:
                    item_name = match.group(1)  # The first capturing group (item name)
                    target_name = match.group(2)
                obs = self.put_item(item_name, target_name)
            
            elif command.startswith("examine"):
                item_name = command[len("examine "):]
                item = self.current_room.item_names[item_name]
                obs = item.describe()
                if item.contains:
                    for i in item.contains:
                        if i.is_static==False and f"collect {i.name}" not in self.current_room.act_space:
                           self.current_room.act_space.append(f"collect {i.name}")

            elif command == "inventory":
                items = [i.name for i in self.inventory]
                obs = f"Your inventory includes : {','.join(items)}. "
            
            else:
                print("Invalid action.")
            
            current_location = self.current_room.name
            action_space = self.current_room.get_actions()
        
        result = {
            "current_location": current_location,
            "observation": obs,
            "action_space": action_space
        }
        return result

# cmds = ['examine doctor #1', 'inventory', 'go to doctor chamber #1', 'examine dustbin', 'examine patient bed table']
# game = Game()
# res = game.start(cmd_list=cmds)
# print(res)
