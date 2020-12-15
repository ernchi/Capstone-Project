import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Setting up Watson Assistant 
authenticator = IAMAuthenticator('ygyXFo1z5e4GfX4EOXXWphgLxmEPk1bVvHV4SxwP65vW') # api key
assistant = AssistantV2(
    version='2020-09-17',
    authenticator=authenticator
)
assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com/instances/d56b83b2-43bb-4756-908e-8c770e24a90c')
assistant_id='b589568b-fbaf-4488-9d47-1913119493ab'

response = assistant.create_session(
    assistant_id=assistant_id
).get_result()
session_id = response["session_id"]

# Import classes
from monster import Monster
from player import Player

# Create new player
player = Player('John', 100, 'Magic', 50) 
print(player.__dict__)

# Create new monster
monster = Monster('Goblin', 100, 20, 'It is green and ugly.')

# Response maps
response_map = {'Go':'Preset movement response', 'pick-up':'Pick up object response'}
actions = {'Go' : 'You move through the empty room and open the door.'}

# Generate story 
print("You stand in an empty room. There is a door. There is a key in the corner of the room.")
text = input()

response = assistant.message(
    assistant_id,
    session_id,
    input={
        'message_type': 'text',
        'text': text
    }
).get_result()
print(json.dumps(response, indent=2))

answer = response["output"]["generic"][0]["text"]
#print(actions[answer])

# Player picks up an item
if answer == 'pick-up':
    print('successfully picked up item')
    player.add_inventory('key')
    print(player.__dict__)
else:
    print('did not pick up')

# Monster attacks player 
print('A monster jumped out and attack you.')
if monster.attack(player) <= 0:
    print('Game over.')
else: 
    print(player.__dict__)

# Delete session
response = assistant.delete_session(
    assistant_id,
    session_id
).get_result()


# Intents: Looking around (describe environment), Interact with object (picking up, putting down/activating/using), attacking
# For picking up actions think of an inventory system that keeps track of what you have picked up so far.
# Maybe add entities to Watson and only allow users to progress through the story by interacting with them.


# Questions:
# How do we do settings?
# We wanted the system to figure out the wording details: maybe have our NLP-model automatically upload intents to Watson to generate the wording. Want ways to have same meaning but with new flavor.
# For the first timebox: Have simple structure by filling up conversation nodes.


# Things to Do:
#   Add intents
#   Figure out which NLP-model to use
#   Figure out how to integrate an NLP-model (set up an adapter pattern)
#   Create a story
#       - Set up the "mad-libs" thing

#   Add a user interface?

#   Don't do masking objects as 'OBJECT'  for the upcoming demo -- we can control the input for this one.
