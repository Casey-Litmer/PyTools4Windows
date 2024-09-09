import menucmd
from menucmd import Menu, Bind as B
from copy import copy

def main():
    result = Menu.result
    kwargs = Menu.kwargs


    menu_shell = Token(shell_struct, name= "shell", return_to = lambda x: x)

    #menu_git = Token(git_struct, name= "git", exit_to = menu_shell, end_to= Menu.exit_to, escape_to= Menu.exit_to, return_to = update_memory2)

    """""
    menu_shell.append(
        ("g", "git", (menu_git, "git", update_memory, (menu_shell, result))),
        ("p", "pip", (menu_git, (), update_memory, (menu_shell, result))),
        ("t", "twine", (menu_git, (), update_memory, (menu_shell, result))),
    )
    """""

    print(menu_shell(""))  #empty memory struct

    """""
    menu_git.append(
        ("p", "push", (lambda s: s + " push", result)),
        ("l", "pull", (lambda s: s + " pull", result), menu_git_pull, result)

    )

    menu_git_pull.append(
        ("o", "origin", (
            lambda s: s + " origin", result,
            input, B(lambda s: s + " (branch):", result)
        ))
    )
"""""


#perhaps make the entire thing a struct?  Only using token class.  Try 'shell_struct'
shell_struct = {
    "git":("g", {
        "pull":("l", {
            "origin":("o", "(branch): ")
        }),
        "push":("p", None)
    })
}



class Token():
    def __init__(self, struct: dict, **kwargs):
        """words: [(key1, word1, token1),(key2, word2, token2)]"""
        self.menu = Menu(**kwargs)

        self.words = struct
        self.kwargs= kwargs

        #append previous commands
        #WIP


        #append tags
        pairs = zip(self.words.keys(), self.words.values())
        pairs2 = zip(self.words.keys(), self.words.values())
        #print(*pairs2)
        #print(self.words.keys())
        #print(self.words.values())
        #print(*pairs)
        #self.menu.append(*map(self.format_entry, [*pairs])) #check on this
        self.append_menu()


    def append_menu(self):
        for k in self.words:
            word = k
            key = self.words[k][0]
            data = self.words[k][1]

            go_to = (Token(data, **self.kwargs), ()) if isinstance(data, dict) else \
                (   #git pull origin (words): #
                    input, B(lambda s: s + " " + data, Menu.result),  #asks for input labled (data)
                    lambda s: s + Menu.result, Menu.result[0],  #append user input to assemblage
                    run_command, Menu.result,  #run command with full string
                    #append to past commands
                    #
                    #print, Menu.result[3],
                    lambda: Menu.result[3], (),  #return assemblage (str)
                    #menucmd.f_escape, ()
                )

            item = (key, word, (
                lambda s: s + " " + word, Menu.result,
                print, Menu.result,
                *go_to
            ))

            self.menu.append(item)



    def __call__(self, arg = None):
        print("token called")
        #for x in self.menu.menu_item_list:
        #    print(x)
        return self.menu(arg)


    def format_entry(self, pair):
        word = pair[0]     #str
        #print(word)
        key = pair[1][0]   #str
        #print(key)
        data = pair[1][1]  #dict or str
        #print(type(data))


        #Options for f_switch
        #   lambda () -> entry_type
        go_to = [
            (Token(data, **self.kwargs), ()),  #Adds a menu call from new dict depth
            (
                #git pull origin (words): #
                input, B(lambda s: s + " " + data, Menu.result),     #asks for input labled (data)
                lambda s: s + Menu.result, Menu.result[0],        #append user input to assemblage
                run_command, Menu.result,                         #run command with full string
                #append to past commands
                #
                print, Menu.result[2],
                lambda: Menu.result[2], (),                       #return assemblage (str)
                #menucmd.f_escape, ()
            )
        ]

        r = (key, word, (
            lambda s: s + " " + word, Menu.result,
            *go_to[not isinstance(data, dict)]
        ))

        print(r)
        return r


def run_command(command):
    #subprocess goes here.
    print("hi")



if __name__ == "__main__":
    main()