__author__ = "github.com/tohkunhao"
__version__ = "0.1.2"


import sqlite3
import os
from argon2 import PasswordHasher
import hashlib
import secrets
from Cryptodome.Cipher import AES
import notifications
import pyperclipfix as pyperclip
import string

class Database():
    
    __pw_db_col = "(u_key TEXT, svcName TEXT, svcSite TEXT, username TEXT, enc_pw TEXT, salt TEXT, nonce TEXT, tag TEXT)"
    __user_db_col = "(user TEXT, password TEXT)"
    
    def __init__(self):
        self.__username = None
        self.__masterpw = None
        self.__connection_DB = None
        self.__cursor = None
        self.__ph = PasswordHasher()
        self.__temp_pw_store = None
        self.__index_to_ukey = {}
        self.__hashed_name = None

    def db_connector(func):
        def with_connection(self, *args, **kwargs):
            self.__connection_DB = sqlite3.connect("passDB.db")
            self.__cursor = self.__connection_DB.cursor()
            
            returned_value = func(self, *args, **kwargs)

            self.__cursor.close()
            self.__connection_DB.close()
            return returned_value
        return with_connection

    def db_table_check(self, table_name, col_input):
        self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name}{col_input}")
    
    @db_connector
    def login(self, cache, verify_only=False, user=None, mas_pw=None):
        
        if verify_only:
            username = user
            password = mas_pw
        else:
            username = cache["Username: "]
            password = cache["Password: "]
        
        self.db_table_check("userDB",self.__class__.__user_db_col)
        self.__cursor.execute("SELECT * FROM userDB WHERE user = ?", (username,))
        result = self.__cursor.fetchall()
        
        if result is []:
            notifications.error_msg("Invalid credentials!")
            return False
        else:
            try:
                verified = self.__ph.verify(result[0][1], password)
            except:
                verified = False
                notifications.error_msg("Invalid credentials!")
            if verified and not verify_only:
                self.__username = cache["Username: "]
                self.__masterpw = cache["Password: "]
                username_bytes = self.__username.encode("utf-8")
                self.__hashed_user = "user" + hashlib.sha3_256(username_bytes).hexdigest()
                if self.__ph.check_needs_rehash(result[0][1]):
                    self.__cursor.execute("UPDATE userDB SET password = ? WHERE name = ?",
                                          (self.__ph.hash(self.__masterpw),self.__username))
                    self.__connection_DB.commit()
            return verified

    def logout(self):
        self.__username = None
        self.__masterpw = None
        self.__class__.__hashed_user = None
        self.__index_to_ukey.clear()

    @db_connector
    def create_new_account(self, cache):
        self.db_table_check("userDB",self.__class__.__user_db_col)
        self.__cursor.execute("SELECT * FROM userDB WHERE user = ?", (cache["Choose a username: "],))
        if self.__cursor.fetchone() is not None:
            notifications.error_msg("Invalid credentials!")
            return False
        else:
            user = cache["Choose a username: "]
            self.__cursor.execute("INSERT INTO userDB VALUES (?,?)",(user, self.__ph.hash(cache["Choose a password: "])))
            self.__connection_DB.commit()
            return True

    @db_connector
    def register_new_service(self, cache):
        y_n_catch = "Registration successful? (y/n): "
        if y_n_catch in cache.keys() and cache[y_n_catch]=="n":
            return False
        pyperclip.copy("")
        service_name = cache["Service Name: "]
        service_site = cache["Service Website: "]
        username = cache["Username: "]
        combi_str = service_name + username
        unique_key = hashlib.sha3_256(combi_str.encode("utf-8")).hexdigest()
        
        if "Password: " in cache.keys():
            encrypt_pass, salt, nonce, tag = self.__aes_encrypt(cache["Password: "], self.__masterpw)
        else:
            encrypt_pass, salt, nonce, tag = self.__aes_encrypt(self.__temp_pw_store, self.__masterpw)
            self.__temp_pw_store = None
        self.db_table_check(self.__hashed_user,self.__class__.__pw_db_col)
        self.__cursor.execute(f"INSERT INTO {self.__hashed_user} VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                              (unique_key, service_name, service_site, username, encrypt_pass, salt, nonce, tag))
        self.__connection_DB.commit()
        notifications.error_msg("Service registered.")
        return True

    def check_service_duplicate(self, cache):
        service_name = cache["Service Name: "]
        service_site = cache["Service Website: "]
        username = cache["Username: "]
        combi_str = service_name + username
        unique_key = hashlib.sha3_256(combi_str.encode("utf-8")).hexdigest()
        result = self.__get_entry_from_db(self.__hashed_user,self.__class__.__pw_db_col,
                                          "*", "u_key", unique_key, False)
        if result is not None:
            notifications.error_msg("Service already registered!")
            return False
        else:
            return True

    def retrieve_password(self, cache, prefix=""):
        display_type = cache["3"]
        db_key = self.__get_dynamic_list_sel("2", cache)
        q_result = self.__get_entry_from_db(self.__hashed_user,self.__class__.__pw_db_col,
                                          "enc_pw, salt, nonce, tag", "u_key", db_key, False)
        pw = self.__aes_decrypt(q_result, self.__masterpw)
        notifications.clear_screen()

        if prefix=="":
            noun_caps = "Password"
        else:
            noun_caps = "password"

        if display_type == "0":
            pyperclip.copy(pw)
            print(f"{prefix} {noun_caps} copied to clipboard")
        elif display_type == "1":
            print(f"{prefix} {noun_caps}: {pw}")
        notifications.countdown_timer(f"{prefix} {noun_caps} will be cleared in:",30)
        pyperclip.copy("")
        notifications.clear_screen()
        return True

    def __get_dynamic_list_sel(self, node_level, cache):
        selection = cache[node_level]
        return self.__index_to_ukey[selection]

    def ret_and_gen_password(self, cache):
        self.retrieve_password(cache, "Old")
        if "5" in cache.keys():
            ret = self.generate_pw(cache, cache["5"], "New")
            if ret:
                notifications.countdown_timer("Password will be cleared in:", 15)
                pyperclip.copy("")
        else:
            self.__temp_pw_store = cache["New password: "]
            ret = True
        return ret
    
    def change_service_password(self, cache):
        y_n_catch = "Registration successful? (y/n): "
        if y_n_catch in cache.keys() and cache[y_n_catch]=="n":
            return False

        db_key = self.__get_dynamic_list_sel("2", cache)
        enc_pw, salt, nonce, tag = self.__aes_encrypt(self.__temp_pw_store, self.__masterpw)
        self.__temp_pw_store = None
        ret = self.__update_entry_db(self.__hashed_user, self.__class__.__pw_db_col,
                                     "enc_pw = ?, salt = ?, nonce = ?, tag = ?", "u_key",
                                     (enc_pw, salt, nonce, tag, db_key))
        notifications.error_msg("Service password changed.")
        return ret
        
    def delete_service_password(self, cache):
        db_key = self.__get_dynamic_list_sel("2", cache)
        ret = self.__delete_entry_from_table(self.__hashed_user, self.__class__.__pw_db_col, "u_key", db_key)
        notifications.error_msg("Service deleted")
        return ret

    def change_master_pw(self, cache):
        if self.login(cache, True, self.__username, cache["Old master password: "]):
            if cache["New master password: "] != cache["Re-enter new master password: "]:
                notifications.error_msg("New passwords do not match!")
                return False
            else:
                ret1 = self.__re_encrypt_db(cache["Old master password: "],cache["New master password: "])
                ret2 = self.__update_entry_db("userDB", self.__class__.__user_db_col,"password = ?",
                                              "user",(self.__ph.hash(cache["New master password: "]), self.__username))
                self.__masterpw = cache["New master password: "]
                if ret1 and ret2:
                    notifications.error_msg("Master password updated.")
                return ret1 and ret2
        else:
            return False

    def __re_encrypt_db(self, old_pw, new_pw):
        result = self.__get_entry_from_db(self.__hashed_user, self.__class__.__pw_db_col,
                                          "enc_pw, salt, nonce, tag, u_key")
        if result == []:
            return True

        for db_row in result:
            svc_pw = self.__aes_decrypt(db_row, old_pw)
            re_encrypted, salt, nonce, tag = self.__aes_encrypt(svc_pw, new_pw)
            ret = self.__update_entry_db(self.__hashed_user,
                                         self.__class__.__pw_db_col,
                                         "enc_pw = ?, salt = ?, nonce = ?, tag=?",
                                         "u_key",
                                         (re_encrypted, salt, nonce, tag, db_row[4]))
        return True
    
    @db_connector
    def __get_entry_from_db(self, table_name, table_col, query_col, query_key=None, db_key=None, fetch_all=True):
        self.db_table_check(table_name, table_col)
        
        if db_key == None:
            self.__cursor.execute(f"SELECT {query_col} FROM {table_name}")
        else:
            self.__cursor.execute(f"SELECT {query_col} FROM {table_name} WHERE {query_key} = ?",(db_key,))
        
        if fetch_all:
            return self.__cursor.fetchall()
        else:
            return self.__cursor.fetchone()

    @db_connector
    def __update_entry_db(self, table_name, table_col, query_col, query_key, arg_tuple):
        self.db_table_check(table_name, table_col)
        self.__cursor.execute(f"UPDATE {table_name} SET {query_col} WHERE {query_key} = ?", arg_tuple)
        self.__connection_DB.commit()
        return True

    @db_connector
    def __delete_entry_from_table(self, db_table, db_col, db_key_col, db_key):
        self.db_table_check(db_table, db_col)
        self.__cursor.execute(f"DELETE FROM {db_table} WHERE {db_key_col} = ?", (db_key,))
        self.__connection_DB.commit()
        return True

    @db_connector
    def __drop_table(self, db_table):
        self.__cursor.execute(f"DROP TABLE IF EXISTS {db_table}")
        self.__connection_DB.commit()
        return True

    def delete_user(self, cache):
        user = self.__get_dynamic_list_sel("1",cache)
        if cache["Enter user's password: "] != cache["Re-enter user's password: "]:
            notifications.error_msg("The passwords do not match!")
            return False
        else:
            if self.login({}, True, user, cache["Enter user's password: "]):
                entry_result = self.__delete_entry_from_table("userDB", self.__class__.__user_db_col, "user", user)
                drop_table = self.__drop_table("user"+hashlib.sha3_256(user.encode("utf-8")).hexdigest())
                notifications.error_msg("Account has been deleted")
                return entry_result and drop_table
            else:
                notifications.error_msg("Invalid credentials!")
                return False

    def __list_from_db(self, query_col, table_name, table_col, list_format):
        self.__index_to_ukey.clear()
        result = self.__get_entry_from_db(table_name, table_col, query_col)
        
        if result == []:
            return result
        
        processed_list = []
        for index, db_row in enumerate(result):
            self.__index_to_ukey[str(index)] = db_row[0]
            if list_format == "service":
                processed_list.append(f"Service: {db_row[1]}({db_row[2]})/Username: {db_row[3]}")
            elif list_format == "users":
                processed_list.append(f"{db_row[0]}")

        return processed_list

    def list_services(self):
        return self.__list_from_db("u_key, svcName, svcSite, username",
                                   self.__hashed_user, 
                                   self.__class__.__pw_db_col,
                                   "service")

    def list_users(self):
        return self.__list_from_db("user", "userDB", self.__class__.__user_db_col, "users")

    def generate_pw(self, cache, output_type="", prefix=""):
        if output_type == "":
            pw_type = cache["3"]
        else:
            pw_type = output_type

        if pw_type == "0":
            usable_chars = string.ascii_letters
            has_digit = True
            has_special = True
        elif pw_type == "1":
            usable_chars = string.digits
            has_digit = True
            has_upper = True
            has_lower = True
            has_special = True
        elif pw_type == "2":
            usable_chars = string.ascii_letters + string.digits
            has_special = True
        elif pw_type == "3":
            usable_chars = string.ascii_letters + string.digits + string.punctuation
        elif pw_type == "4":
            usable_chars = string.ascii_letters + string.digits + cache["Specified Special Characters: "]

        length = cache["Length: "]
        if not length.isnumeric():
            print("Length is not numeric!")
            return False
        elif int(length) < 4:
            print("Password Length is too short!")
            return False

        while True:
            pw = ''.join(secrets.choice(usable_chars) for i in range(int(length)))
            
            if pw_type != "1":
                has_lower = any(c.islower() for c in pw)
                has_upper = any(c.isupper() for c in pw)
                if pw_type != "0":
                    has_digit = any(c.isdigit() for c in pw)
                    if pw_type == "3" or pw_type == "4":
                        has_special = any(c in string.punctuation for c in pw)

            if has_lower and has_upper and has_digit and has_special:
                break

        if prefix == "":
            verb_past = "Generated"
        else:
            verb_past = "generated"
        
        if "6" in cache.keys() and cache["6"] == "1":
            print(f"{prefix} {verb_past} password: {pw}")
        else:
            pyperclip.copy(pw)
            print(f"{prefix} {verb_past} password copied to clipboard.")
        self.__temp_pw_store = pw
        return True

    def __aes_encrypt(self, password, mas_pw):
        salt = secrets.token_bytes(AES.block_size)
        encrypt_key = hashlib.scrypt(mas_pw.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=16)
        aes_cipher = AES.new(encrypt_key, AES.MODE_GCM)
        cipher_text, tag = aes_cipher.encrypt_and_digest(password.encode("utf-8"))
        return cipher_text, salt, aes_cipher.nonce, tag

    def __aes_decrypt(self, db_return, mas_pw):
        decrypt_key = hashlib.scrypt(mas_pw.encode("utf-8"), salt=db_return[1], n=2**14, r=8, p=1, dklen=16)
        aes_cipher = AES.new(decrypt_key, AES.MODE_GCM, nonce=db_return[2])
        plain_text = aes_cipher.decrypt_and_verify(db_return[0], db_return[3])
        return plain_text.decode("utf-8")


