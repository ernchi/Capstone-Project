from room import Room
import random

class GameMap:
    def __init__(self, room_num,setting):
        self.room_num = room_num # number of rooms in map
        self.room_list = []
        self.setting = setting

        # create and store rooms
        for i in range(self.room_num):
            new_room = Room(i, setting)
            self.room_list.append(new_room)
            del setting.rooms[new_room.room_name]
        
        room_monster = random.randint(1, len(self.room_list) - 1)
        # 
        new_monster_list = random.sample(self.setting.monster_list, len(self.setting.monster_list)) 
        self.room_list[room_monster].monster = new_monster_list[0]

        self.room_list[1].addPerson("shakespeare")
        self.room_list[2].addPerson("shaw")
		
        # room that player starts the game in 
        self.start_room = self.room_list[0]
        self.gen_link()

    # generate the links between the rooms 
    def gen_link(self):
        for i in range(self.room_num - 1):
            self.link_room(self.room_list[i], self.room_list[i + 1]) 

    # randomly links one room to another
    def link_room(self, room1, room2):
        # randomly choose a direction the room will be connected to 
        direction = random.randint(1, 4)
        # ensure not already connected to another room
        while(room1.get_linked_room(direction) is not None):
            direction = random.randint(1, 4)
        if direction == 1:
            room1.set_north(room2)
            room2.set_south(room1)
        elif direction == 2:
            room1.set_south(room2)
            room2.set_north(room1)
        elif direction == 3:
            room1.set_east(room2)
            room2.set_west(room1)
        elif direction == 4:
            room1.set_west(room2)
            room2.set_east(room1)
            
        
