from menucmd import Menu, Bind as B, edit_list, dynamic_wrapper
import subprocess as sp, os, sys
from re import sub
from macrolibs.filemacros import get_script_dir, open_json, save_json
from macrolibs.typemacros import list_compliment, list_intersect, list_union
from default_struct import DEFAULT_STRUCT


#Get mode argument
try:
    mode = sys.argv[1]
except IndexError:
    mode = "global"

if mode not in ("global", "local"):
    raise f"{mode} not recognized"


#Get script run location and config path
DIR = os.path.abspath(get_script_dir())
CONFIG_PATH = os.path.join(DIR, "config.json")

if mode == "local":
    CONFIG_PATH = os.path.join(os.getcwd(), "commandmenu_config.json")


result = Menu.result

def main():
    #Menu definitions
    main_menu = Menu(name = "Commands", arg_to= dynamic_wrapper(dyn_arg_to))
    settings_menu = Menu(name = "Settings", exit_to= main_menu, end_to= Menu.exit_to)
    memory_menu = Menu(name = "Memory", exit_to= B(main_menu, []), end_to= Menu.exit_to)

    #Memory manager function (attributed to main_menu)
    main_menu.add_mem = lambda cmd: update_memory(memory_menu, cmd)
    update_memory(memory_menu, [])

    #Main Menu
    main_menu.append(("$", "Settings", (settings_menu, ())),
                            ("#", "Memory", (memory_menu, ()))
                            #(Other items appended via arg_to)
                     )

    #Settings Menu
    settings_menu.append(
        ("i", "Include Commands", (inc_commands, ())),
        ("x", "Exclude Commands", (exc_commands, ())),
        ("m", "Change Memory Length", (
            change_memory_length, (),
            update_memory, (memory_menu, [])
        ))
    )

    #Run main_menu
    main_menu([])


#---------------------------------------------------------------------------------------------------------------------

#Removes '[key]' from beginning of string
remove_brackets = lambda k: k[k.index("]")+1:]

#Removes string between #...#
remove_comments = lambda k: sub(r"#.*?#", "", k)


#TODO for later version:  create markdown for returning to specific menu!
#TODO...    Also allow for chains of {"input1"} {"input2"}... etc

#Convert command json structs to nested menus
def struct_to_items(S: dict, add_mem, **kwargs) -> tuple:
    #Appends subcommands.  Menu comp morphism
    append_command = lambda x, xs: x + list(xs.strip().split()) * bool(xs)
    append_user_input = lambda x, xs: x + [xs.strip()] * bool(xs)

    #switches func/args base on input type.  ad-hoc polymorphism
    def val_behaviour(k: str) -> tuple:
        v = S[k]

        #Open new menu
        if isinstance(v, dict):
            new_menu = Menu(**kwargs)                    #<--- change menucmd to have dynamic names  (arg -> name)
            new_menu.add_mem = add_mem                                #pass main_menu memory func to all nested menus
            new_menu.append(*struct_to_items(v, add_mem, **kwargs))   #recursion call:
            return (new_menu, result[1])                              #convert all nested dicts to nested menu items

        #Ask for input and run
        elif isinstance(v, str):
            q = 0 #q = v[0] == "r"  #this might be necessary (test later)
            return (input, v.strip("r"),                                      #get user input
                    lambda s:q*"\""+ s +"\""*q, result,                       #add quotes if not 'r' string
                    Menu.id, B(append_user_input, result[1], result),   #append to command
                    sp.run, (result),                                         #run command
                    #print, B(" ".join, result[-2]),                          #print full command (unnecessary)
                    B(lambda x: x.add_mem, Menu.self), result[-2],      #update menu memory
                    Menu.end, ())                                             #escape_to = end_to = main_menu

        #Run
        elif v == []:
            return (sp.run, result[1],                                        #run full command
                    B(lambda x:x.add_mem, Menu.self), result[1],        #update menu memory
                    Menu.end, ())                                             #end chain

    #Condense dict key to menu key
    def format_key(k: str) -> str:
        first_idx = k.index("[") + 1
        second_idx = k.index("]")
        return k[first_idx:second_idx]

    #Dict key to menu item
    format_to_item = lambda x: (format_key(x), remove_brackets(x).replace("#",""), (             #key, message, (
                                Menu.id, B(append_command, result[0],                     #append to command
                                            remove_comments(remove_brackets(x))),               #also remove #-# text here
                                print, B(" ".join, result))                               #display command
                                + val_behaviour(x)                                              #ad-hoc val_behaviour
                                )                                                               #)
    #Return all items
    return tuple(map(format_to_item, S))


