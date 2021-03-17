'''
By Nicholas A Zehm
3/17/21
Monster class
filename: monster.py
version 1
for MonsterBattle-Console.py version  0.1.3

To simplify code a wee bit, the monster class has been placed here.
'''

# The Monster Object
class Monster:
    '''Initialize the monster'''
    def __init__(self, health, exp):
        self.health = health
        self.exp = exp
        self.maxhealth = health
        self.stamina = 10
        self.maxstamina = 10
        self.level = 0

    #Accessors
    def getHealth(self):
        return self.health

    def getExp(self):
        return self.exp

    def getMaxHealth(self):
        return self.maxhealth
        
    def getStamina(self):
        return self.stamina
    
    def getMaxStamina(self):
        return self.maxstamina
    
    def getLevel(self):
        return self.level

    #Mutators
    def setHealth(self, health):
        self.health = health

    def setExp(self, exp):
        self.exp = exp

    def setMaxHealth(self, health):
        self.maxhealth = health

    def setStamina(self, stamina):
        self.stamina = stamina
    
    def setMaxStamina(self, stamina):
        self.maxstamina = stamina
        
    def setLevel(self, level):
        self.level = level
