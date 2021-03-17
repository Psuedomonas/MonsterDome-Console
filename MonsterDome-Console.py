#!/usr/bin/python3.8
# Filename: MonsterDome-Console.py

'''
By Nicholas A Zehm
3/5/21
A simple monster dueling game

filename: MonsterDome-Console.py
Version 0.1.3.1 (2021/3/17)

Todo
* consider use case: redundant monster names
* try, except relevant user inputs
'''

# Import Modules
import random # for random numbers
import time # for delay stuff
import pickle # save data
import math # for log?

# Import files
from monster import Monster

# Storage File
penStoreFile = 'monsterPenSave.mnst'

# The Monster Pen
pen = {}

##### Pen Methods #####

'''
Adds some monsters to the pen for testing
'''
def demo():
    obj = Monster(20, 10, 0 , 0) #(max_health, max_stamina, experience, level)
    obj.setHealth(10)
    pen['bill'] = obj

    obj = Monster(10, 10, 0, 0)
    pen['ted'] = obj

    obj = Monster(10, 10, 10, 0)
    pen['bob'] = obj

    obj = Monster(10, 10, 0, 0)
    obj.setHealth(20)
    pen['fred'] = obj

    obj = Monster(1,1,1,1)
    pen['Zanz'] = obj

    del obj
    print('Some monsters were added to the pen')


'''
Makes a new Monster object
Adds the object to the pen list
'''
def makeMonster():
    print('\nLets make a monster!')
    name = input('What shall it be named?: ') # get name
    health = 10
    stamina = 10
    exp = 0
    lvl = 0
    print('\n{0} is level {1}, has {2} health, {3} stamina, and {4} experience'.format(name, lvl, health, stamina, exp))
    toPen = input('Save to pen? (yes/no) : ')
    if toPen == 'yes':
        obj = Monster(health, stamina, exp, lvl) # make the monster
        try:
            pen[name] = obj #store in pen
        except:
            print(name, 'fled! [Something went wrong with storing the object list]')
            if name in pen:
                print('Probably a name collision error')
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
    if max_h <= 0:
        print('Monster immediately died!')
        return main()

    health = int(input('Enter its current health: '))
    if health <= 0:
        print('Monster immediately died!')
        return main()

    exp = int(input('Enter its experience: '))
    if exp < 0:
        exp = 0

    max_s = int(input('Enter its maximum stamina: '))
    if max_s < 0:
        max_s = 0

    stamina = int(input('Enter its current stamina: '))
    '''if stamina < 0: # I may not use this check
        stamina = 0'''

    lvl = int(input('Enter its level (start = 0): '))
    if lvl < 0:
        lvl = 0

    print('\n{0} is level {1}, has {2}/{3} health, {4}/{5} stamina, and {6} experience'.format(name, lvl, health, max_h, stamina, max_s,exp))
    toPen = input('Save to pen? (yes/no): ')
    if toPen == 'yes':
        obj = Monster(max_h, max_s, exp, lvl)

        if not health == max_h:
            obj.setHealth(health)

        if not stamina == max_s:
            obj.setStamina(stamina)

        pen[name] = obj #store in pen
        del obj #its in the pen, don't need it elsewhere
    else:
        print('{0} has been slaughtered\n'.format(name))
    return main()


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
save data to disk
'''
def savePen():
    #build list
    stats = {}
    for name in pen:
        obj = pen[name]
        stats.update({name : obj})

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
        pen[name] = newPen[name]

    showPen()
    main()


##### Pen and Combat Methods #####

'''
checkMonster
Check monsters attributes
input  'name' of monster
proc   check pen for name, get object associated with it
output print, object values

Now being used by showPen()
'''
def checkMonster(name):
    if name in pen:
        #print('\nPreforming health check of monster...') #I'm not using this to parse the pen yet
        obj = pen[name]
        lvl = obj.getLevel()

        health = obj.getHealth()
        max_h = obj.getMaxHealth()

        stamina = obj.getStamina()
        max_s = obj.getMaxStamina()

        exp = obj.getExp()

        del obj
        print('{0}:\tLevel: {1}\tHealth: {2}/{3}\tStamina: {4}/{5}\t Experience: {6}'.format(name, lvl, health, max_h, stamina, max_s,exp))
    else:
        print('For mysterious reasons', name, 'does not appear to be in the pen.')


'''
Show the monsters in the pen
'''
def showPen():
    for name in pen:
        checkMonster(name)


def liveInPen(name):
    obj = pen[name]
    if obj.getHealth() <= 0:
        print(name, "had died and was eaten by the others (or just rotted there)!")
        del obj
        del pen[name]
        return False
    else:
        return True


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
            print("All the monsters are fed!\n")
    else:
        print('\nFor reasons of your own, you put food in the empty pen...\n')

    proc = input('')
    if corpse == False:
        return main() #through to main function

##### Battle Functions #####

'''
Select a monster from pen list for the battle dome!

