import subprocess as sp, os
from menucmd import Menu, yesno_ver
from macrolibs.filemacros import get_script_dir, full_walk, open_json, save_json
from macrolibs.typemacros import list_union


DIR = get_script_dir()

CONFIG_PATH = os.path.join(os.path.abspath(DIR), "config.json")
DEFAULT_CONFIG = {"outpath":os.getcwd(), "cwd":os.getcwd()}


def main():
    result = Menu.result

    main_menu = Menu(name= "PyInstaller")
    settings_menu = Menu(name= "Settings", exit_to= main_menu, end_to= Menu.exit_to, arg_to= show_dirs)
    batch_menu = Menu(name= "Batch", exit_to= main_menu, end_to= Menu.exit_to)


    main_menu.append(
        ("b", "Batch a Script", (batch_menu, ())),
        ("s", "Settings", (settings_menu, ())),
        ("w", "Open Working Directory", (
            open_json, (CONFIG_PATH, DEFAULT_CONFIG),
            lambda x:x["cwd"], result,
            sp.run, ["explorer", result],
            Menu.end, ()
        )),
        ("d", "Open Output Directory", (
            open_json, (CONFIG_PATH, DEFAULT_CONFIG),
            lambda x: x["outpath"], result,
            sp.run, ["explorer", result],
            Menu.end, ()
        )),
    )

    batch_menu.append(
        ("b", "Batch", (batch, False)),
        ("d", "Batch with dependencies", (batch, True)),
    )

    settings_menu.append(
        ("w", "Change Working Directory", (change_dir, (result, "cwd"))),
        ("d", "Change Output Directory", (change_dir, (result, "outpath")))
    )


    main_menu()


#----------------------------------------------------------------------------------------------------------------------

#Batch a script
def batch(inc_dependencies = False) -> None:
    #Open config
    config = open_json(CONFIG_PATH, DEFAULT_CONFIG)
    outpath = config["outpath"]
    cwd = config["cwd"]

    #Get script (full or relative path)
    script_path = input("Python File Path: ")

    #Break if no entry
    if not script_path:
        return Menu.escape

    #Get full path
    full_path = os.path.join(cwd, script_path)
    script_path = full_path if os.path.exists(full_path) else script_path

    #Break if path does not exist
    if not os.path.exists(script_path):
        print(f"Path '{script_path}' does not exist.")
        return Menu.escape

    #Get exe name
    print("(leave empty to use name of .py file)")
    exe_name = input("Exe Name: ")
    exe_name = exe_name if exe_name else os.path.basename(script_path)[:-3]

    exe_path = os.path.join(outpath, exe_name)

    #Include Dependencies
    dependencies = []  #[(path, new_path),]
    if inc_dependencies:
        while dep := input("Include Dependency: ").strip():
            full_path = os.path.join(cwd, dep)

            #Break if path does not exist
            if not os.path.exists(full_path):
                print(f"Path '{full_path}' does not exist.")
                return Menu.escape

            #Mirrors path structure in outpath
            new_path = lambda p: os.path.join(exe_path, os.path.relpath(p, start=cwd))

            #Add all subdirs and files to dependency list if dir, else add single path
            if os.path.isdir(full_path):
                dependencies = list_union(dependencies,  #Get full paths for all files and zip with new path
                                          list(zip(files := full_walk(full_path), list(map(new_path, files)))))
            else:
                dependencies = list_union(dependencies, [(full_path, new_path(full_path))])

    print("Compiling...")

    #Copy Dependencies
    os.mkdir(exe_path)
    for src, dest in dependencies:
        if not os.path.exists(new_dir := os.path.split(dest)[0]):
            os.mkdir(new_dir)
        r = sp.run(["copy", src, dest], check=True, capture_output=True, text=True, shell=True)

        print(r.stdout.strip("\n"))

    #Run
    line = ["--distpath", exe_path, "--workpath", os.path.join(exe_path, "build"), "--specpath", exe_path]
    r = sp.run(["pyinstaller", *line, f"--name={exe_name}", "--onefile", script_path],
           check=True, capture_output=True, text=True)

    print(r.stdout); print(r.stderr)



def batch_another_script():
    return yesno_ver(yes=None, no=Menu.__END__, name="Batch Another Script?")

#----------------------------------------------------------------------------------------------------------------------

#arg_to for settings
def show_dirs() -> dict:
    config = open_json(CONFIG_PATH, DEFAULT_CONFIG)
    print(f"Working Directory: {config["cwd"]}")
    print(f"Output Directory: {config["outpath"]}")

    return config


#Update config
def change_dir(config: dict, key: str) -> None:
    print("('cwd' for current directory)")
    new_dir = input({"cwd":"Working Directory: ", "outpath":"Output Directory: "}[key])
    new_dir = os.getcwd() if new_dir.strip() == "cwd" else new_dir

    save_json(config | {key:new_dir}, CONFIG_PATH)



#######################################################################################################################

if __name__ == "__main__":
    main()