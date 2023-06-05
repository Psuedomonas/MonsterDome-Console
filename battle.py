'''
By Nicholas Zehm
2021-3-19
Battle logic
filename: battle.py
for MonsterBattle-Console-exp/MonsterBattleDome.py
version  0.2.2 (2023-01-18)
'''

# Import Modules
import random # for random numbers
import time # for delay stuff
import math # for log?


# Import the project
from monster import *


'''Dictionaries for the battle'''
turn_order = []
potential_targets = []
not_alive = []


'''The battle sequence'''
def battle():
    turn = 1
    still_fighting = True
  
    try:
        while still_fighting:
            #Start Turn 'turn'
            print('**** \t Start turn', turn, '\t ****')

            #build turn order
            turn_order = rollForTurnOrder()
    
            for name in turn_order:
                # Name is awake and is alive
                if isAwake(name) and isAlive(name):
                    print(name, "'s turn")
                    
                    potential_targets = to_arena.copy()
                    potential_targets.remove(name)
                    
                    if name in potential_targets:
                        print('logic error!')
                        break
                    
                    if len(potential_targets) > 1:
                        target = list(potential_targets)[-1]
                    else:
                        target = rollForTarget(potential_targets)

                    fight(name, target)
                    
                    proc = input("next...")
                    
                #Name is alive but not awake
                elif isAlive(name):
                    sleep_type = sleepAdjectives()
                    obj = pen[name]
                    stamina = obj.getStamina()
                    stamina = stamina + 3
                    obj.setStamina(stamina)
                    print(name, sleep_type, ' to regain 3 stamina')
                    
                #Name is dead
                else:
                    #Check if less than two are alive
                    if len(to_arena) < 2:
                        still_fighting = False
                        return battleEnd()
                #Check if less than two are alive
                if len(to_arena) < 2:
                    still_fighting = False
                    return battleEnd()
            
            proc = input('****\t End turn {0}\t ****: '.format(turn))
            turn += 1

    except KeyboardInterrupt:
        print("You flee the arena... with your monsters...")
        
    return battleEnd()


''' the action sequence '''
#
#  name: fight(name1, name2)
#  purpose:
#  @param
#  @return
#
def fight(name1, name2):
    #Attacker
    obj1 = pen[name1]
    exp1 = obj1.getExp()
    s1 = obj1.getStamina()
    a_s1 = obj1.getAttackSkill()
    m_s1 = obj1.getMaxStamina()

    #Defender
    obj2 = pen[name2]
    exp2 = obj2.getExp()
    h2 = obj2.getHealth()
    s2 = obj2.getStamina()
    d_s2 = obj2.getDefenseSkill()
    m_h2 = obj2.getMaxHealth()
    m_s2 = obj2.getMaxStamina()

    a = attackType() #what type of attack does monster 1 do?
    print('\n{0} {1} {2}...'.format(name1, a, name2))
    
    s1 = s1 - 3
    obj1.setStamina(s1)

    print('\t{0} stamina = {1}/{2}'.format(name1, s1, m_s1))

    time.sleep(0.5) #provide delay between attack and result...

    #attack 'roll'
    roll_attack = random.randint(1, 20) + math.log2(1 + a_s1)
    #print('attack roll =',roll_attack)
    
    #Target defense
    if isAwake(name2): # Target us awake
        
        #defense 'roll'
        roll_defense = random.randint(1, 20) + math.log2(1 + d_s2)
        #print('defense roll =',roll_defense)
        
        if roll_attack < 5:   # Attacker Missed
            #attack experience gain
            exp1 = exp1 + 1
            obj1.setExp(exp1)
            #target experience gain
            exp2 = exp2 + 1
            obj2.setExp(exp2)

            fails(name1)

            print('\t', name1, ' experience = ', exp1, ', ', name2, 'experience = ', exp2)

        elif roll_attack >= roll_defense:   # Attack Success
            #damage calculation
            damage = random.randint(0, 3) + math.log2(1 + a_s1)

            #target stamina loss
            s2 = s2 - 1
            obj2.setStamina(s2)

            #target experience gain
            exp2 = exp2 + 1
            obj2.setExp(exp2)

            print('attack hits!')

            #target health loss
            h2 = h2 - damage
            if h2 < 0:
                h2 = 0
                print(name2,'takes {0} damage and dies!'.format(damage))
                
                exp1 = exp1 + 2
            else:
                print('\t{0} takes {1} damage, health = {2}/{3}, stamina = {4}/{5}'.format(name2, damage, h2, m_h2, s2, m_s2))
           
            obj2.setHealth(h2)
            isAlive(name2)
            
            #attacker experience gain
            exp1 = exp1 + 2
            obj1.setExp(exp1)
            print('\t{0} stamina = {1} / {2}'.format(name1, s2, m_s2))
            print('\t', name1, 'experience = ', exp1, ', ', name2, 'experience = ', exp2)

        else:   # Defense Success
            defenseType(name1, name2)

            #attacker experience gain
            exp1 = exp1 + 1
            obj1.setExp(exp1)

            #defender stamina loss
            s2 = s2 - 1
            obj2.setStamina(s2)

            #defender stamina gain
            exp2 = exp2 + 2
            obj2.setExp(exp2)

    else:   # Attacker gets better chance for an attack
        if roll_attack < 5:   # Missed
            #attacker experience gain
            exp1 = exp1 + 1
            obj1.setExp(exp1)
            
            fails(name1)

            print('\t', name1, 'experience = ', exp1, ', ', name2, 'experience = ', exp2)

        else:   # Attack Success
            print('attack hits!')
            
            damage = random.randint(0,5) + math.log2(1 + a_s1)

            #defender health loss
            h2 = h2 - damage
            if h2 < 0:
                h2 = 0
                print(name2,'takes {0} damage and dies!'.format(damage))
                isAlive(name2)
            else:
                print('\t{0} takes {1} damage, health = {2}/{3}, stamina = {4}/{5}'.format(name2, damage, h2, m_h2, s2, m_s2))
            obj2.setHealth(h2)

            #attacker experience gain
            exp1 = exp1 + 2
            obj1.setExp(exp1)
            print('\t{0} stamina = {1} / {2}'.format(name1, s1, m_s1))
            print('\t',name1, 'experience = ', exp1, ', ', name2, 'experience = ', exp2)


