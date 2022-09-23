#!/usr/bin/python3.8
# Filename: MonsterDomeConsole.py

'''
By Nicholas Zehm
2021-3-5
A simple monster dueling game
filename: MonsterDomeConsole.py
Version 0.1.6.1 (2022-3-19)
'''

# Activate Debug mode (so many neat features...)
debug_mode = True

# Import Modules
import pickle # save data

# Import files
from monster import Monster, pen
from battle import *

# Storage File
penStoreFile = 'monsterPenSave.mnst'

# configures main menu
if debug_mode == True:
    main_menu = {'show' : "check out the monsters in the pen",
                'add' : "add a new monster to the pen",
                'dm' : "add a new monster to the pen in dungeon master mode", # debug code
                'kill' : "kill a monster in the pen",
                'fight' : "fight monsters in the pen",
                'feed' : "feed the monsters in the pen, brings them to full health",
                'save' : "Save the pen",
                'load' : "Load a pen",
                'exit' : "Exit the monster dome"}
else:
    main_menu = {'show' : "check out the monsters in the pen",
                'add' : "add a new monster to the pen",
                'kill' : "kill a monster in the pen",
                'fight' : "fight monsters in the pen",
                'feed' : "feed the monsters in the pen, brings them to full health",
                'save' : "Save the pen",
                'load' : "Load a pen",
                'exit' : "Exit the monster dome"}


'''
##### Pen Methods #####
'''
#
#  name: demo
#  purpose: place some monsters in the pen at start
#  @param   none
#  @return  none
#
def demo():
    obj = Monster(20, 10, 0 , 0) #(max_health, max_stamina, experience, level)
    obj.setHealth(10)
    pen['dragon'] = obj

    obj = Monster(10, 10, 0, 0)
    pen['beast'] = obj

    obj = Monster(10, 10, 10, 0)
    pen['chimera'] = obj

    obj = Monster(10, 10, 0, 0)
    obj.setHealth(20)
    pen['george'] = obj

    obj = Monster(1,1,1,1)
    pen['scarecrow'] = obj

    del obj
    print('Some monsters were added to the pen')


#
#  name: makeMonster
#  purpose: add a user created monster to the pen
#  @param   none
#  @return  tail call back to interface
#
def makeMonster():
    print('\nLets make a monster!')
    name = input('What shall it be named?: ') # get name
    if name in pen:
        print(name, 'is already in pen!')
        return main()
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

    return interface() #bring back the menu interface


#
#  name: dmMakeMonster
#  purpose: add a customized monster to the pen, for testing
#  @param   none
#  @return  tail call back to interface
#
def dmMakeMonster():
    print('\nGreetings monster deity\n')
    name = input('What shall the new monster be named? : ')

    max_h = int(input('Enter its maximum health: '))
    if max_h <= 0:
        print('Monster immediately died!')
        return interface()

    health = int(input('Enter its current health: '))
    if health <= 0:
        print('Monster immediately died!')
        return interface()

    exp = int(input('Enter its experience: '))

    max_s = int(input('Enter its maximum stamina: '))

    stamina = int(input('Enter its current stamina: '))

    lvl = int(input('Enter its level (start = 0): '))

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

    return interface()


#
#  name: killMonster
#  purpose: User cam remove/terminate a monster in the pen
#  @param   None
#  @return  tail call back to interface
#
def killMonster():
    showPen()
    name = input('\nWhich monster do you want to kill? : ')
    if name in pen:
        obj = pen[name]
        health = obj.getHealth()
        exp = obj.getExp()
        del obj
        kmonst = input('Are you sure you want to kill {0}, who has {1} health and {2} experience? (yes/no): '.format(name, health, exp))
        if kmonst == 'yes':
            del pen[name]
            print('\n{0} has been killed...'.format(name))
            do_with_corpse = input("Do you want to 'feed' the corpse to the monsters (heals them) or 'incinerate' it? : ")
            if do_with_corpse == 'incinerate':
                feedingTime(killcall = True, feeding = False)
            else:
                feedingTime(killcall = True, feeding = True)
            showPen()
            print('\n')
    else:
        print('\n{0} is not in the pen!\n'.format(name))

    return interface()


#
#  name: savePen
#  purpose: save pen to file
#  @param   none
#  @return  tail call back to interface
#
def savePen():
    #build list
    stats = {}
    for name in pen:
        obj = pen[name]
        stats.update({name : obj})

    with open(penStoreFile, 'wb') as f:
        pickle.dump(stats, f)

    output = "Pen saved '{0}'".format(penStoreFile)
    print('\n', output,'\n')

    return interface()


