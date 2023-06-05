'''
By Nicholas Zehm
2021-3-17
Monster class
filename: monster.py
for MonsterBattle-Console-exp/MonsterBattleDome.py 
version  0.2.0 (2022-10-25)
'''

#Monsters in the pen
pen = {}

#Monsters in the combat areana
to_arena = []

class Monster:
    '''Initialize the monster'''
    def __init__(self, health, stamina, exp, lvl, attack_skill, defense_skill):
        self.health = health
        self.exp = exp
        self.maxhealth = health
        self.stamina = stamina
        self.maxstamina = stamina
        self.attack_skill = attack_skill
        self.defense_skill = defense_skill
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
        
    def getAttackSkill(self):
        return self.attack_skill

    def getDefenseSkill(self):
        return self.defense_skill

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
        
    def setAttackSkill(self, attack_skill):
        if attack_skill < 0:
            attack_skill = 0
        self.attack_skill = attack_skill
        
    def setDefenseSkill(self, defense_skill):
        if defense_skill < 0:
            defense_skill = 0
        self.defense_skill = defense_skill

    def setLevel(self, level):
        if level < 0:
            level = 0
        self.level = level
