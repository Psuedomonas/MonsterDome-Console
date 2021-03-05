#!/usr/bin/python3.8
# Filename: monsterdome-Console.py
'''
By Nicholas A Zehm
3/5/21
A simple monster dueling game
filename: monsterdome-console.py
Version 0.1.1

Todo
* Make damaging insults less common?
* Add stamina
* Implement a new code formalism
    camel case, pascal case, etc
* consider use case: redundant monster names
* try, except relevant user inputs
'''

import random # for random numbers
import time # for delay stuff
import pickle # save data
import math # for log?

debug_mode = True

# Storage File
penStoreFile = 'monsterPenSave.mnst'

# The Monster Pen
pen = {}

# The Monster Object
class Monster:
    '''Initialize the monster'''
    def __init__(self, health, exp):
        self.health = health
        self.exp = exp
        self.maxhealth = health

    #Accessors
    def getHealth(self):
        return self.health

    def getExp(self):
        return self.exp

    def getMaxHealth(self):
        return self.maxhealth

    #Mutators
    def setHealth(self, health):
        self.health = health

    def setExp(self, exp):
        self.exp = exp

    def setMaxHealth(self, health):
        self.maxhealth = health


'''
Feed the monsters - restores health
'''
def feedingTime(corpse):
    if len(pen) > 0:
        # called by a kill from killmonster() or from main() for feeding
        if corpse == True:
            print("its bloody corpse has been eaten by the others.")
        else:
            print("\nIts Feeding time!\n")

        # the feeding
        for monster in pen:
            obj = pen[monster]
            h = obj.getHealth()
            m = obj.getMaxHealth()
            if m > h:
                obj.setHealth(m)
                print("{0} now feed and healed {1} for {2} health\n".format(monster, m-h, m))
            del obj
        # if called from main(), immersive output
        if corpse == False:
            print("All the monsters are feed!\n")
    else:
        print('\nFor reasons of your own, you put food in the empty pen...\n')

    proc = input('')
    if corpse == False:
        return main() #through to main function


'''
Makes a new Monster object
Adds the object to the pen list (should double check which I am using here)
'''
def makeMonster():
    print('\nLets make a monster!')
    name = input('What shall it be named? : ') # get name
    health = 10
    exp = 0
    print('\n{0} has {1} health and {2} experience'.format(name,health,exp))
    toPen = input('Save to pen? (yes/no) : ')
    if toPen == 'yes':
        obj = Monster(health, exp) # make the monster
        pen[name] = obj #store in pen
        del obj
    else:
        print('{0} has been slaughtered\n'.format(name))
    return main()


'''
Makes a custom new monster object
Adds the object to the pen list
'''
def dmMakeMonster():
    print('\nGreetings monster deity\n')
    name = input('What shall the new monster be named? : ')
    max_h = int(input('Enter its maximum health: '))
    exp = int(input('Enter its experience: '))
    health = int(input('Enter its current health: '))
    print('\n{0} has {1} health and {2} experience'.format(name,health,exp))
    toPen = input('Save to pen? (yes/no) : ')
    if toPen == 'yes':
        obj = Monster(health, exp) # make the monster
        pen[name] = obj #store in pen
        if not health == max_h:         #adds the custom health. note: I'm not checking if max is lower than current health
            obj.setHealth(health)
        del obj
    else:
        print('{0} has been slaughtered\n'.format(name))
    return main()


def demo():
    obj = Monster(10, 0)
    pen['bill'] = obj
    obj = Monster(10, 0)
    pen['ted'] = obj
    obj = Monster(10, 10)
    pen['bob'] = obj
    obj = Monster(10, 0)
    obj.setHealth(20)
    pen['fred'] = obj
    print('Some monsters were added to the pen')


'''
checkMonster
Check monsters attributes
input  'name' of monster
proc   check pen for name, get object associated with it
output print, object values
NOTE: This method is not currently being used...
'''
def checkMonster(name):
  if name in pen:
    print('\nPreforming health check of monster...')
    obj = pen[name]
    health = obj.getHealth()
    exp = obj.getExp()
    del obj
    print('\n{0} has {1} health and {2} experience'.format(name, health, exp))
  else:
    print('\nFor mysterious reasons', name, 'does not appear to be in the pen.')


'''
Monster's turn
'''
def fight(name1, name2):
    '''Monsters'''
    obj1 = pen[name1] #Monster 1
    obj2 = pen[name2] #Monster 2
    exp1 = obj1.getExp()
    exp2 = obj2.getExp()

    alive = True #monsters should be alive at this point

    a = attackType() #what type of attack does monster 1 do?
    print('\n{0} {1} {2}...'.format(name1, a, name2))
    success = battleRoll(exp1, exp2, False) # does monster 1's attack succeed?

    if success == True:
        #attack damage
        h = obj2.getHealth()
        h -= 1
        obj2.setHealth(h)
        if h <= 0:
            alive = False
            print(name2,'takes 1 damage and dies!')
        else:
            m = obj2.getMaxHealth()
            print('{0} takes 1 damage, now at {1}/{2} health'.format(name2, h, m))

        #gain experience
        x = obj1.getExp()
        x += 1
        obj1.setExp(x)
    else:
        defenseType(name1, name2)

    return alive


