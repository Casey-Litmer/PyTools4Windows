# CommandMenu

```
pip install pytools4windows.commandmenu
```

Menu interface for building modular command-line toolkits.  Converts json datastructures into nested menus that append 
subcommands together to run in terminal. 
This allows for much faster navigation of commonly used
terminal commands in your development environment.

***Command Struct Tutorial*** \
https://github.com/Casey-Litmer/PyTools4Windows/blob/main/PyTools4Windows/commandmenu/Command%20Struct%20Tutorial.md


## Main Menu

-------


```commandline
Commands
[$]- Settings
[#]- Memory
[g]- git
[p]- pip
[t]- twine
[e]- exit
```

### [$] Settings menu
Change which commands to display and the number of commands to store in memory.
### [#] Memory Menu
Run past commands stored in memory.
### [x] Command Menus
Run a command starting from its base subcommand.

## Settings Menu

--------

```commandline
Settings
[i]- Include Commands
[x]- Exclude Commands
[m]- Change Memory Length
[e]- exit
```

### [i] Include Commands 

Choose which available command struct jsons to display on the main menu.  
```
Include:
[0]- git
[1]- pip
[2]- python
[3]- twine
[e]- exit
```

### [x] Exclude Commands

Choose which available command struct jsons to exclude from the main menu.  


### [m] Change Memory Length

Change the length of the maximum number of past commands to memorize.  Leave blank to keep the same.

*(default: 6)*

```commandline
Memory Length:  6
New Length: 
```


## Memory Menu

---------

Shows all past commands run by the user up to `memory length`.  

```
Memory
[0]- twine check dist/*
[1]- pip list
[2]- git status
[3]- git branch
[e]- exit
```

## Command Menus

------------

Each selection will open a new menu with all listed sub commands and string them together until
* a full command is reached
* user input is required

!!! *TODO: allow for sequential user inputs and validity checks!* !!!

For example, for the `git` command:

```commandline
git

Choose Action
[i]- init
[s]- status
[a]- add
[r]- remote
[t]- tag
[b]- branch
[k]- checkout
[h]- push
[l]- pull
[c]- commit -m
[m]- rm --cached
[e]- exit
h
```

```commandline
git push

Choose Action
[x]- (push current branch)
[o]- origin
[u]- -u origin (set upstream)
[e]- exit
o
```

```commandline
git push origin

Choose Action
[x]- (push branch)
[v]- v
[e]- exit
x
```

```commandline
git push origin
{branch} main
```

Each partial subcommand sequence is displayed above the next action as if then user was typing it themselves.


## Local Mode

------

All settings will be saved in a config file next to commandmenu.py or commandmenu.exe by default
```commandline
#Run script
python commandmenu.py local

#Run exe
commandmenu.exe local
```
Run `commandmenu` with argument `local` to initialize a new config file in the current working directory. \
***All settings and memory will be relative to this run location.***