input:
    user input, 'name' of a 'monster' object from 'pen' list
proc:
    checks that enough monsters are in 'pen',
    user input 'name' is in pen,
    monster is alive with liveInPen(),
    sets combat order with whosOnFirst()
output:
    main() or battle()
'''
def selectMonster():
    if len(pen) < 2:
        print('\nThere is not enough monsters in the pen!')
        print('\nLeaving the Battle Dome...\n')
        return main()

    showPen()

    name1 = input('\nChoose a monster to fight in the battle dome! : ')
    if name1 in pen:
        if liveInPen(name1) == False: #is monster still alive?
            return main()
        else:
            obj1 = pen[name1]
    else:
        print('\n{0} is not in the pen!\n'.format(name1))
        return main()

    name2 = input('Choose the monster to fight {0}!\n'.format(name1))
    if name2 in pen:
        if liveInPen(name2) == False:
            del obj1 #clear the previous monster
            return main()
        else:
            obj2 = pen[name2]
    else:
        print('\n{0} is not in the pen!\n'.format(name2))
        return main()
    print('\nEntering the battle pit!')

    #Who gets to attack first, then start the battle
    exp1 = obj1.getExp()
    exp2 = obj2.getExp()

    #Don't need these in memory anymore
    del obj1
    del obj2

    whosOnFirst = battleRoll(exp1, exp2, True)

    if whosOnFirst == True:
        return battle(name1, name2)
    else:
        return battle(name2, name1)


'''
Monster's turn
'''
def fight(name1, name2, rest):
    '''Monsters'''
    obj1 = pen[name1] #Monster 1
    obj2 = pen[name2] #Monster 2
    exp1 = obj1.getExp()
    exp2 = obj2.getExp()

    alive = 2 #monsters should be alive at this point

    a = attackType() #what type of attack does monster 1 do?
    print('\n{0} {1} {2}...'.format(name1, a, name2))

    if rest == True:    #Is the opponent sleeping?
        success = True
    else:
        success = battleRoll(exp1, exp2, False) # does monster 1's attack succeed?

    time.sleep(0.5) #provide delay between attack and result...

    if success == True:
        #attack damage
        h = obj2.getHealth()
        h -= 1
        obj2.setHealth(h)
        if h <= 0:
            alive = 1
            print(name2,'takes 1 damage and dies!')
        else:
            m = obj2.getMaxHealth()
            print('{0} takes 1 damage'.format(name2))

        #gain experience
        x = obj1.getExp()
        x += 1
        obj1.setExp(x)
    else:
        defenseType(name1, name2)

    return alive


'''
The Monster battle function
Two monsters go in, but (possibly) only one will leave
'''
def battle(name1, name2):
    alive = 2 #Monsters are alive
    keepFighting = True # The fight is still on
    turn = 1    #Track the turn number
    needs_rest1 = False #is monster 1 sleepy
    needs_rest2 = False #is monster 2 sleepy

    survivor_name = ''

    obj1 = pen[name1]
    obj2 = pen[name2]

    print(name1, 'attacks first!')

    while alive == 2 and keepFighting == True:
        '''Monster 1's turn'''
        stam1 = obj1.getStamina()
        stam2 = obj2.getStamina()

        if stam2 <= 0: # is opponent awake?
            needs_rest2 = True

        if stam1 > 0: # is monster 1 awake
            needs_rest1 = False
            alive = fight(name1, name2, needs_rest2)
            stam1 -= 1
            obj1.setStamina(stam1)
        else: # Monster 1 sleeps and gets some stamina back
            needs_rest1 = True
            stam1 += 2
            obj1.setStamina(stam1)
            print(name1, 'rests for a bit')

        '''Monster 2's turn'''
        if alive == 2: #Both monsters are still alive
            time.sleep(1)

            if stam1 <= 0:
                needs_rest1 = True

            if stam2 > 0:
                needs_rest2 = False
                alive = fight(name2, name1, needs_rest1)
                stam2 -= 1
                obj2.setStamina(stam2)
            else:
                needs_rest2 = True
                stam2 += 2
                obj2.setStamina(stam2)
                print(name2, 'rests for a bit')

        '''End of turn'''
        if alive == 2:
            h = obj1.getHealth()
            hm = obj1.getMaxHealth()
            sm = obj1.getMaxStamina()
            s = obj1.getStamina()
            x = obj1.getExp()
            print('\n{5} at {0}/{1} health, {2}/{3} stamina, {4} experience'.format(h, hm, s, sm, x, name1))

            h = obj2.getHealth()
            hm = obj2.getMaxHealth()
            sm = obj2.getMaxStamina()
            s = obj2.getStamina()
            x = obj2.getExp()
            print('{5} at {0}/{1} health, {2}/{3} stamina, {4} experience'.format(h, hm, s, sm, x, name2))

            proc = input('****\t End turn {0}\t ****: '.format(turn))
            turn += 1

            if proc == 'exit': # a chance to end the fight, if only the user knew this existed...
                keepFighting = False
                print("You flee the arena... with your monsters...")


    '''Clean up after battle'''
    if alive == 1:
        t = 0
        heal = 0
        if obj1.getHealth() <= 0:   # First monster defeated, eaten by second
            survivor_name = name2

            if obj2.getMaxHealth() > obj2.getHealth(): # for now, we allow for greater than max health, but not for healing
                heal = obj1.getMaxHealth() // 3
                print(heal)

                if obj2.getMaxHealth() >= (heal + obj2.getHealth()):
                    t = obj2.getHealth() + heal
                    obj2.setHealth(t)
                else:
                    heal = obj2.getMaxHealth() - obj2.getHealth()
                    t = obj2.getMaxHealth()
                    obj2.setHealth(t)
            else:
                heal = 0
                t = obj2.getMaxHealth()

            max_s = obj2.getMaxStamina() # The monster sleeps in pen, UI tells user monster is resting in pen later
            obj2.setStamina(max_s)

            print("{0} wins! {0} eats {1}'s bloodied corpse and heals {2} for {3} health".format(name2, name1, heal, t))
            del pen[name1]

        elif obj2.getHealth() <= 0: # Second monster defeated, eaten by first
            survivor_name = name1

            if obj1.getMaxHealth() > obj1.getHealth(): # for now, we allow for greater than max health, but not for healing
                heal = obj2.getMaxHealth() // 3
                print(heal)
                if obj1.getMaxHealth() >= (heal + obj1.getHealth()):
                    t = obj1.getHealth() + heal
                    obj1.setHealth(t)
                else:
                    heal = obj1.getMaxHealth() - obj1.getHealth()
                    t = obj1.getMaxHealth()
                    obj1.setHealth(t)
            else:
                heal = 0
                t = obj2.getMaxHealth()

            max_s = obj1.getMaxStamina() # The monster sleeps in pen, UI tells user monster is resting in pen later
            obj1.setStamina(max_s)

            print("{0} wins! {0} eats {1}'s bloodied corpse and heals {2} for {3} health".format(name1, name2, heal, t))
            del pen[name2]

        elif obj1.getHealth() <= 0 and obj2.getHealth() <= 0: #This should not happen
            print("Egads! Both {0} and {1} have died! Surely this is a 'feature', not a bug.".format(name1, name2))
            alive = 0
            del pen[name1]
            del pen[name2]

    else:
        survivor_name = name1 + ' and ' + name2

        max_s = obj1.getMaxStamina() # The monster sleeps in pen, UI tells user monster is resting in pen later
        obj1.setStamina(max_s)

        max_s = obj2.getMaxStamina() # The monster sleeps in pen, UI tells user monster is resting in pen later
        obj2.setStamina(max_s)

    del obj1
    del obj2
    return battleEnd(survivor_name, alive)


