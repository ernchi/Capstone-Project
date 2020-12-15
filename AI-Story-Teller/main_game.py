import json
import pickle
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from game import Game
from setting import Setting
from player import Player
from response_handling import *
from ui_map import *
import time
from aitextgen import aitextgen
from item import *


MOVEMENT_INTENT_LIST = ['Go-Left','Go-Right','Go-North','Go-West','Go-East','Go-South','Go-Back','Go-Forward']
ITEM_INTENT_LIST = ['Pick-Up','Use-Object','Look']
CONVERSATION_INTENT_LIST = ['StartConversation']

CALL_WATSON = True

# tkinter methods 
def add_one_message(user_message):
	messages.configure(state='normal')
	messages.insert(INSERT, '%s\n' % user_message)
	messages.configure(state='disabled')
	messages.see("end")

def add_two_messages(user_message, Ai_message):
	messages.configure(state='normal')
	messages.insert(INSERT, '%s\n' % user_message)
	messages.insert(INSERT, '%s\n' % Ai_message)
	messages.configure(state='disabled')
	messages.see("end")


def ai_response(user_input, user_text):
	global CALL_WATSON
	if CALL_WATSON:
		response = assistant.message(
			assistant_id,
			session_id,
			input={
				'message_type': 'text',
				'text': user_input
			}
		).get_result()
		print(json.dumps(response, indent=2))

		# detected intents and entities from watson
		try:
			intent = response['output']['intents'][0]['intent']
		except:
			intent = None

		try:
			entity = (response['output']['entities'][0]['entity'],
			response['output']['entities'][0]['value'])
		except:
			entity = None

		print('intent = ',intent)
		print('entity = ',entity)
		
		# response string from watson 
		try:
			resp = response["output"]["generic"][0]["text"]
		except: 
			resp = "anything-else"
		print(resp)

		if intent in MOVEMENT_INTENT_LIST:
			temp = get_response(intent, player, game)
			# print(resp)
			answer = "<AI> " + temp + '\n'
			add_two_messages(user_text, answer)
			input_user.set('')

			# update map when player enters new room 
			if temp != 'You have reached a dead end' and temp != 'TRY AGAIN':
				if game.cur_location.visited is False:
					# create new room
					update_map(canvas, game.cur_location)
					game.cur_location.set_visited() # mark the room as visited 
				# update player location and direction
				update_player_dir(canvas, player.facing)
				update_player_loc(canvas, 'go-' + player.facing)
			else:
				# change player facing direction 
				update_player_dir(canvas, player.facing)
				move_to_cur_room(canvas)

			# player wins the game when they enter the last room 
			if game.cur_location.id == len(game.gamemap.room_list) - 1: 
				add_one_message('\nCongratulations! You have reached the final room and completed the game.')


		# handle item related intents
		if intent in ITEM_INTENT_LIST:
			try: 
				item = entity[1]
			except:
				item = None
			answer = "<AI> " + handle_items(intent, item, game) + '\n'
			add_two_messages(user_text, answer)
			input_user.set('')
	
	if not CALL_WATSON or intent in CONVERSATION_INTENT_LIST:
		if len(game.cur_location.people) != 0:
			first_call = CALL_WATSON
			CALL_WATSON = False
			model_type = game.cur_location.people[0]
			model_map = {"shakespeare":ai2, "shaw":ai3}
			talk = user_text[6:]
			if first_call:
				input_user.set('')
				add_one_message("\nYou walk over to greet the stranger.\n")
			elif talk.lower() != "goodbye":
				input_user.set('')
				c = ""
				n = 0
				while len(c) == 0 and n < 5:
					conv = model_map[model_type].generate_one(prompt=talk)
					print(conv)
					c = parseConv(conv[len(talk):]) # if "no dialogue found" then call generate again until dialogue found
					n = n+1
				name_tag = "<DRUNK THESPIAN> "
				if model_type is "shaw":
					name_tag = "<DRUNK PHILOSOPHER> "
				add_two_messages("<YOU> " + talk, name_tag + c)
			else:
				input_user.set('')
				add_one_message("<YOU> " + talk)
				CALL_WATSON = True
			

		# if intent == "Use-Object":
		# 	answer = "<AI> You used the "+ item + '\n'
		# 	add_one_message(answer)
		# 	use_item(item)
		# if intent == "Pick-Up":
		# 	answer = "<AI> You picked up the "+ item + '\n'
		# 	add_one_message(answer)
		# 	take_item(item)

def enter_pressed(event):
	input_get = input_field.get()
	print(input_get)
	output_text = "<You> " + input_get
	# add_one_message(output_text)

	input_user.set('')

	
	ai_response(input_get, output_text)
	return "break"

def close(event):
	response = assistant.delete_session(
		assistant_id,
		session_id
	).get_result()
	print(response)


