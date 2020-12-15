from player import Player
from setting import Setting
from gamemap import GameMap
from item import Item
import random
import re



# initializes player, setting, game map 
class Game:
	def __init__(self, player, setting, room_num, ai):
		self.player = player
		self.setting = Setting(setting)
		#self.room_num = random.randint(3, 5) # randomly sets number of rooms in game map 
		self.gamemap = GameMap(room_num, self.setting)
		# self.itemmap = Item_Map(self,room_num)
		self.cur_location = self.gamemap.start_room
		self.ai = ai
		

	def pick_up_item(self,item):
		if self.player.add_inventory(item,self.cur_location) == 1:
			self.player.change_inventory_widget()
			return 'You pick up the ' + item
		else:
			return "There is no such item in current room."

	def use_item(self,item):
		if self.player.has_item(item):
			self.player.remove_inventory(item,self.cur_location) 
			self.player.change_inventory_widget()
			return "You used " + str(item)
		else:
			return "You dont have the" + str(item) +", try pick it up first."





	def check_room_item(self):
		return 'There are a ' + ' and a '.join(self.cur_location.items)

	def is_in_room(self,item):
		return (item in self.cur_location.items)

	def describeItem(self,item):
		item_obj = self.cur_location.item_objs[item]
		# return item_obj.d
		if item_obj.is_descibed:
			return item_obj.AI_des
		else:
			
			prompt = item + item_obj.d + " Describe the object: "
			temp = self.ai.generate_one(prompt=prompt)
			txt = temp.replace(prompt, "")
			delimiters = ". ", ".\n"
			segments = split(delimiters, txt)
		
			sentences = [item_obj.d]
			for s in segments:
				s = s.replace("\n", " ")
				s = s.replace("\r", " ")
				sentences.append(s)
		
			description = sentences[0] + " "
			if len(sentences) > 3:
				description = description + sentences[1] + ". " + sentences[2] + ". " + sentences[3] + ". "

			item_obj.add_AI_des(description)
			return description


	def return_description(self, items_list):
		if (self.cur_location.described == False):
			self.cur_location.described = True
			self.cur_location.description = self.describeRoom('You are now in the ' + str(self.cur_location.room_name) + '. ' + self.cur_location.room_description) + "There is a " + items_list + " in the room."
			if len(self.cur_location.people) != 0:
				self.cur_location.description = self.cur_location.description + " There is a person in the room."
		return self.cur_location.description
			
	def go_north(self):
		if self.cur_location.north is not None:
			self.cur_location = self.cur_location.north
			items_list = self.separate_list(self.cur_location.items)
			description = self.return_description(items_list)
			return description
		else: return 'You have reached a dead end'

	def go_south(self):
		if self.cur_location.south is not None:
			self.cur_location = self.cur_location.south
			items_list = self.separate_list(self.cur_location.items)
			description = self.return_description(items_list)
			return description
		else: return 'You have reached a dead end'

	def go_east(self):
		if self.cur_location.east is not None:
			self.cur_location = self.cur_location.east
			items_list = self.separate_list(self.cur_location.items)
			description = self.return_description(items_list)
			return description
		else: return 'You have reached a dead end'

	def go_west(self):
		if self.cur_location.west is not None:
			self.cur_location = self.cur_location.west
			items_list = self.separate_list(self.cur_location.items)
			description = self.return_description(items_list)
			return description
		else: return 'You have reached a dead end'
	
	def separate_list(self, items_list):
		items = ''
		if len(items_list) == 1:
			return items_list[0].upper()
		new_list = [x.upper() for x in items_list]
		return '{} and {}'.format(', '.join(new_list[:-1]), new_list[-1])

	def describeRoom(self, room_tag):
		prompt = room_tag + " Describe the room: "
		temp = self.ai.generate_one(prompt=prompt)
		txt = temp.replace(prompt, "")
		delimiters = ". ", ".\n"
		segments = split(delimiters, txt)
		
		sentences = [room_tag]
		for s in segments:
			s = s.replace("\n", " ")
			s = s.replace("\r", " ")
			sentences.append(s)
		
		description = sentences[0] + " "
		if len(sentences) > 3:
			description = description + sentences[1] + ". " + sentences[2] + ". " + sentences[3] + ". "
		return description

	"""
	For testing without aitextgen 
	"""
	def go_north_dummy(self):
		if self.cur_location.north is not None:
			self.cur_location = self.cur_location.north
			return 'You are now in room ' + str(self.cur_location.id)
		else: return 'You have reached a dead end'

	def go_south_dummy(self):
		if self.cur_location.south is not None:
			self.cur_location = self.cur_location.south
			return 'You are now in room ' + str(self.cur_location.id)
		else: return 'You have reached a dead end'

	def go_east_dummy(self):
		if self.cur_location.east is not None:
			self.cur_location = self.cur_location.east
			return 'You are now in room ' + str(self.cur_location.id)
		else: return 'You have reached a dead end'
	
	def go_west_dummy(self):
		if self.cur_location.west is not None:
			self.cur_location = self.cur_location.west
			return 'You are now in room ' + str(self.cur_location.id)
		else: return 'You have reached a dead end'


def split(delimiters, string, maxsplit=0):
	regexPattern = '|'.join(map(re.escape, delimiters))
	return re.split(regexPattern, string, maxsplit)
	
