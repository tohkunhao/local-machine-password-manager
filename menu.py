__author__ = "github.com/tohkunhao"
__version__ = "0.1"

import notifications
from time import sleep
import getpass
import copy
import types

class Menu:
    '''
    Class used to create menus.
    Menus can display a list, or progressively display prompts.
    
    Constructor arguments:
    list_items - list(str) or function reference - List of strings containing different menu options to print to screen.
                                                   Function reference must be to a function with no arguments.
    list_funcs - list(func) - List of functions that are executed according to which menu option is chosen.
    node_level - (str) - The node level of the menu object in the menu tree. This is to aid traversal and node jumps.
                         Non-sequential menus should be an integer string, i.e. 0, 1, 2, 3.
                         Sequential menus should not be numeric.
                         Root menu should be 0.
    exit_node - (str) - This is the node level to exit to when exit code is pressed.
    on_fail - (str) - This is the node level to exit to if any of the options selected fail.
    on_succeed - (str) - This is the node level to exit to if any of the options selected succeed.
    func_args - (list) default: [] - This are list of arguments that will be fed into list_funcs functions. 
                                     Each index correspond to each function. Use list of lists where necessary.
    exit_code - (str) default : "q" - Key to press to escape out of the current menu.
    exit_label - (str) default: "Quit" - Label for exit button.
    exit_func - (func) default: None - Function to execute when exit code is pressed.
    clear_screen_on_display - (bool) default: True - True to clear the terminal on displaying current menu object. 
                                                     False to leave it as is.
    is_sequential - (bool) default: False - True to make menu progressive display prompt.
                                            False to make it display a list of items at once.
                                            When used as sequential, list_func is executed in loop after
                                            looping through all items in list_items.
    display_current_pos - (bool) default: True - True to show position in menu tree.
                                                 False to not show anything.
    '''
    
    prev_selection = ["Main Menu"]
    exit_to = None
    pop_status = False
    cache = {}

    def __init__(self, 
                list_items, 
                list_funcs, 
                node_level,
                exit_node,
                on_fail,
                on_succeed,
                func_args = [], 
                exit_code = "q",
                exit_label = "Quit",
                exit_func = None,
                is_yes_no = False,
                clear_screen_on_display = True,
                is_sequential = False,
                display_current_pos = True,
                clear_cache_on_run = True,
                clear_cache_on_exit = True,
                show_exit_prompt = True,
                func_on_succeed = None,
                fos_arg = None):
        
        self.list_items = list_items
        self.list_funcs = list_funcs
        self.node_level = node_level
        self.exit_node = exit_node
        self.on_fail = on_fail
        self.on_succeed = on_succeed
        self.exit_label = exit_label
        self.func_args = func_args
        self.exit_code = exit_code
        self.exit_func = exit_func
        self.clear_screen_on_display = clear_screen_on_display
        self.is_sequential = is_sequential
        self.display_current_pos = display_current_pos
        self.clear_cache_on_run = clear_cache_on_run
        self.clear_cache_on_exit = clear_cache_on_exit
        self.tree_position = None
        self.is_yes_no = is_yes_no
        self.show_exit_prompt = show_exit_prompt
        self.func_on_succeed = func_on_succeed
        self.fos_arg = fos_arg
	
    def run(self):
        selection = "start"
        while selection.lower() != self.exit_code:
            if self.clear_screen_on_display:
                notifications.clear_screen()

            '''=====SHOW NODE POSITION====='''
            if self.display_current_pos:
                if self.node_level.isnumeric():
                    while len(self.__class__.prev_selection) - 1 > int(self.node_level):
                        self.__class__.prev_selection.pop(-1)

                self.tree_position = self.__class__.prev_selection[0]
                for index in range(1,len(self.__class__.prev_selection)):
                    self.tree_position += ">" + self.__class__.prev_selection[index]
                print(self.tree_position)
                print("")
            '''=====LOG IN STATUS====='''

            '''=====CLEAR CACHE====='''
            if self.clear_cache_on_run:
                self.__class__.cache.clear()

            '''=====MENU LIST====='''
            if type(self.list_items) == types.FunctionType or type(self.list_items) == types.MethodType:
                list_to_use = self.list_items()
            else:
                list_to_use = self.list_items

            '''=====DISPLAY====='''
            if list_to_use == []:
                print("No items to display")
            else:
                for index, item in enumerate(list_to_use):
                    if self.is_sequential:
                        if index == 0 and self.show_exit_prompt:
                            print(f"Press {self.exit_code} to {self.exit_label.lower()}")
                            print("")

                        if "password" in item.lower():
                            sequence_input = getpass.getpass(f"{item}")
                        else:
                            sequence_input = input(f"{item}")

                        if sequence_input == self.exit_code:
                            selection = self.exit_code
                            self.__class__.exit_to = self.exit_node
                            self.__class__.pop_status = True
                            if self.clear_cache_on_exit:
                                self.__class__.cache.clear()
                            func_succeed = False
                            if self.exit_func is not None:
                                self.exit_func()
                            break
                        elif self.is_yes_no and sequence_input not in ["y","n"]:
                            func_succeed = False
                            self.__class__.pop_status = True
                            self.__class__.exit_to = self.node_level
                            notifications.error_msg("Not a valid input!")
                        else:
                            self.__class__.cache[item] = sequence_input

                    else:
                        print(f"{index}. {item}")
            
            '''=====EXECUTE SELECTION====='''
            if self.is_sequential and len(list_to_use) > 0 and not self.__class__.pop_status:
                func_succeed = True
                for i, fun in enumerate(self.list_funcs):
                    if func_succeed:
                        func_succeed = self.func_execute(i)        
                    else:
                        self.__class__.exit_to = self.on_fail
                        self.__class__.pop_status = True
                        break
            elif not self.is_sequential:
                print(f"{self.exit_code}. {self.exit_label}")
                print("")
                selection = input("Please enter selection: ")
                func_succeed = self.parse_selection(selection, list_to_use)
                if func_succeed and self.func_on_succeed is not None and self.fos_arg is not None:
                    self.func_on_succeed(self.fos_arg)
                elif func_succeed and self.func_on_succeed is not None and self.fos_arg is None:
                    self.func_on_succeed()
            
            '''=====NODE TRAVERSAL====='''
            if func_succeed and not self.__class__.pop_status and selection != self.exit_code:
                self.__class__.exit_to = self.on_succeed
            elif not func_succeed and not self.__class__.pop_status and selection != self.exit_code:
                self.__class__.exit_to = self.on_fail
            
            if not self.__class__.pop_status:
                self.__class__.pop_status = True

            if self.__class__.pop_status:
                if self.__class__.exit_to != self.node_level:
                    selection = self.exit_code
                else:
                    self.__class__.pop_status = False

        return True

    def parse_selection(self, selection, items):
        if selection.isnumeric():
            if int(selection) < len(items):
                self.tree_pos_update(selection + ". " + items[int(selection)])
                self.__class__.cache[self.node_level] = selection
                if len(self.list_funcs)==1:
                    return self.func_execute(0)
                else:
                    return self.func_execute(int(selection))
            else:
                notifications.error_msg("Not a valid selection!")
        elif selection !=  self.exit_code:
            notifications.error_msg("Not a valid selection!")
        else:
            self.__class__.exit_to = self.exit_node
            self.__class__.pop_status = True
            if self.clear_cache_on_exit:
                self.__class__.cache.clear()
            if self.exit_func is not None:
                self.exit_func()
        return False

    def func_execute(self, index):
        if len(self.func_args) == 0 or self.func_args[index] == "":
            return self.list_funcs[index]()
        else:
            return self.list_funcs[index](self.func_args[index])

    def tree_pos_update(self, add_level = None):
        if add_level not in self.__class__.prev_selection:
            self.__class__.prev_selection.append(add_level)

    def clear_cache(self):
        self.__class__.cache.clear()

    def debug(self):
        for key in aggregate_dict.keys():
            print(aggregate_dict[key])
        sleep(2)
