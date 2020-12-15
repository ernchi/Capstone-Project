# generates the objects and monsters based on setting
class Setting:

    # setting is an int where 
    # 1 - fantasy setting
    # 2 - sci-fi setting
    def __init__(self, setting):
        self.setting = setting
        self.obj_list = self.set_obj()
        self.obj_des = self.set_obj_des()
        self.monster_list = self.set_monster()
        self.resource = self.set_resource()
        self.rooms = self.set_rooms()
        self.items = self.set_obj()


    def set_obj(self):
        if self.setting == 1: return ['Wand', 'Potion',  "Key", "Skeleton", "Gold", "Sword", "Armour", 'Bowl', "Apple"]
        elif self.setting == 2: return ['robot part']

    def set_obj_des(self):
        if self.setting == 1: return {
            'Wand' : ' a wooden stick wizzard used to cast magic',
            'Potion' : ' a glass bottle with red liquid in',
            'Key' : ' a silver jey with complicated signet on it',
            'Skeleton' : ' skeleton from a giant monster that you don recognize',
            'Gold' : ' Shining piece of gold',
            'Sword' : ' Covered with dry blood and dirt and spider webs',
            'Bowl': ' Useless bowl for food',
            'Apple' : ' Help you stay healthy and away from doctors and monsters',
            'Armour' : ' Covered with blood and heavily damaged iron armour'
        } 
        elif self.setting == 2: return {'robot part':'some mechanical and elctronic parts looks like they are from a droid'}

    def set_monster(self):
        if self.setting == 1: return ['goblin', 'dragon', 'gnome']
        elif self.setting == 2: return ['evil robot', 'sentient chainsaw']

    def set_resource(self):
        if self.setting == 1: return 'Magic'
        elif self.setting == 2: return 'Mech skill'

    def set_rooms(self):
        if self.setting == 1: 
            return {
            "Dungeon": "An underground room intented for holding prisoners.",
            "Great Hall": "The main meeting and dining area.",
            "The Throne Room": "A large room with steps leading to the throne.",
            "Kitchen" :  "A room used to cook food."
            }
        elif self.setting == 2:
            return {
            "Bridge":  "A room where the captain and officers give commands",
            "Engine Room": "A room where the engine is located",
            "Galley" :  "A room where the food is prepared.",
            "Cabin" : "A room where people live in."
            
        }







