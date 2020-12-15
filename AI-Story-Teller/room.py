import random
import item

class Room:
    def __init__(self, room_id, setting):
        self.id = room_id # int
        #self.objects = []
        # connecting rooms 
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.setting = setting
        self.room_name, self.room_description = self.set_room()
        self.items = self.set_items()
        self.monster = None
        self.visited = False # set to True if player has visited the room 
        self.described = False
        self.description = ""
        self.people = []

        #fill the obj list
        self.item_objs = {}
        self.set_item_objs()

    def set_north(self, room):
        self.north = room

    def set_south(self, room):
        self.south = room
    
    def set_east(self, room):
        self.east = room

    def set_west(self, room):
        self.west = room

    def get_id(self):
        return self.id

    def get_linked_room(self, direction):
        if direction == 1: return self.north
        elif direction == 2: return self.south
        elif direction == 3: return self.east
        elif direction == 4: return self.west    

    def print(self):
        print('Room id: ', self.id)
        if self.north is not None: print('North: ', self.north.id)
        else: print('North: ')

        if self.south is not None: print('South: ', self.south.id)
        else: print('South: ')
        
        if self.east is not None: print('East: ', self.east.id)
        else: print('East: ')
        
        if self.west is not None: print('West: ', self.west.id)
        else: print('West: ')

    # returns the direction of the next room
    def next_room(self):
        if self.north is not None:
            if self.north.id > self.id:
                return 'NORTH'
        if self.south is not None:
            if self.south.id > self.id:
                return 'SOUTH'
        if self.east is not None:
            if self.east.id > self.id:
                return 'EAST'
        if self.west is not None:
            if self.west.id > self.id:
                return 'WEST'

    def set_room(self):
        key = random.choice(list(self.setting.rooms))

        obj = {}
        obj[key] = self.setting.rooms[key]
        return key, self.setting.rooms[key]
    
    def set_items(self):
        random_number = random.randint(1, 3)
        items = []

        settings_list = self.setting.items

        new_list = random.sample(settings_list, len(settings_list))  
        for i in range(random_number):
            new_item = new_list.pop()
            items.append(new_item)
            
        return items

    def set_item_objs(self):
        for i in self.items:
            self.item_objs[i] = item.Item(i,self.setting.obj_des[i],i)


    # mark the room as already visited by player 
    def set_visited(self):
        self.visited = True

    # returns the direction of the previous room 
    def prev_room(self):
        if self.north is not None:
            if self.north.id < self.id:
                return 'NORTH'
        if self.south is not None:
            if self.south.id < self.id:
                return 'SOUTH'
        if self.east is not None:
            if self.east.id < self.id:
                return 'EAST'
        if self.west is not None:
            if self.west.id < self.id:
                return 'WEST'


    def addPerson(self, person):
        self.people.append(person)
        



