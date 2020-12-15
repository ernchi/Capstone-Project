from room import Room 

class Player:
    def __init__(self, name, health, resource_points, inventory_widget,healthbar_widget ):
        self.name = name
        self.health = health
        self.resource_points = resource_points 
        self.inventory = []
        self.item_objs = {}
        self.inventory_widget = inventory_widget
        self.healthbar_widget = healthbar_widget
        self.facing = 'north' # player starts the game by facing north 


    #check if a player has certain items
    def has_item(self, item):
        return item in self.inventory

    # returns 0 if player attempts to add item that is not present in the room
    # returns 1 otherwise 
    def add_inventory(self, item, room):
        # check if item is an object in the room 
        if item in room.items: 
            self.inventory.append(item)
            self.item_objs[item] = room.item_objs[item]
            room.items.remove(item)
            room.item_objs.pop(item)
            return 1
        else: return 0

    # returns 0 if player attempts to remove item not in their inventory
    # returns 1 otherwise 
    def remove_inventory(self, item, room):
        # check if item is in inventory
        if item in self.inventory:
            self.inventory.remove(item)
            the_item = self.item_objs.pop(item)
            room.items.append(item)
            room.item_objs[item] = the_item
            return 1
        else: return 0
    
    def attack(self, monster, weapon):
        monster.health -= weapon.damage

    def use_resource(self):
        self.resource_points -= 5
    
    def reduce_health(self, amount):
        self.health -= amount
        self.healthbar_widget.configure(text=("Health: " + str(self.health)))

    def change_inventory_widget(self):
        self.inventory_widget.configure(text=("Inventory: (" + str( ','.join(self.inventory)) + ')'))

    # change the direction the player is facing 
    def turn_right(self):
        if self.facing == 'north': self.facing = 'east'
        elif self.facing == 'south': self.facing = 'west'
        elif self.facing == 'east': self.facing = 'south'
        elif self.facing == 'west': self.facing = 'north'
    
    def turn_left(self):
        if self.facing == 'north': self.facing = 'west'
        elif self.facing == 'south': self.facing = 'east'
        elif self.facing == 'east': self.facing = 'north'
        elif self.facing == 'west': self.facing = 'south'

    def turn_back(self): 
        if self.facing == 'north': self.facing = 'south'
        elif self.facing == 'south': self.facing = 'north'
        elif self.facing == 'east': self.facing = 'west'
        elif self.facing == 'west': self.facing = 'east'

    def set_facing_direction(self, new_dir):
        self.facing = new_dir

        

