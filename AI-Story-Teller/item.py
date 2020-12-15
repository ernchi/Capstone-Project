# ITEM_TYPE = 
# {
#     'key':'KEY'
#     'K
# }
import random
import setting

# ITEM_LIST = ['key', 'map', 'potion']

class Item:
	def __init__(self, name, description,obj_type):
		self.name = name
		self.is_descibed = False
		self.d = description
		self.obj_type = obj_type
		self.AI_des = None

	def add_AI_des(self,des_text):
		if self.AI_des == None:
			self.AI_des = des_text
			self.is_descibed = True
		else:
			print("Room already has an Ai generated describiton")

	def use_item(self,game):
		pass





#self.items { room_num : item }?????
#

# class Item_map:
# 	def __init__(self,game,room_num,item_dic = None):
# 		self.game = game
# 		self.room_num = room_num
# 		self.items = {}

# 	#add random item in each room
# 		for i in range(room_num):
# 			i_name = random.choice(ITEM_LIST)
# 			description = "An item"
# 			self.items[i] = Item(i_name,description,i_name)
			
# 	#for adding specific item in specific room
# 	def add_item(self, room_num,item_name):
# 		# add item description 
# 		description = "An item"
# 		an_Item = Item(item_name,description,item_name)
# 		self.items[room_num] = an_Item


# def use_item(item):
# 	pass

# def take_item(item):
# 	pass