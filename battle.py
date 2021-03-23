'''
By Nicholas A Zehm
2021-3-19
Battle logic
filename: battle.py
version 1
for MonsterBattleConsole.py version  0.1.4 (2021-3-19)
'''


# Import Modules
import random # for random numbers
import time # for delay stuff
import math # for log?

from monster import Monster, pen


#  
#  name: liveInPen(name)
#  purpose: 
#  @param
#  @return
#  
def liveInPen(name):
    obj = pen[name]
    if obj.getHealth() <= 0:
        print(name, "had died and was eaten by the others (or just rotted there)!")
        del obj
        del pen[name]
        return False
    else:
        return True


#  
#  name: selectMonster()
#  purpose: Select a monster from the pen list for the battle dome fight, determine fight order
#  @param   pen - list of monsters
#  @return  battle(nameA, nameB) - to begin the fight
#  
def beginFight(combatants):
    name1 = combatants.pop()
    name2 = combatants.pop()
    
    obj1 = pen[name1]
    obj2 = pen[name2]

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


#  
#  name: fight(name1, name2, rest)
#  purpose:
#  @param
#  @return
#  
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


#  
#  name: battle(name1, name2)
#  purpose:
#  @param
#  @return
#  
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


#  
#  name: battleEnd(name1, name2, rest)
#  purpose:
#  @param
#  @return
#  
def battleEnd(names, alive):

    proc = input('') #wait for user at end
    print('Exiting Arena!')

    if alive == 2:
        print(names, 'go to sleep in pen, recover missing stamina\n')
    elif alive == 1:
        print(names, 'goes to sleep in pen, recovers missing stamina\n')


#  
#  name: battleRoll(expA, expB, cond)
#  purpose:
#  @param
#  @return
#  
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


#  
#  name: attackType()
#  purpose:
#  @param
#  @return
#  
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


#  
#  name: defenseType(name1, name2)
#  purpose:
#  @param
#  @return
#  
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