#----------------------------------------------------------------------------------------------------------------------
#Collect all non-excluded json and return full struct.  Save config.json
def get_struct() -> dict:
    sett = open_json(CONFIG_PATH, DEFAULT_STRUCT)

    S = {}; names = []
    for file in os.listdir(os.path.join(DIR, "jsons")):
        name = os.path.basename(file).strip("json")[:-1]             #name of file
        file_path = os.path.join(DIR, "jsons", file)                 #path of json (must be in relative jsons folder)

        if file[-5:] == ".json" and name != "config":
            json_struct = open_json(file_path); full_name = list(json_struct)[0]          #Get full dictionary
            names.append(full_name)                                                       #Append full_name to list

            if full_name not in sett["exclude"]:
                S = S | json_struct                                                           #Add json to runtime struct
                sett["commands"] = list_union(sett["commands"], [full_name])               #Add new commands to list

    sett["commands"] = list_intersect(sett["commands"], names)    #Remove all non-existent jsons from the list
    sett["exclude"] = list_intersect(sett["exclude"], names)      #|

    save_json(sett, CONFIG_PATH)

    return S


#Updates main_menu items on arg_to.  Passes arg.
def dyn_arg_to(menu, arg):
    menu.add_mem([])    #Do this to update any changes in the memory length.  Kind of spaghetti-y, I know.
                        #Maybe separate concerns by adding json_open/json_save into the settings menu functions themselves
                        #instead of having them accept and return dict.
    menu.delete(2, len(menu.menu_item_list) - 1)

    struct = get_struct()

    menu.append(*struct_to_items(struct, menu.add_mem, exit_to=B(menu, []),
                                 end_to=Menu.exit_to, escape_to=Menu.end_to,
                                 ))
    return arg


def update_memory(menu: Menu, command: list[str]) -> None:
    #Get saved memory
    sett = open_json(CONFIG_PATH, DEFAULT_STRUCT)
    length = int(sett["memory length"])
    L = sett["memory"]
    L = list_union([command], L)[:length] if command else L

    #Update Memory menu
    menu.clear()
    menu.append(*[(str(n), " ".join(cmd), (      #[n]- 'command'
        sp.run, cmd,                             #run each command (list[str])
        update_memory, (menu, cmd),              #refresh memory list, ensures same behaviour as manual run
        Menu.end, ()                             #
    )) for n, cmd in enumerate(L)])              #for all commands in L

    sett["memory"] = L
    save_json(sett, CONFIG_PATH)


#---------------------------------------------------------------------------------------------------------------------

def inc_commands() -> None:
    sett = open_json(CONFIG_PATH, DEFAULT_STRUCT)
    exclude = sett["exclude"]

    abbr_pairs = {remove_brackets(k):k for k in exclude}

    new = edit_list(list(abbr_pairs), name= "Include:", empty_message= "-*Nothing To Include*-")
    new = [abbr_pairs[n] for n in new]

    sett["exclude"] = new
    save_json(sett, CONFIG_PATH)


def exc_commands() -> None:
    sett = open_json(CONFIG_PATH, DEFAULT_STRUCT)
    commands = sett["commands"]
    exclude = sett["exclude"]

    abbr_pairs = {remove_brackets(k): k for k in commands}

    new = edit_list(list(abbr_pairs), name= "Exclude:", empty_message= "-*Nothing To Exclude*-")
    new = [abbr_pairs[n] for n in new]

    sett["exclude"] = list_union(list_compliment(commands, new), exclude)
    sett["commands"] = new

    save_json(sett, CONFIG_PATH)


def change_memory_length() -> None:
    sett = open_json(CONFIG_PATH, DEFAULT_STRUCT)
    length = sett["memory length"]
    print("Memory Length: ", length)

    while new_length := input("New Length: ").strip():
        try:
            length = int(new_length)
            break
        except ValueError:
            print("length must be an integer")

    sett["memory length"] = length
    sett["memory"] = sett["memory"][:length]
    save_json(sett, CONFIG_PATH)


####################################################################################################################

if __name__ == "__main__":
    main()