#
#  name: loadPen
#  purpose: Load pen from file
#  @param   none
#  @return  tail call back to interface
#
def loadPen():
    with (open(penStoreFile, "rb")) as f:
        newPen = pickle.load(f)
    # rebuild objects from saved nested list

    for name in newPen:
        pen[name] = newPen[name]

    showPen()
    return interface()


'''
##### Pen and Combat Methods #####
'''
#
#  name: checkMonster
#  purpose:
#  @param
#  @return
#
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


#
#  name: showPen
#  purpose:
#  @param
#  @return
#
def showPen():
    for name in pen:
        checkMonster(name)


#
#  name: feedingTime
#  purpose:
#  @param   corpse = Boolean
#  @return  tail call back to interface
#
def feedingTime(killcall, feeding):
    if feeding == True:
        # called by a kill from killmonster() or from mainUserInterface() for feeding
        if killcall == True:
            #called by killmonster()
            print("its bloody corpse has been eaten by the others.")
        else:
            #from feed monsters in mainUserInterface
            print("\nIts Feeding time!\n")

        # the feeding
        for monster in pen:
            obj = pen[monster]
            h = obj.getHealth()
            m = obj.getMaxHealth()
            if m > h:
                obj.setHealth(m)
                print("{0} now fed and healed {1} for {2} health\n".format(monster, m-h, m))
            del obj
        # if called from main(), immersive output
    else:
        print("The corpse was incinerated!\n")

    proc = input('')
    if killcall == False:
        return interface() #throw interface()


#
#  name: liveInPen
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
#  name: selectMonster
#  purpose:
#  @param
#  @return  tail call back to interface
#
def selectMonster():
    name1 = input('\nChoose a monster to fight in the battle dome! : ')
    if name1 in pen:
        if liveInPen(name1) == False: #is monster still alive?
            return interface()
    else:
        print('\n{0} is not in the pen!\n'.format(name1))
        return interface()

    name2 = input('Choose the monster to fight {0}! : '.format(name1))
    if name2 in pen:
        if liveInPen(name2) == False:
            del obj1 #clear the previous monster
            return interface()
    else:
        print('\n{0} is not in the pen!\n'.format(name2))
        return interface()
    print('\nEntering the battle pit!')

    combatants = {name1, name2}
    beginFight(combatants)
    return interface()


'''
#####   The Main Function   #####
'''
#
#  name: main
#  purpose:
#  @param
#  @return
#
def main():
    if debug_mode == True:
        demo()

    print('*** Welcome to the monster battle dome! ***')

    return interface()   #tail call (I believe that's what it's called)


#
#  name: mainUserInput
#  purpose:
#  @param
#  @return
#
def mainUserInput():
    i = input('What would you like to do (type your choice and hit the enter key)? : ')

    if i == 'show':
        print('\nThere are {0} monsters in the pen'.format(len(pen))) #FIXME?
        showPen()
        wait = input('')
        return interface()

    elif i == 'add':
        return makeMonster()

    elif i == 'fight':
        #Check before calling, don't want to edit pen when I don't need to, even with self
        if len(pen) < 2:
            print('\nThere is not enough monsters in the pen!')
            print('\nLeaving the Battle Dome...\n')
            return mainUserInput()
        else:
            showPen()
            #setPen(pen)
            return selectMonster() #leads towards the actual battle

    elif i == 'kill':

        if len(pen) == 0:
            print('\nThere is no-one in the pen!')
            print('Leaving the slaughterhouse...\n')
            return mainUserInput()
        else:
            return killMonster()

    elif i == 'save':
        '''
        # commented this out because right now I'm ok with blanking the save file
        if len() == 0:
            print('\nThere is no-one in the pen!')
            return mainUserInput()
        else:
            return savePen()
        '''
        return savePen()

    elif i == 'load':
        return loadPen()

    elif i == 'dm' and debug_mode == True:
        return dmMakeMonster()

    elif i == 'exit':
        exit()

    elif i == 'feed':

        if len(pen) > 0:
            return feedingTime(killcall = False, feeding = True)
        else:
            print('\nFor reasons of your own, you put food in the empty pen...\n')
            return mainUserInput()

    else:
        return mainUserInput() # We are assuming the user won't put an obscene amount of bad input


#
#  name: interface
#  purpose:
#  @param
#  @return
#
def interface():
    for menu_option in main_menu:
        print("\t",menu_option, "\t:\t", main_menu[menu_option])
    mainUserInput()


# Program procedure
main()
