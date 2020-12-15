from tkinter import *
from room import Room

# coordinates for room and player
room_pos = [0, 0] # x, y coord
player_pos = [0, 0]

# coordinates for player token
arrow_origin_x0 = 120
arrow_origin_y0 = -15
arrow_origin_x1 = arrow_origin_x0
arrow_origin_y1 = -25

arrow_east_x0 = arrow_origin_x0 - 5 # 115
arrow_east_y0 = arrow_origin_y0 - 5 # -20
arrow_east_x1 = 125
arrow_east_y1 = arrow_east_y0

# create new window for map 
def open_map_window(window): 
    map_window = Toplevel(window) 
    map_window.title("Map") 
    map_window.geometry("400x400") 
    Label(map_window,  
          text ="Map").pack() 
    return map_window 

# initialize canvas and starting room in map window 
def show_map(window, game_map):
    canvas = Canvas(window, height=400, width=400)
    start_room = draw_start_room(canvas)
    tag = "room-" + str(game_map.start_room.id)
    canvas.itemconfig(start_room, tags=(tag))
    game_map.start_room.set_visited() # mark the room as visited by player 
    shift_center(canvas, tag)

    # create player token
    draw_start_player(canvas)
    # center it in the start room 
    shift_player(canvas, 'player')
    
    return canvas

def draw_start_room(canvas):
    start_room = canvas.create_rectangle(100, 10, 130, 30,
                outline="black", fill="red", width=2)
    canvas.pack(side=TOP, fill=BOTH, expand=1) 
    return start_room 

def draw_room(canvas):
    cur_room = canvas.create_rectangle(100, 10, 130, 30,
                outline="black", fill="white", width=2)
    canvas.pack(side=TOP, fill=BOTH, expand=1) 
    return cur_room

def draw_start_player(canvas):
    # arrow points north
    player = canvas.create_line(arrow_origin_x0, arrow_origin_y0, arrow_origin_x1, arrow_origin_y1, 
                    arrow=LAST, tags=("player"), fill="blue")
    return player

def shift_center(canvas, tag):
    canvas.move(tag, 80, 80)

def shift_player(canvas, tag):
    canvas.move('player', 75, 120)

def update_map(canvas, cur_loc):
    cur_room = draw_room(canvas)
    tag = "room-" + str(cur_loc.id)
    canvas.itemconfig(cur_room, tags=(tag))
    shift_center(canvas, tag)

    if cur_loc.prev_room() == 'NORTH': room_pos[1] += 20
    if cur_loc.prev_room() == 'SOUTH': room_pos[1] -= 20
    if cur_loc.prev_room() == 'EAST': room_pos[0] -= 30
    if cur_loc.prev_room() == 'WEST': room_pos[0] += 30
    canvas.move(cur_room, room_pos[0], room_pos[1])

# updates player location when they enter a new room
def update_player_loc(canvas, player_move):
    if player_move == 'go-north': player_pos[1] -= 20
    if player_move == 'go-south': player_pos[1] += 20
    if player_move == 'go-east': player_pos[0] += 30
    if player_move == 'go-west': player_pos[0] -= 30
    canvas.move('player', player_pos[0], player_pos[1])
    canvas.tag_raise('player')

# updates the direction the player is facing 
def update_player_dir(canvas, player_dir):
    canvas.delete('player')
    if player_dir == 'north': 
        canvas.create_line(arrow_origin_x0, arrow_origin_y0, arrow_origin_x1, arrow_origin_y1, 
                    arrow=LAST, tags=("player"), fill="blue")
    if player_dir == 'south': 
        canvas.create_line(arrow_origin_x0, arrow_origin_y0, arrow_origin_x1, arrow_origin_y1, 
                    arrow=FIRST, tags=("player"), fill="blue")
    if player_dir == 'east': 
        canvas.create_line(arrow_east_x0, arrow_east_y0, arrow_east_x1, arrow_east_y1, 
                    arrow=LAST, tags=("player"), fill="blue")
    if player_dir == 'west': 
        canvas.create_line(arrow_east_x0, arrow_east_y0, arrow_east_x1, arrow_east_y1, 
                    arrow=FIRST, tags=("player"), fill="blue")
    shift_player(canvas, 'player')
    canvas.tag_raise('player')

# moves the token to the current room player is in 
def move_to_cur_room(canvas):
    canvas.move('player', player_pos[0], player_pos[1])
    canvas.tag_raise('player')
