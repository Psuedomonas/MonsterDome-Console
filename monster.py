'''
By Nicholas Zehm
2021-3-17
Monster class
filename: monster.py
for MonsterBattle-Console.py version  0.1.3.1 (2021-3-19)
version 1.1 (2021-3-19)

Notes:
The advantage, as far as I can see, for wrapping variables in methods is protecting client input
Otherwise, with some code changes, I could simply use a dictionary. This would use a lot less code, no idea
how it would effect execution time.
'''

pen = {}


class Monster:
    '''Initialize the monster'''
    def __init__(self, health, stamina, exp, lvl):
        self.health = health
        self.exp = exp
        self.maxhealth = health
        self.stamina = stamina
        self.maxstamina = stamina
        self.level = lvl

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
        if health < 0: 
            health = 0
        self.health = health

    def setExp(self, exp):
        if exp < 0:
            exp = 0
        self.exp = exp

    def setMaxHealth(self, health):
        if health < 0:
            health = 0
        self.maxhealth = health

    def setStamina(self, stamina):
        self.stamina = stamina
    
    def setMaxStamina(self, stamina):
        if stamina < 0:
            stamina = 0
        self.maxstamina = stamina
        
    def setLevel(self, level):
        if level < 0:
            level = 0
        self.level = level
