import subprocess as sp, os
from menucmd import Menu, Bind as B, escape_on
from macrolibs.filemacros import get_script_dir, full_walk, open_json, save_json
from macrolibs.typemacros import list_union


#Get script run location and config path
DIR = get_script_dir()
CONFIG_PATH = os.path.join(os.path.abspath(DIR), "config.json")
DEFAULT_CONFIG = {"outpath":os.getcwd(), "cwd":os.getcwd()}



result = Menu.result

def main():
    #Config load call
    get_json = B(open_json, CONFIG_PATH, DEFAULT_CONFIG)

    main_menu = Menu(name= "PyInstaller")
    settings_menu = Menu(name= "Settings", exit_to= main_menu, end_to= Menu.exit_to, arg_to= show_dirs)
    batch_menu = Menu(name= "Batch", exit_to= main_menu, end_to= Menu.exit_to)



    main_menu.append(
        ("b", "Batch a Script", (batch_menu, get_json)),
        ("s", "Settings", (settings_menu, get_json)),
        ("w", "Open Working Directory", (open_dir, (get_json, "cwd"))),
        ("d", "Open Output Directory", (open_dir, (get_json, "outpath"))),
    )


    input_script_path = B(lambda x: x.strip(), B(input, "Python File Path: "))

    #result[0] = config
    batch_menu.append(
        ("b", "Batch", (
            escape_on, (input_script_path, ""),
            batch, (result[0].CONFIG, result.SCRIPT_PATH),
            escape_on, (result.BATCH_DATA, None),
            installer, (result.BATCH_DATA.expand(), )
        )),
        ("d", "Batch with dependencies", (
            escape_on, (input_script_path, ""),
            batch, (result[0].CONFIG, result.SCRIPT_PATH),
            escape_on, (result.BATCH_DATA, None),
            inc_dependencies, (result.CONFIG, B(lambda x:x[0], result.BATCH_DATA)),
            escape_on, (result.DEPENDENCIES, None),
            installer, (result.BATCH_DATA.expand(), Menu.kwargs(dependencies = result.DEPENDENCIES))
        )),
    )

    settings_menu.append(
        ("w", "Change Working Directory", (change_dir, (result.CONFIG, "cwd"))),
        ("d", "Change Output Directory", (change_dir, (result.CONFIG, "outpath")))
    )


    main_menu()


#----------------------------------------------------------------------------------------------------------------------



def batch(config: dict, script_path: str, exe_name: str | None = None) -> tuple | None:
    """Batch a script with or without dependencies"""
    outpath = config["outpath"]
    cwd = config["cwd"]

    #Get full path
    full_path = os.path.join(cwd, script_path)
    script_path = full_path if os.path.exists(full_path) else script_path

    #Break if path does not exist
    if not os.path.exists(script_path):
        print(f"Path '{script_path}' does not exist.")
        return None

    #Get exe name
    if exe_name is None:
        print("(leave empty to use name of .py file)")
        exe_name = input("Exe Name: ")
    exe_name = exe_name if exe_name else os.path.basename(script_path)[:-3]

    exe_path = os.path.join(outpath, exe_name)

    return (exe_path, exe_name, script_path)


def installer(exe_path: str, exe_name: str, script_path: str, dependencies: list = []) -> None:

    print(f"Compiling {exe_name}...")

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


def inc_dependencies(config: dict, exe_path: str, dependencies: list | None = None) -> list | None:
    """"""
    cwd = config["cwd"]

    #dependencies: [(path, new_path),]

    #User input for dependencies
    if dependencies is None:
        dependencies = []

        while dep := input("Include Dependency: ").strip():
            full_path = os.path.join(cwd, dep)

            #Break if path does not exist
            if not os.path.exists(full_path):
                print(f"Path '{full_path}' does not exist.")
                return None

            dependencies.append(full_path)

    #Get full list of dependencies
    full_list = []
    for full_path in dependencies:
        #Mirrors path structure in outpath
        new_path = lambda p: os.path.join(exe_path, os.path.relpath(p, start=cwd))

        #Add all subdirs and files to dependency list if dir, else add single path
        if os.path.isdir(full_path):
            full_list = list_union(full_list,  #Get full paths for all files and zip with new path
                                      list(zip(files := full_walk(full_path), list(map(new_path, files)))))
        else:
            full_list = list_union(full_list, [(full_path, new_path(full_path))])


    return full_list



#----------------------------------------------------------------------------------------------------------------------

def show_dirs(config: dict) -> dict:
    """arg_to for settings menu.  Takes config struct, prints directories and returns struct."""
    print(f"Working Directory: {config["cwd"]}")
    print(f"Output Directory: {config["outpath"]}")

    return config


#Update config
def change_dir(config: dict, key: str) -> None:
    """Update config paths.  Takes the config struct and stores the user input into the corresponding key."""
    print("('cwd' for current directory)")
    new_dir = input({"cwd":"Working Directory: ", "outpath":"Output Directory: "}[key])
    new_dir = os.getcwd() if new_dir.strip() == "cwd" else new_dir

    save_json(config | {key:new_dir}, CONFIG_PATH)


def open_dir(config: dict, key: str) -> None:
    """key = 'cwd' to open working directory, 'outpath' to open output directory"""
    sp.run(["explorer", config[key]])


#######################################################################################################################

if __name__ == "__main__":
    main()