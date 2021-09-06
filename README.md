# MonsterDome-Console
A simple monster dueling game

using python 3.8

By Nicholas Zehm 2013-1-8

filename: MonsterDomeConsole.py

#### Version 0.1.5 (2021-5-17)
Changes:
* fixed indentation issue with killMonster()
* cleaned user interface prompts with killMonster()
* removed redudant liveInPen() method from battle.py
* cleaned user interface prompts with selectMonster()

Notes:
* Weird issues may still occur in combat.
* Using python 3.9, some linux machines may use 3.8


#### Version 0.1.4 (2021-3-19) Stable
Changes:
* separated battle.py
* adjusted code to prevent circular referencing - now better suited for gui
* changed main, added interface and mainUserInterface to reduce printing of main_menu
* minor edits and fixes


#### Version 0.1.3.1 (2021-3-17) Experimental
Changes:
* Separated monster.py to minutely simplify code.
* Added stamina to the monster object
* Added level to the monster object
* updated with changes from version 0.1.1.2
* Adjusted the file date to reflect date of earliest prototype of this project (MonsterPenWorks.py)
* switched to international standard date format
* Adjust combat logic to utilize stamina
* Changed save system to save dictionary of objects
* Added a check for redundant names

Fixed:
* post battle healing logic fixed
* minor UI output stuff

## ToDo:
* finish function descriptions throughout code
* multiple pens to save file
* delete pens from save file
* save as?
* use an internal ID system for monsters, instead of name? - allow same redundant names?
* user interaction for attacks/defense
* leveling
* other monster attributes
* start thinking about a UI

Other options
* add partial interface for save/load pen
* Add full interface... (like the unstable tk version)

This version works appears to work- calling it stable
