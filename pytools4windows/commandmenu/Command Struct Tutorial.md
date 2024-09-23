## Command Structs

commandmenu uses json files to construct recursive menus that piece together subcommands.

The json files are stored in the `jsons` folder parallel to the script making it easy to add menus 
for new commands.

```commandline
commandmenu/
    commandmenu.exe
    jsons/
        git.json
        twine.json
        ...
```

This short tutorial will help you to create your own toolkits for commonly used commands!


------
## Basic Format


Each dictionary *key* is composed of 
- a menu **key** in [brackets] *
- a **subcommand**

**A key can be any string or character except for `e` which is reserved for the menu `exit` key*

Each dictionary *item* can either be 
- an empty list `[]`
- a string `"{request}"`
- or another dictionary `{"[x]key":item}`


For example:

```commandline
'command.json'
                         
{
"[c]command": {                   #command
    "[a]subcmd1": [],             #command subcmd1                 >> run 
    "[b]subcmd2": "{request}",    #command subcmd2 {user input}    >> run
    "[c]subcmd3": {               #command subcmd3           
        "[x]subcmd4": [],         #command subcmd3 subcmd4         >> run
        "[y]subcmd5":{            #command subcmd3 subcmd5 ...
            etc...
        }
    }
}
```

***The first item in the struct must have the same name as the json file and contain a dictionary of all subcommands.***

### Dict Item Behaviour

Upon pressing a menu **key**, the script will add append the **subcommand** to its current string and do one of three
things based on the *item* type: 

- `[]` will run the current string in terminal 
 

- `{request}` will prompt the user for an input (such as a file path) and display "{request}" 


- `{"[x]key":item}` will open a nested menu with more subcommands


The script will append together all sequential nested menu **subcommand** selections until it prompts the user
for input or runs the command as it is.

Note:
*this is subject to change in a future update to introduce the ability for sequential user input*

Within each dictionary, the menu **keys** should be unique within that layer but may be repeated in other dictionaries. 
Again, be sure that none of the **keys** are `e` as this will be overwritten by the default exit.

-----
## Comments

Wrapping a substring with `#` allows you to include specific display instructions without changing
the compilers interpretation of the **subcommand**.


For example:
```commandline
{
    "[x]command #(installs more RAM)#": ...
}
```
will display in the menu as
```
[x]- command (installs more RAM)
```
but only `"command"` will be appended to the string that gets run.

This is helpful for commenting empty subcommands that exist only to run the command 
as it is currently constructed.


### Multiple Subcommands

After the compiler removes all comments from the **subcommand** all spaces will split into separate
subcommands allowing the user to group a sequence of subcommands into one menu item.

```commandline
{
    "[x]command subcmd #comment#": ...
}
```
will evaluate as
```commandline
> command subcommand
```

-----
## Git Struct Example



https://github.com/Casey-Litmer/PyTools4Windows/blob/main/PyTools4Windows/commandmenu/jsons/git.json