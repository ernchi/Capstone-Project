class Monster:
    def __init__(self, name, health, damage, description):
        self.name = name
        self.health = health
        self.damage = damage
        self.description = description

    def describe(self):
        print("The monster is a {}. {}.".format(self.name, self.description))

    def attack(self, player):
        player.health -= self.damage
        return player.health


        
        
        