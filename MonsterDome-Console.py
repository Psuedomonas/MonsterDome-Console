#!/usr/bin/python3.4
# Filename: MonsterPenWorks008.py
''' 
By Nicholas A Zehm
filename: myClassMonster.py
08-Jan-2013
An attempt at making a monster dueling game
5/11/15
Version 0.0.9
fix logic errors in battle/fight - Never hits!!!

TODO
error catching
streamline UI
load/save file not tested
'''

import random # for random numbers
import time # for delay stuff
import pickle # save data
import math # for log

# Storage File
penStoreFile = 'MonsterPen.monsterpy'

# The Monster Pen
pen = {}

# The Monster Object
class Monster:
  '''Initialize the monster'''
  def __init__(self, health, exp):
    self.health = health
    self.exp = exp
    self.totalHealth = health

  #Accesors
  def getHealth(self):
    return self.health

  def getExp(self):
    return self.exp
		
  def getTotalHealth(self):
    return self.totalhealth
	
  #Mutators
  def setHealth(self, health):
    self.health = health
	
  def setExp(self, exp):
    self.exp = exp

'''Makes a new Monster object'''
def makeMonster():
  print('\nLets make a monster!')
  name = input('What shall it be named? : ') # get name
  health = random.randint(1,20) # make monster health
  exp = 0
  print('\n{0} has {1} health and {2} experience'.format(name,health,exp))
  toPen = input('Save to pen? (yes/no) : ')
  if toPen == 'yes':
    obj = Monster(health, exp) # make the monster
    pen[name] = obj #store in pen
    del obj
  else:
    print('{0} has been slaughtered'.format(name))
  return main()

'''
checkMonster
Check monsters attributes
input  'name' of monster
proc   check pen for name, get object associated with it
output print, object values
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
    print('\nFor mysterious reasons ', name, ' does not appear to be in the pen.')

		
def fight(nameA, nameB):
  #Get Object Data
  objA = pen[nameA]
  expA = objA.getExp()
  objB = pen[nameB]
  hB = objB.getHealth()
  expB = objB.getExp()
	

  del objA
  del objB
  return True

	
'''The battle'''
def battle(name1, name2):
  #Monsters are alive
  alive = True
  obj1 = pen[name1] #Monster 1
  obj2 = pen[name2] #Monster 2
  #Simulation loop
  while alive == True:
    #get experience
    exp1 = obj1.getExp()
    exp2 = obj2.getExp()


  del obj1
  del obj2
  proc = input('')
  print('Exiting Arena!')
  return main()


                
'''Select a monster from pen array'''
'''chooses a monster for the battle pit'''
def selectMonster():
  if len(pen) < 2:
    print('\nThere is not enough monsters in the pen!')
    print('\nLeaving the Battle Dome...\n')
    return main()
  else:
    showPen()
    name1 = input('Choose a monster to fight in the battle dome!\n')
    if name1 in pen:
      obj = pen[name1]
      if obj.getHealth() <= 0:
        print('\nMonster is a deceased deficated mass!')
        print('\nLeaving the Battle Dome...\n')
        del obj
        return main()
    else:
      print('\n{0} is not in the pen!\n'.format(name1))
      return main()

    name2 = input('Choose the monster to fight {0}!\n'.format(name1))
    if name2 in pen:
      obj = pen[name2]
      if obj.getHealth() <= 0:
        print('\nMonster is a deceased deficated mass!')
        print('\nLeaving the Battle Dome...\n')
        del obj
        return main()
    else:
      print('\n{0} is not in the pen!\n'.format(name2))
      return main()
    print('\nEntering the battle pit!')
    return battle(name1, name2)

'''kills a monster in the pen'''
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
        print('\n{0} has been killed... Its bloody corpse was eaten by the others.\n'.format(name))
        showPen()
    else:
      print('\n{0} is not in the pen!\n'.format(name))
  return main()


def showPen():
  for name in pen:
    obj = pen[name]
    health = obj.getHealth()
    exp = obj.getExp()
    print('Name : {0}  \t Health: {1} \t Experience: {2}'.format(name, health, exp))
    del obj
  
# save data to disk
def savToFile():
  f = open(SavFilName, 'wb')


# read data from disk
def getFromFile():
  f = open(SaveFilName, 'rb')

def main():
  '''The Main Menu function'''
  print('You can : \n\t"check"\tout the monsters in the pen.\n\t"add"\ta new monster to the pen.\n\t"kill"\ta monster from the pen.')
  print('\t"fight" monsters in the pen.\n\t"save"\tthe pen\n\t"load"\tPen from file\n\t"exit"\tthe dome.')

  i = input('What would you like to do? : ')
  if i == 'c' or i == 'check':
    print('\nThere are {0} monsters in the pen'.format(len(pen)))
    showPen()
    wait = input('')
    return main()
  elif i == 'a' or i == 'add':
    return makeMonster()
  elif i == 'f' or i == 'fight':
    return selectMonster()
  elif i == 'k' or i == 'kill':
    return killMonster()
  elif i == 's' or i == 'save':
    return savePen()
  elif i == 'l' or i == 'load':
    return loadPen()

# Program procedure
print('*** Welcome to the monster battle dome! ***')
main()
print('\nLeaving the battle dome...')
