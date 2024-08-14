__author__ = "github.com/tohkunhao"
__version__ = "0.1.2"

import menu
import database
import notifications

def main():
    db = database.Database()
    gen_pw_menu_C = menu.Menu(["Registration successful? (y/n): "],
                              [db.register_new_service],
                              "C",
                              "2",
                              "3",
                              "1",
                              [getattr(menu.Menu,"cache")],
                              exit_code="b",
                              is_yes_no=True,
                              clear_screen_on_display=False,
                              is_sequential=True,
                              display_current_pos=False,
                              clear_cache_on_run=False,
                              clear_cache_on_exit=False,
                              show_exit_prompt=False)

    gen_pw_menu_B = menu.Menu(["Length: "],
                              [db.generate_pw,gen_pw_menu_C.run],
                              "B",
                              "3",
                              "B",
                              "1",
                              [getattr(menu.Menu,"cache"),""],
                              exit_code="b",
                              exit_label="Go back",
                              clear_screen_on_display=False,
                              is_sequential=True,
                              display_current_pos=False,
                              clear_cache_on_run=False,
                              clear_cache_on_exit=False,
                              show_exit_prompt=False)

    gen_pw_menu_preB = menu.Menu(["Specified Special Characters: "],
                                 [gen_pw_menu_B.run],
                                 "b",
                                 "3",
                                 "b",
                                 "1",
                                 exit_code="b",
                                 exit_label="Go back",
                                 clear_screen_on_display=False,
                                 is_sequential=True,
                                 display_current_pos=False,
                                 clear_cache_on_run=False,
                                 clear_cache_on_exit=False,
                                 show_exit_prompt=False)

    reg_svc_menu_2 = menu.Menu(["Alphabet only","Numbers only","Alphanumeric","Alphanumeric with special character",
                                "Alphanumeric with specified characters"],
                               [gen_pw_menu_B.run, gen_pw_menu_B.run, gen_pw_menu_B.run, gen_pw_menu_B.run, gen_pw_menu_preB.run],
                               "3",
                               "2",
                               "3",
                               "1",
                               exit_code="b",
                               exit_label="Go back",
                               clear_cache_on_run=False)
    
    gen_pw_menu_A = menu.Menu(["Service Name: ","Service Website: ","Username: "],
                              [db.check_service_duplicate,reg_svc_menu_2.run],
                              "A",
                              "2",
                              "A",
                              "1",
                              [getattr(menu.Menu,"cache"),""],
                              exit_code="b",
                              exit_label="Go back",
                              is_sequential=True,
                              clear_cache_on_run=False,
                              clear_cache_on_exit=False)

    input_pw_menu = menu.Menu(["Service Name: ","Service Website: ","Username: ","Password: "],
                              [db.register_new_service],
                              "A",
                              "2",
                              "2",
                              "1",
                              [getattr(menu.Menu,"cache")],
                              exit_code="b",
                              exit_label="Go back",
                              is_sequential=True)

    reg_svc_menu = menu.Menu(["Generate a password","Manually input a password"],
                             [gen_pw_menu_A.run,input_pw_menu.run],
                             "2",
                             "1",
                             "2",
                             "1",
                             exit_code="b",
                             exit_label="Go back")

    ret_pw_menu = menu.Menu(["Copy to clipboard","Display on screen"],
                            [db.retrieve_password],
                            "3",
                            "2",
                            "3",
                            "1",
                            [getattr(menu.Menu,"cache")],
                            exit_code="b",
                            exit_label="Go back",
                            clear_cache_on_run=False,
                            clear_cache_on_exit=False)
    
    change_pw_gen_menu_B = menu.Menu(["Registration successful? (y/n): "],
                                     [db.change_service_password],
                                     "B",
                                     "4",
                                     "4",
                                     "1",
                                     [getattr(menu.Menu,"cache")],
                                     exit_code="b",
                                     is_yes_no=True,
                                     clear_screen_on_display=False,
                                     is_sequential=True,
                                     display_current_pos=False,
                                     clear_cache_on_run=False,
                                     clear_cache_on_exit=False,
                                     show_exit_prompt=False)

    change_pw_gen_menu_C = menu.Menu(["Use special characters? (y/n): "],
                                     [change_pw_gen_menu_B.run],
                                     "A",
                                     "4",
                                     "A",
                                     "1",
                                     exit_code="b",
                                     is_yes_no=True,
                                     is_sequential=True,
                                     clear_cache_on_run=False,
                                     clear_cache_on_exit=False)

    change_pw_menu_4 = menu.Menu(["Copy new password to clipboard","Display new password on screen"],
                                 [db.ret_and_gen_password],
                                 "6",
                                 "5",
                                 "6",
                                 "1",
                                 [getattr(menu.Menu,"cache")],
                                 exit_code="b",
                                 exit_label="Go back",
                                 clear_cache_on_run=False,
                                 clear_cache_on_exit=False,
                                 func_on_succeed=change_pw_gen_menu_B.run)
    
    change_pw_gen_menu_A = menu.Menu(["Length: "],
                                     [change_pw_menu_4.run],
                                     "A",
                                     "5",
                                     "A",
                                     "1",
                                     exit_code="b",
                                     clear_screen_on_display=False,
                                     is_sequential=True,
                                     display_current_pos=False,
                                     clear_cache_on_run=False,
                                     clear_cache_on_exit=False,
                                     show_exit_prompt=False)
    
    change_pw_gen_menu_preA = menu.Menu(["Specified Special Characters: "],
                                        [change_pw_gen_menu_A.run],
                                        "a",
                                        "5",
                                        "a",
                                        "1",
                                        exit_code="b",
                                        clear_screen_on_display=False,
                                        is_sequential=True,
                                        display_current_pos=False,
                                        clear_cache_on_run=False,
                                        clear_cache_on_exit=False,
                                        show_exit_prompt=False)
    
    change_pw_menu_3 = menu.Menu(["Alphabet only","Numbers only","Alphanumeric","Alphanumeric with special character",
                                  "Alphanumeric with specified characters"],
                                 [change_pw_gen_menu_A.run, change_pw_gen_menu_A.run, change_pw_gen_menu_A.run,
                                  change_pw_gen_menu_A.run, change_pw_gen_menu_preA.run],
                                 "5",
                                 "4",
                                 "5",
                                 "1",
                                 exit_code="b",
                                 exit_label="Go back",
                                 clear_cache_on_run=False,
                                 clear_cache_on_exit=False)

    change_pw_man_confirm_menu = menu.Menu(["Are you sure? (y/n): "],
                                           [db.change_service_password],
                                           "B",
                                           "4",
                                           "B",
                                           "1",
                                           [getattr(menu.Menu,"cache")],
                                           exit_code="n",
                                           is_yes_no=True,
                                           is_sequential=True,
                                           clear_cache_on_run=False,
                                           clear_cache_on_exit=False,
                                           show_exit_prompt=False)

    change_pw_manual_menu = menu.Menu(["New password: "],
                                      [db.ret_and_gen_password,change_pw_man_confirm_menu.run],
                                      "A",
                                      "4",
                                      "1",
                                      "1",
                                      [getattr(menu.Menu,"cache"),""],
                                      exit_code="b",
                                      exit_label="Go back",
                                      is_sequential=True,
                                      clear_cache_on_run=False,
                                      clear_cache_on_exit=False)

    change_pw_menu_2 = menu.Menu(["Generate new password","Manually input new password"],
                                 [change_pw_menu_3.run,change_pw_manual_menu.run],
                                 "4",
                                 "3",
                                 "4",
                                 "1",
                                 exit_code="b",
                                 exit_label="Go back",
                                 clear_cache_on_run=False,
                                 clear_cache_on_exit=False)

    change_pw_menu = menu.Menu(["Copy old password to clipboard","Display old password on screen"],  
                               [change_pw_menu_2.run],
                               "3",
                               "2",
                               "3",
                               "1",
                               exit_code="b",
                               exit_label="Go back",
                               clear_cache_on_run=False,
                               clear_cache_on_exit=False)

    del_pw_menu = menu.Menu(["Are you sure you want to delete this service? (y/n): "],
                            [db.delete_service_password],
                            "A",
                            "1",
                            "A",
                            "1",
                            [getattr(menu.Menu,"cache")],
                            exit_code="n",
                            is_yes_no=True,
                            is_sequential=True,
                            clear_cache_on_run=False,
                            show_exit_prompt=False)
    
    def menu_brancher(cache):
        if cache["1"] == "1":
            return ret_pw_menu.run()
        elif cache["1"] == "2":
            return change_pw_menu.run()
        elif cache["1"] == "3":
            return del_pw_menu.run()
        
    from_db_list_menu = menu.Menu(db.list_services,
                                  [menu_brancher],
                                  "2",
                                  "1",
                                  "2",
                                  "1",
                                  [getattr(menu.Menu,"cache")],
                                  exit_code="b",
                                  exit_label="Go back",
                                  clear_cache_on_run=False)

    change_mas_pw_menu = menu.Menu(["Old master password: ","New master password: ","Re-enter new master password: "],
                                   [db.change_master_pw],
                                   "2",
                                   "1",
                                   "1",
                                   "1",
                                   [getattr(menu.Menu,"cache")],
                                   exit_code="b",
                                   exit_label="Go back",
                                   is_sequential=True)

    userscreen = menu.Menu(["Register new service","Retrieve password","Change service password",
                            "Delete service","Change master password"],
                           [reg_svc_menu.run,from_db_list_menu.run,from_db_list_menu.run,
                            from_db_list_menu.run,change_mas_pw_menu.run],
                           "1",
                           "0",
                           "1",
                           "1",
                           exit_code="l",
                           exit_label="Logout",
                           exit_func=db.logout,)

    master_pw_check = menu.Menu(["Enter user's password: ","Re-enter user's password: "],
                                [db.delete_user],
                                "B",
                                "1",
                                "B",
                                "0",
                                [getattr(menu.Menu,"cache")],
                                exit_code="b",
                                exit_label="Go back",
                                is_sequential=True,
                                clear_cache_on_run=False)

    del_user_confirmation = menu.Menu(["Are you sure you want to delete selected account? (y/n): "],
                                      [master_pw_check.run],
                                      "A",
                                      "0",
                                      "A",
                                      "0",
                                      exit_code="n",
                                      is_yes_no=True,
                                      is_sequential=True,
                                      clear_cache_on_run=False,
                                      show_exit_prompt=False)

    show_users = menu.Menu(db.list_users,
                           [del_user_confirmation.run],
                           "1",
                           "0",
                           "1",
                           "0",
                           exit_code="b",
                           exit_label="Go back to main menu")

    login= menu.Menu(["Username: ","Password: "],
                     [db.login, userscreen.run],
                     "A",
                     "0",
                     "0",
                     "0",
                     [getattr(menu.Menu,"cache"),""],
                     exit_code="b",
                     exit_label="Go back to main menu",
                     is_sequential=True)

    create_new_account = menu.Menu(["Choose a username: ","Choose a password: "],
                                   [db.create_new_account],
                                   "A",
                                   "0",
                                   "0",
                                   "0",
                                   [getattr(menu.Menu,"cache")],
                                   exit_code="b",
                                   exit_label="Go back to main menu",
                                   is_sequential=True)

    main_menu = menu.Menu(["Create New Account","Login","Delete account"],
                          [create_new_account.run,login.run,show_users.run],
                          "0",
                          "0",
                          "0",
                          "0")
    main_menu.run()
    notifications.clear_screen()

if __name__ == "__main__":
    main()
