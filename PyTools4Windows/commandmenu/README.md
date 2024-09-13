```
pip install pytools4windows.commandmenu
```

Menu interface for building modular command-line toolkits


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

### [#] Memory Menu
Run past commands stored in memory.

## Settings Menu

--------

Opening settings will automatically generate a config file with the `cwd` as the `Working Directory` and 
the `Output Directory`.

```commandline
Settings
[i]- include commands
[x]- exclude commands
[e]- exit

```

### [w] Change Working Directory

Changes the directory that the python script and dependencies are contained in.
*(full path)*
```
('cwd' for current directory)
Working Directory: 
```

Enter `cwd` to assign the current woring directory.

### [d] Change Output Directory

Changes the directory to compile to.  *(full path)*


