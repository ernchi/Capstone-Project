"""
Dummy Watson Assistant that takes in very simple player commands 
and returns simple output. For testing purposes. 
"""

from tkinter import *
from game import Game
from setting import Setting
from player import Player
from response_handling import *
from ui_map import *

# tkinter methods 
def ai_response(user_input):
	dummy_resp = dummy_response(user_input, player, game)
	answer = "<AI> " + dummy_resp
	messages.insert(INSERT, '%s\n' % answer)
	input_user.set('')

	# update map when player enters new room 
	if dummy_resp != 'You have reached a dead end' and dummy_resp != 'TRY AGAIN':
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

	if game.cur_location.id == len(game.gamemap.room_list) - 1: 
		win_msg = 'Congratulations! You have reached the final room and completed the game.'
		messages.insert(INSERT, '%s\n' % win_msg)

def enter_pressed(event):
	input_get = input_field.get()
	#print(input_get)
	output_text = "<You> " + input_get
	messages.insert(INSERT, '%s\n' % output_text)

	input_user.set('')

	ai_response(input_get)
	return "break"

window = Tk()

messages = Text(width = 50, height=24, font=("Helvetica", 16))
messages.pack()
input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.pack(side=BOTTOM, fill=X)

# create label for inventory
inventory_widget = Label(window, text=("Inventory: ()"))
inventory_widget.pack(side=BOTTOM, fill=X)

# create label for health
healthbar_widget = Label(window, text=("Health: " + str(100)))
healthbar_widget.pack(side=BOTTOM, fill=X)

# initialize game and player 
player = Player('John', 100, 50, inventory_widget, healthbar_widget)
game = Game(player, 1, 4, None) # ai field leave empty 
messages.insert(INSERT, 'Game world created!\n')

# ui map set up 
map_window = open_map_window(window)
canvas = show_map(map_window, game.gamemap)

# print out path to next room 
for i in range(game.gamemap.room_num - 1):
	print(game.gamemap.room_list[i].next_room())

output = "<AI> Welcome"
messages.insert(INSERT, '%s\n' % output)

frame = Frame(window)  # , width=300, height=300)
input_field.bind("<Return>", enter_pressed)
frame.pack()
window.mainloop()