'''
end of the battle sequence, ui back to main()
'''
def battleEnd(names, alive):

    proc = input('') #wait for user at end
    print('Exiting Arena!')

    if alive == 2:
        print(names, 'go to sleep in pen, recover missing stamina\n')
    elif alive == 1:
        print(names, 'goes to sleep in pen, recovers missing stamina\n')
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

    attack_r = random.randint(1,26) #randomly choose attack type

    if attack_r == 1: #bites
        att = attacks[6]
    elif attack_r == (2 or 6): #claws
        att = attacks[1]
    elif attack_r == (6 or 11): #punches
        att = attacks[2]
    elif attack_r == (11 or 16): #spits at
        att = attacks[3]
    elif attack_r == (16 or 21): #stabs tail at
        att = attacks[4]
    else:                       # words can hurt too
        att = attacks[5]

    adjective_r = random.randint(1,6) #adjust for length of adjectives dictionary + 2 for 2 chances of no adjective

    if adjective_r > 4: #set to length of adjectives
        attack_string = att
    else:
        attack_string = adjectives[adjective_r] + ' ' + att

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



#####   The Main Function   #####
'''
The Main Menu function
'''
def main():
    mainMenu = {'check' : "check out the monsters in the pen",
                    'add' : "add a new monster to the pen",
                    'dm' : "add a new monster to the pen in dungeon master mode", # debug code
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
        return selectMonster() #leads towards the actual battle
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


# Program procedure
print('*** Welcome to the monster battle dome! ***')
demo() # debug code
main()
print('\nLeaving the battle dome...')
