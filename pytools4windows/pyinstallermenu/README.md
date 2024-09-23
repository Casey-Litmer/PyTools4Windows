# PyInstallerMenu
```
pip install pytools4windows.pyinstallermenu
```

Menu interface for pyinstaller with custom dependency copying.

-------
## Main Menu

```commandline
PyInstaller
[b]- Batch a Script
[s]- Settings
[w]- Open Working Directory
[d]- Open Output Directory
[e]- exit
```

### [b] Batch menu
Batch a python script to exe
### [s] Settings Menu
Chnage and view the `Working Directory` and `Output Directory`
### [w] Open Working Directory
Open the saved `Working Directory` in explorer
### [d] Open Output Directory
Open the saved `Output Directory` in explorer

-------
## Batch Menu

```commandline
Batch
[b]- Batch
[d]- Batch with dependencies
[e]- exit
```

### [b] Batch


Asks for the file path of the python script to be compiled.  *(full or relative)*  
Must include .py in name. 
```commandline
Python File Path: 
```

Then asks for the name of the exe to compile to.  This will also be the name of the folder it creates in the `Output Directory.`  

```
(leave empty to use name of .py file)
Exe Name: 
```

### [d] Batch With Dependencies

Has an additional prompt to include files or directories ***parallel*** to the script to be compiled.
*(full or relative)*  
The menu will enter into a loop of requesting files until the user enters a blank line.

```commandline
Include Dependency: path1
Include Dependency: path2
Include Dependency: 
```
The compiler will copy the file structure exactly into the `Output Directory` containing the .exe

For example:

```commandline
                                          |Output Directory/ 
|Working Directory/             --->      |    exe_name/
|    script.py                  --->      |        exe_name.exe
|    dependency1                --->      |        dependency1
|    subdir/                    --->      |        subdir/
|            dependency2        --->      |            dependency2
|            dependency3        --->      |            dependency3
|            
```

***Dependencies outside of the `Working Directory` will not work!***

-------
## Settings Menu

Opening settings will automatically generate a config file with the `cwd` as the `Working Directory` and 
the `Output Directory`.

```commandline
Working Directory: C:\Users\{username}\PycharmProjects\PyTools4Windows\project
Output Directory: C:\Users\{username}\PyTools4Windows

[w]- Change Working Directory
[d]- Change Output Directory
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


