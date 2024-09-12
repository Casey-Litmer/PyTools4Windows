from menucmd import Menu, edit_list, dynamic_wrapper
from macrolibs.typemacros import list_union
import os, winreg as reg, ctypes



MODES = {
        "user":(reg.HKEY_CURRENT_USER, r"Environment"),
        "sys":(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
    }


result = Menu.result

def main():

    main_menu = Menu(name = "Edit PATH")
    path_menu = Menu(arg_to = dynamic_wrapper(change_name))


    main_menu.append(
        ("u", "Edit user PATH", (path_menu, "user")),
        ("s", "Edit system PATH", (path_menu, "sys")),
        #("n", "Edit session PATH", (path_menu, "sesh")),      #Devs, let me know if this is a useful feature, then I will add it
    )

    path_menu.append(
        ("p", "Show PATH", (
            get_path, result[0],
            show_path, result
        )),
        ("r", "Remove path from PATH", (
            get_path, result[0],
            edit_list, (result, Menu.kwargs(name= "Remove Paths:")),
            set_path, (result, result[0])
        )),
        ("a", "Add paths to PATH", (
            get_path, result[0], add_paths, (),
            list_union, (result[1], result[2]),
            set_path, (result, result[0])
        ))

    )


    main_menu()


def change_name(menu_id, arg):
    menu_id.name = "Edit " + {"sys":"System","user":"User"}[arg] + " Path"
    return arg


#---------------------------------------------------------------------------------------------------------------------

def get_path(mode: str) -> list:
    reg_key, paths = None, []

    #Change Mode
    mode_data = MODES[mode]

    try:
        # Open the registry key for user environment variables
        reg_key = reg.OpenKey(mode_data[0], mode_data[1], 0, reg.KEY_ALL_ACCESS)

        # Get the current PATH value
        paths = reg.QueryValueEx(reg_key, "Path")[0].split(os.pathsep)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if reg_key:
            reg.CloseKey(reg_key)

    #Remove empty lines
    if "\n" in paths:
        paths.remove("\n")
    if "" in paths:
        paths.remove("")

    #Remove all duplicates (keeps order)
    #paths = list_union([[x] for x in paths])

    return paths if paths else Menu.escape


def show_path(paths: list) -> None:
    print("\n")
    for i in paths:
        print(i)
    print("\nPATH=" + os.pathsep.join(paths) + "\n")


def set_path(paths: list, mode: str) -> None:
    #Remove all duplicates (keeps order)
    paths = list_union([[x] for x in paths])

    #Change Mode
    mode_data = MODES[mode]

    reg_key = None
    try:
        # Open the registry key for user environment variables
        reg_key = reg.OpenKey(mode_data[0], mode_data[1], 0, reg.KEY_ALL_ACCESS)

        # Set the new PATH value in the registry
        reg.SetValueEx(reg_key, "Path", 0, reg.REG_EXPAND_SZ, os.pathsep.join(paths))

        #Update system
        notify_environment_change()
        print("PATH updated...\nRestart the session for changes to take effect.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if reg_key:
            reg.CloseKey(reg_key)


def add_paths() -> list:
    new_paths = []

    print("\n(* for all immediate subdirectories) (non-recursive)")
    print("('cwd' for current directory)")

    while new_path := input("New Path: "):
        if new_path.strip() == "cwd":
            new_paths.append(os.getcwd())
        elif new_path[-1] == "*":
            new_paths += [os.path.join(new_path[:-1], path) for path in os.listdir(new_path[:-1])]
        else:
            new_paths.append(new_path)

    return new_paths


def notify_environment_change() -> None:
    # Broadcasts the WM_SETTINGCHANGE message to notify the system
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x1A
    SMTO_ABORTIFHUNG = 0x0002
    r = ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", SMTO_ABORTIFHUNG, 5000, None)
    if r:
        print("Environment change broadcast successfully.")
    else:
        print("Failed to broadcast environment change.")


######################################################################################################################

if __name__ == "__main__":
    main()