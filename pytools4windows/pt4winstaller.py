from menucmd import Menu, yesno_ver, choose_items, f_switch, f_end
import os
from macrolibs.filemacros import get_script_dir
from macrolibs.typemacros import list_union

from .pathmenu.pathmenu import get_path, set_path, notify_environment_change
from .pyinstallermenu.pyinstallermenu import batch, installer, inc_dependencies, open_dir



DEFAULT_EXE_PATH = os.path.join(os.path.expanduser("~"), "pytools4windows")
DIR = get_script_dir()

print(DIR)
print(os.listdir(DIR))

result = Menu.result

def main():

    main_menu = Menu(name = "Install pytools4windows", end_to=Menu.exit_to)

    main_menu.append(
        ("x", "Install", (
            get_install_location, (),
            choose_installs, result[-1].OUTPATH,
            batch_list, (result[-1].INSTALLS, result.OUTPATH),

            yesno_ver, Menu.kwargs(name="Add to PATH?", exit_message="no"),
            f_switch(result, [f_end, add_paths_to_PATH]), result[-2].EXE_PATHS,

            yesno_ver, Menu.kwargs(name="Open PyTools4Windows Folder?", exit_message="no"),
            f_switch(result, [f_end, open_dir]), ({"outpath":result.OUTPATH}, "outpath"),
        ))
    )

    main_menu()
    
#---------------------------------------------------------------------------------------------------------------------

def get_install_location() -> str:
    path = DEFAULT_EXE_PATH
    print("Default Install Location: ")
    print(os.path.split(path)[0] + "\\")

    #Ask for different install location
    if yesno_ver(name = "Use different location?", exit_message = "no"):
        while not os.path.exists(i := input("New Location: ")) and i.strip():
            print(f"{i} does not exist")

        path = os.path.join(i, "pytools4windows") if i.strip() else DEFAULT_EXE_PATH

    return path


def choose_installs(path: str) -> list:
    libs = []

    for _dir in os.listdir(DIR):
        full_path = os.path.join(DIR, _dir)

        print("subdir: ", full_path)
        print("isdir: ", os.path.isdir(full_path))
        print("has init: ", os.path.isdir(full_path) and "__init__.py" in os.listdir(full_path))

        if os.path.isdir(full_path) and "__init__.py" in os.listdir(full_path):
            script = os.path.join(full_path, f"{_dir}.py")  #main script MUST have same name as subpackage
            libs.append(script)

    if yesno_ver(name = "Install", yes_message= "All .exe", exit_message = "Specific Exes"):
        return libs
    else:
        return choose_items(libs, name = f"Install Exes to {path}", display_as = lambda x:os.path.basename(x)[:-3])


def batch_list(paths: list[str], outpath: str) -> list[str]:
    exe_paths = []
    #paths = []
    for path in paths:
        cwd = os.path.dirname(path)
        config = {"cwd":cwd, "outpath":outpath}
        data = batch(config, path, exe_name="")
        exe_paths.append(data[0])

        dependencies = []

        include = os.path.join(cwd, "__include__.txt")
        print("basename: ", cwd)
        if os.path.exists(include):
            print("True")
            with open(include, "r") as f:
                dependencies = map(lambda x:os.path.join(cwd, x), f.readlines())
            f.close()

        dependencies = inc_dependencies(config, data[0], dependencies=dependencies)

        installer(*data, dependencies=dependencies)

    return exe_paths


def add_paths_to_PATH(exe_paths: list[str]) -> None:
    PATH = list_union(get_path("user"), exe_paths)
    set_path(PATH, "user")
    notify_environment_change()



####################################################################################################################

if __name__ == "__main__":
    main()