#
#
#
#
#
#
def fails(name):
    failed = [" missed!", "'s attack failed!", " biffed!", " totally missed the mark!", " completely failed the attack!"]

    r = random.randint(0,4)

    print(name, failed[r])


#
#
#
#
#
#
def battleEnd():
    for name in to_arena:
       print(name)
       
    print('Has won the battle!')
    
    #reset stamina
    for name in to_arena:
        print(name, 'sleeps in pen')
        obj = pen[name]
        max_stamina = obj.getMaxStamina()
        obj.setStamina(max_stamina)
    
    if not len(not_alive) == 0:
        proc = input('Do you wish to resurrect the dead monster(s)? (y/n): ')
        if proc == 'y':
            print('Very well')
            for name in not_alive:
                print(name, 'resurrected to 1 health')
                obj = pen[name]
                obj.setHealth(1)
    
    to_arena.clear()
    
    print('Exiting Arena!\n')
    #return interface()


#
#
#
#
#
def rollForTurnOrder():
    battle_order = {}
    for name in to_arena:
        obj = pen[name]
        level = obj.getLevel()
        the_roll = random.randint(1, 20) + math.log(1 + level)
        battle_order[name] = the_roll

    battle_order = dict(sorted(battle_order.items(), key=lambda item: item[1], reverse = True))
    
    return battle_order


#
#
#
#
#
def rollForTarget(potential_targets):
    battle_order = {}
    
    for name in potential_targets:
        obj = pen[name]
        level = obj.getLevel()
        the_roll = random.randint(1, 20) + math.log(1 + level)
        battle_order[name] = the_roll

        battle_order = dict(sorted(battle_order.items(), key=lambda item: item[1],reverse = True))
        
        return list(battle_order)[-1]
        
                
#
#  name: attackType()
#  purpose:
#  @param
#  @return
#
def attackType():
    attacks = ['bites', 'claws', 'punches', 'spits at', 'stabs tail at', 'insults']
    adjectives = ['viciously', 'ferociously', 'wildly', 'mindlessly']

    attack_r = random.randint(1,26) #randomly choose attack type

    if  1 <= attack_r <= 5: # bites
        att = attacks[0]
    elif 6 <= attack_r <= 10: # claws
        att = attacks[1]
    elif 11 <= attack_r <= 15: # punches
        att = attacks[2]
    elif 16 <= attack_r <= 20: # spits at
        att = attacks[3]
    elif 21 <= attack_r <= 25: # stabs tail at
        att = attacks[4]
    elif attack_r == 26: # words can hurt too
        att = attacks[5]

    adjective_r = random.randint(0,6) #adjust for length of adjectives list + 3 chances of no adjective

    if adjective_r > 3: #set to length of adjectives
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
    def_adjectives = ['deftly', 'nimbly', 'skillfully', 'adeptly']
    def_verbs = ['blocks', 'dodges', 'evades', 'defends']

    verb_r = random.randint(0,3)
    verb = def_verbs[verb_r]

    adj_r = random.randint(0,6)
    if adj_r > 3:
        # no adjective
        print(name2, verb, '!')
    else:
        print(name2, def_adjectives[adj_r], verb, "!")


#
#
#
#
#
''' And now, some functions'''
'''Check of monster is alive'''
def isAlive(name):
    obj = pen[name]
    if obj.getHealth() <= 0:
        if name in to_arena:
            to_arena.remove(name)
        if name not in not_alive:
            not_alive.append(name)

        return False
    else:
        return True


#
#
#
#
#
'''Check if monster is awake'''
def isAwake(name):
    obj = pen[name]
    if obj.getStamina() <= 0:
        return False
    else:
        return True


#
#
#
#
#
def sleepAdjectives():
    sleep_words = ['sleeps', 'rests', 'naps', 'dozes', 'snoozes', 'slumbers']
    adjectives = ['peacefully', 'serenely ', 'fretfully', 'soundly']

    r = random.randint(0,5)

    adj_r = random.randint(0,6)

    if adj_r > 3:
        sleep_string = sleep_words[r]
    else:
        sleep_string = sleep_words[r] + " " + adjectives[adj_r]

    return sleep_string