'''
The Monster battle function
Two monsters go in, but only one (should) come out
'''
def battle(name1, name2):
    #Monsters are alive
    alive = True
    keepFighting = True
    turn = 1

    print(name1, ' attacks first!')

    while alive == True and keepFighting == True:
        '''Monster 1's turn'''
        if alive == True and keepFighting == True:
            alive = fight(name1, name2)

        '''Monster 2's turn'''
        if alive == True and keepFighting == True:
            time.sleep(1)
            alive = fight(name2, name1)
            proc = input('End turn {0}'.format(turn))

            turn += 1

            if proc == 'exit':
                keepFighting = False
                print("You flee the arena... with your monsters...")

    '''Clean up after battle'''
    if alive == False:
        obj1 = pen[name1]
        obj2 = pen[name2]

        if obj1.getHealth() <= 0:   # First monster defeated, eaten by second
            heal = obj1.getMaxHealth() % 3

            if obj2.getMaxHealth() <= heal + obj2.getHealth():
                t = obj2.getHealth() + heal
                obj2.setHealth(t)
            else:
                heal = obj2.getMaxHealth() - obj2.getHealth()
                t = obj2.getMaxHealth()
                obj2.setHealth(t)

            print("{0} wins! {0} eats {1}'s bloodied corpse and heals {2} for {3} health".format(name2, name1, heal, t))
            del pen[name1]
        elif obj2.getHealth() <= 0: # Second monster defeated, eaten by first
            heal = obj2.getMaxHealth() % 3

            if obj1.getMaxHealth() <= heal + obj1.getHealth():
                t = obj1.getHealth() + heal
                obj1.setHealth(t)
            else:
                heal = obj1.getMaxHealth() - obj1.getHealth()
                t = obj1.getMaxHealth()
                obj1.setHealth(t)

            print("{0} wins! {0} eats {1}'s bloodied corpse and heals {2} for {3} health".format(name1, name2, heal, t))
            del pen[name2]
        elif obj1.getHealth() <= 0 and obj2.getHealth() <= 0: #This should not happen
            print("Egads! Both {0} and {1} have died! Surely this is a 'feature', not a bug.".format(name1, name2))
            del pen[name1]
            del pen[name2]

        del obj1
        del obj2

    proc = input('') #wait for user at end
    print('Exiting Arena!')
    return main()


'''
Input   2 numbers (real), bool
proc    roll numbers, cond indicates whether a draw should recurse for re-roll
output  bool,
'''
def battleRoll(expA, expB, cond):
    #roll for initiative
    mAroll = random.randint(1, 10) + math.log10(1 + expA)
    mBroll = random.randint(1, 10) + math.log10(1 + expB)

    if mAroll > mBroll:
        return True             #1 is first
    elif mAroll < mBroll:
        return False            #2 is first
    elif cond == True:
        print('Both rolled the same!') #I'm interested to see how often this would happen
        return battleRoll(expA, expB, cond) #recursion until there is a victor
    else:
        return True


'''
Randomly sets the attack type
'''
def attackType():
    attacks = {1 : 'bites', 2 : 'claws', 3 : 'punches', 4 : 'spits at', 5 : 'stabs tail at', 6 :  'insults'}
    adjectives = {1 : 'viciously', 2 : 'ferociously', 3 : 'wildly', 4 : 'mindlessly'}

    attack_r = random.randint(1,6)
    adjective_r = random.randint(1,6) #adjust for length of adjectives dictionary + 2 for 2 chances of no adjective

    if adjective_r > 4: #set to length of adjectives
        attack_string = attacks[attack_r]
    else:
        attack_string = adjectives[adjective_r] + ' ' + attacks[attack_r]

    return attack_string


'''
Prints random defense type
'''
def defenseType(name1, name2):
    r = random.randint(1,3)

    if r == 1:
        print(name1, 'misses')
    elif r == 2:
        defense_adjectives = {1 : 'deftly', 2 : 'nimbly'}
        adjective_r = random.randint(1,4)

        if adjective_r >= 2:
            print(name2, 'dodges')
        else:
            print(name2, defense_adjectives[adjective_r], 'dodges')
    else:
        print('attack fails')




'''
Select a monster from pen list for the battle dome!
Also sets the attack order
'''
def selectMonster():
    if len(pen) < 2:
        print('\nThere is not enough monsters in the pen!')
        print('\nLeaving the Battle Dome...\n')
        return main()

    showPen()

    name1 = input('\nChoose a monster to fight in the battle dome! : ')
    if name1 in pen:
        obj1 = pen[name1]
        if obj1.getHealth() <= 0:
            print(name1, " had died and was eaten by the others (or just rotted there)!")
            del obj1
            return main()
    else:
        print('\n{0} is not in the pen!\n'.format(name1))
        return main()

    name2 = input('Choose the monster to fight {0}!\n'.format(name1))
    if name2 in pen:
        obj2 = pen[name2]
        if obj2.getHealth() <= 0:
            print(name2, " had died and was eaten by the others (or just rotted there)!")
            del obj2
            del obj1
            return main()
    else:
        print('\n{0} is not in the pen!\n'.format(name2))
        return main()
    print('\nEntering the battle pit!')

    #Who gets to attack first, then start the battle
    exp1 = obj1.getExp()
    exp2 = obj2.getExp()

    whosOnFirst = battleRoll(exp1, exp2, True)

    if whosOnFirst == True:
        battle(name1, name2)
    else:
        battle(name2, name1)


