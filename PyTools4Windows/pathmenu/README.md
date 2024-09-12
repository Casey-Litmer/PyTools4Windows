```
pip install pytools4windows.pathmenu
```

Menu interface for changing the PATH environment variable.



## Main Menu

-------

```commandline
Edit PATH
[u]- Edit user PATH
[s]- Edit system PATH
[e]- exit
```

### [u] Edit User Path

Edit the PATH for the current user only

### [s] Edit System Path

Edit the PATH for the whole system


## Path Menu

-------
```commandline
Edit {User/System} Path
[p]- Show PATH
[r]- Remove path from PATH
[a]- Add paths to PATH
[e]- exit
```

### [p] Show PATH

Prints a list of all entries in the PATH variable, as set in the registry
and the full path string.
```commandline
C:\Windows\system32
C:\Windows
C:\Windows\System32\Wbem
C:\Windows\System32\WindowsPowerShell\v1.0\
C:\Windows\System32\OpenSSH\
C:\Program Files\dotnet\
C:\Program Files\Git\cmd
C:\Users\{current-user}\AppData\Local\Programs\Python\Python312\Scripts\
C:\Users\{current-user}\AppData\Local\Programs\Python\Python312\
C:\Users\{current-user}\PyTools4Windows\pyinstallermenu
C:\Users\{current-user}\PyTools4Windows\commandmenu
C:\Users\{current-user}\PyTools4Windows\pathmenu

PATH=C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;......
```


### [r] Remove Entries From PATH

Select which path(s) to remove.  Updates PATH on `exit`.

```commandline
[0]- C:\Windows\system32
[1]- C:\Windows
[2]- C:\Windows\System32\Wbem
[3]- C:\Windows\System32\WindowsPowerShell\v1.0\
[4]- C:\Windows\System32\OpenSSH\
[5]- C:\Program Files\dotnet\
[6]- C:\Program Files\Git\cmd
[7]- C:\Users\{current-user}\AppData\Local\Programs\Python\Python312\Scripts\
[8]- C:\Users\{current-user}\AppData\Local\Programs\Python\Python312\
[9]- C:\Users\{current-user}\PyTools4Windows\pyinstallermenu
[10]- C:\Users\{current-user}\PyTools4Windows\commandmenu
[11]- C:\Users\{current-user}\PyTools4Windows\pathmenu
[e]- exit
```

### [a] Add Paths to PATH

Prompts the user to enter multiple paths.  *(full or relative)* \
The menu will enter into a loop of requesting files until the user enters a blank line.

```commandline
(* for all immediate subdirectories) (non-recursive)
('cwd' for current directory)
New Path: path1
New Path: path2
New Path: cwd
New Path: C:\Users\{current user}\Destkop\folder\*
New Path:
```

Enter `cwd` for the current working directory.

Writing `folder\*` will include all subdirectories in folder, non-recursively.

**To add all PyTools4Windows exes to the PATH, write:** 
```
C:\Users\{current user}\PyTools4Windows\*
```

