from game import Game 
from player import Player 
from ui_map import * 

def get_response(text, player, game):
    res = change_player_direction(text, player)
    ans = handle_response(res, game)
    return ans 

# generates AI response based on player intent 
def handle_response(text, game):
    if text == 'go-north': return game.go_north()
    elif text == 'go-south': return game.go_south()
    elif text == 'go-east': return game.go_east()
    elif text == 'go-west': return game.go_west()
    elif text == 'anything-else': return 'TRY AGAIN'

def handle_items(intent,item,game):
    if intent == 'Look':
        if item == 'Room': return game.check_room_item()
        elif game.is_in_room(item) : return game.describeItem(item)
        else : return 'TRY AGAIN'

    elif intent == 'Pick-Up' :
        if item == 'Room': return 'You can not pick up a room. '
        elif item in game.setting.obj_list : return game.pick_up_item(item)
        else : return str(item) + " is not present in this game."

    elif intent == 'Use-Object' :
        if item == 'Room': return "What do you mean? Try again."
        elif item in game.setting.obj_list : return game.use_item(item)
        else : return "You dont even have a " + str(item)

    else : return 'TRY AGAIN, No such intent'

def dummy_response(text, player, game):
    res = change_player_direction(text, player)
    ans = dummy_handle_response(res, game)
    return ans 

def dummy_handle_response(text, game):
    if text == 'go-north': return game.go_north_dummy()
    elif text == 'go-south': return game.go_south_dummy()
    elif text == 'go-east': return game.go_east_dummy()
    elif text == 'go-west': return game.go_west_dummy()
    elif text == 'anything-else': return 'TRY AGAIN'

# def change_player_direction(text, player):
#     if text == 'go-north': player.set_facing_direction('north')
#     elif text == 'go-south': player.set_facing_direction('south')
#     elif text == 'go-east': player.set_facing_direction('east')
#     elif text == 'go-west': player.set_facing_direction('west')
#     elif text == 'go-forward': return 'go-' + player.facing # don't need to change player facing direction 
#     elif text == 'go-back': player.turn_back()
#     elif text == 'go-right': player.turn_right()
#     elif text == 'go-left': player.turn_left()
#     else: return 'anything-else'

#     return 'go-' + player.facing 



def change_player_direction(text, player):
    if text == 'Go-North': player.set_facing_direction('north')
    elif text == 'Go-South': player.set_facing_direction('south')
    elif text == 'Go-East': player.set_facing_direction('east')
    elif text == 'Go-West': player.set_facing_direction('west')
    elif text == 'Go-Forward': return 'go-' + player.facing # don't need to change player facing direction 
    elif text == 'Go-Back': player.turn_back()
    elif text == 'Go-Right': player.turn_right()
    elif text == 'Go-Left': player.turn_left()


    else: return 'anything-else'

    return 'go-' + player.facing   