'''
kill a monster in the pen
'''
def killMonster():
    if len(pen) == 0:
        print('\nThere is no-one in the pen!')
        print('Leaving the slaughterhouse...\n')
        return main()
    else:
        showPen()
        name = input('\nWhich monster do you want to kill? : ')
        if name in pen:
            obj = pen[name]
            health = obj.getHealth()
            exp = obj.getExp()
            del obj
            kmonst = input('Are you sure you want to kill {0}, who has {1} health and {2} experience? '.format(name, health, exp))
        if kmonst == 'yes':
            del pen[name]
            print('\n{0} has been killed...'.format(name))
            feedingTime(corpse = True)
            showPen()
            print('\n')
        else:
            print('\n{0} is not in the pen!\n'.format(name))
    return main()


'''
Show the monsters in the pen
'''
def showPen():
    for name in pen:
        obj = pen[name]
        health = obj.getHealth()
        maxhealth = obj.getMaxHealth()
        exp = obj.getExp()
        print('Name : {0}  \t Health: {1}/{2} \t Experience: {3}'.format(name, health, maxhealth, exp))
        del obj


'''
save data to disk
'''
def savePen():
    #build list
    stats = {}
    for name in pen:
        obj = pen[name]
        health = obj.getHealth()
        max_h = obj.getMaxHealth()
        exp = obj.getExp()
        stats[name] = {}
        stats[name]['health'] = health
        stats[name]['exp'] = exp
        stats[name]['max_h'] = max_h

    with open(penStoreFile, 'wb') as f:
        pickle.dump(stats, f)

    output = "Pen should be saved to {0}".format(penStoreFile)
    print(output)

    main()


'''
read data from disk
'''
def loadPen():
    with (open(penStoreFile, "rb")) as f:
        newPen = pickle.load(f)
    # rebuild objects from saved nested list

    for name in newPen:
        health = newPen[name]['health']
        exp = newPen[name]['exp']
        max_h = newPen[name]['max_h']
        obj = Monster(max_h,exp)
        obj.setHealth(health)
        pen[name] = obj
        del obj

    showPen()
    main()


'''
The Main Menu function
'''
def main():

    if debug_mode == True:
        demo()
        
        mainMenu = {'check' : "check out the monsters in the pen",
                    'add' : "add a new monster to the pen",
                    'dm' : "add a new monster to the pen in dungeon master mode",
                    'kill' : "kill a monster in the pen",
                    'fight' : "fight monsters in the pen",
                    'feed' : "feed the monsters in the pen, brings them to full health",
                    'save' : "Save the pen",
                    'load' : "Load a pen",
                    'exit' : "Exit the monster dome"}

        for menuOption in mainMenu:
            print("\t",menuOption, "\t:\t", mainMenu[menuOption])
    
        i = input('What would you like to do (type your choice and hit the enter key)? : ')
        if i == 'check':
            print('\nThere are {0} monsters in the pen'.format(len(pen)))
            showPen()
            wait = input('')
            return main()
        elif i == 'add':
            return makeMonster()
        elif i == 'fight':
            return selectMonster()
        elif i == 'kill':
            return killMonster()
        elif i == 'save':
            return savePen()
        elif i == 'load':
            return loadPen()
        elif i == 'dm':
            return dmMakeMonster()
        elif i == 'exit':
            exit()
        elif i == 'feed':
            feedingTime(corpse = False)
        else:
            return main()
    else:
        mainMenu = {'check' : "check out the monsters in the pen",
                    'add' : "add a new monster to the pen",
                    'kill' : "kill a monster in the pen",
                    'fight' : "fight monsters in the pen",
                    'feed' : "feed the monsters in the pen, brings them to full health",
                    'save' : "Save the pen",
                    'load' : "Load a pen",
                    'exit' : "Exit the monster dome"}

        for menuOption in mainMenu:
            print("\t",menuOption, "\t:\t", mainMenu[menuOption])
    
        i = input('What would you like to do (type your choice and hit the enter key)? : ')
        if i == 'check':
            print('\nThere are {0} monsters in the pen'.format(len(pen)))
            showPen()
            wait = input('')
            return main()
        elif i == 'add':
            return makeMonster()
        elif i == 'fight':
            return selectMonster()
        elif i == 'kill':
            return killMonster()
        elif i == 'save':
            return savePen()
        elif i == 'load':
            return loadPen()
        elif i == 'exit':
            exit()
        elif i == 'feed':
            feedingTime(corpse = False)
        else:
            return main()

# Program procedure
print('*** Welcome to the monster battle dome! ***')
main()
print('\nLeaving the battle dome...')