def parseConv(data):
	# with open('shakespeare.txt', 'r') as file:
    data = data.replace('\n', '')

    delimiters = ". ", ".\n"
    segments =re.split(r'[.?!]\s*', data)
    dialogue = ""
    for x in range(0, len(segments)):
        if segments[x].isupper() and len(segments) > 2:
            i = data.find(segments[x + 1]) 
            dialogue += segments[x + 1] + "" + data[i+len(segments[x + 1])] + " "
            if segments[x+2].isupper() is False and len(segments) > 3:
                i = data.find(segments[x + 2])
                dialogue += segments[x + 2] + "" + data[i+len(segments[x + 2])]
                break
            else:
                break

    if dialogue == "":
        print("no dialogue found")
    
    return dialogue

if __name__ == '__main__':
	# tkinter set up
	window = Tk()
	window.resizable(0,0)

	messages = scrolledtext.ScrolledText(window, undo=True, width = 47, height=24, font=("Helvetica", 16), wrap="word")
	messages.pack(expand=True, fill='both')

	input_user = StringVar()
	input_field = Entry(window, text=input_user)
	input_field.pack(side=BOTTOM, fill=X)

	# create label for inventory
	inventory_widget = Label(window, text=("Inventory: ()"))
	inventory_widget.pack(side=BOTTOM, fill=X)

	# create label for health
	healthbar_widget = Label(window, text=("Health: " + str(100)))
	healthbar_widget.pack(side=BOTTOM, fill=X)

	# set up watson assistant
	#Ziwei ibm credential
	api_key = 'MgBfHbCLqSordjG8qU-X8SoBIRmBj2238guZePfZKXw8' # Ziwei
	service_url = 'https://api.us-south.assistant.watson.cloud.ibm.com'
	assistant_id = 'c6a78bfa-6c79-41c4-a716-65176938c27f'


	# api_key = 'cyYZ0cTQb_F_xWaxb7s_OA9kEVItu57f0axkYvvezCaK' # ern chi's
	# service_url = 'https://api.us-south.assistant.watson.cloud.ibm.com'
	# assistant_id = '61ef2103-c32a-4a2d-b03e-d5672238633a'
	version = '2020-04-01'
	authenticator = IAMAuthenticator(api_key) 

	try:
		assistant = AssistantV2(
			version=version,
			authenticator=authenticator
		)
	except Exception:
		print('Error: failed to create new watson assistan')

	assistant.set_service_url(service_url)

	try:
		session = assistant.create_session(
			assistant_id=assistant_id
		).get_result()
	except Exception:
		print('Error: failed to create new session')

	session_id = session["session_id"]

	# create GPT-2 model
	# ai = pickle.load(open("warpeace_model.p","rb"))
	ai = aitextgen()
	ai2 = pickle.load(open("shakespeare_model.p", "rb")) # This is the first character AI used for dialogue
	ai3 = pickle.load(open("shaw_model.p", "rb")) # This is the second character AI used for dialogue
	# create game 
	player = Player('John', 100, 50, inventory_widget, healthbar_widget)
	game = Game(player, 1, 4, ai)
	
	for i in range(game.gamemap.room_num - 1):
		print(game.gamemap.room_list[i].next_room())
	# set up map 
	map_window = open_map_window(window)
	canvas = show_map(map_window, game.gamemap)

	# watson assistant sends first message
	response = assistant.message(
		assistant_id,
		session_id,
		input={
			'message_type': 'text',
			'text': ''
	}
	).get_result()
	output = "<AI> " + response["output"]["generic"][0]["text"] + '\n'
	
	frame = Frame(window)  # , width=300, height=300)

	input_field.bind("<Return>", enter_pressed)
	input_field.bind('<Escape>', close)


	frame.pack()
	add_one_message('Welcome to Amnesiac Story Teller!\n')
	add_one_message('Amnesiac Story teller is a dynamic text-based game that uses Artifical Intelligence to generate content.\n')
	add_one_message('How to Play\n')
	add_one_message('1) You can pick up items, use items, or move around the world by typing what you want to do in the chat box below and clicking the enter button on your keyboard.')
	add_one_message('Example: Move Right.')
	add_one_message('Example: Pick up sword.\n')

	add_one_message('2) Visit all of the rooms to win the game.')
	add_one_message('3) Have fun!\n')

	add_one_message('Game world created!\n')
	add_one_message(output)
	window.mainloop()


"""
print("Test text: ")
text = input()
while text != 'exit': 
	response = assistant.message(
		assistant_id,
		session_id,
		input={
			'message_type': 'text',
			'text': text
		}
	).get_result()
	ai_response = response["output"]["generic"][0]["text"]
	print(ai_response)
	print("Test text: ")
	text = input()

session_delete = assistant.delete_session(
		assistant_id,
		session_id
	).get_result()
"""


"""
print('Welcome. \nEnter your name: ')
#player_name = input()
print('\nSelect a setting: ')
print('1 - Fantasy')
print('2 - Sci-Fi\n')
#setting = input()
#setting = int(setting) # convert str to int 

# initialize game 
print('\nCreating game world... ')
game = Game('Chi', 1, 3)

print('\nPlayer: ', game.player.__dict__)
print('\nSetting: ', game.setting.__dict__)

print('\nCurrent Location: ', game.cur_location.__dict__)

for i in range(game.gamemap.room_num):
	game.gamemap.room_list[i].print()
"""
