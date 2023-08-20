# local-machine-password-manager
Tired of cloud services and their data breaches? Try a local machine password manager instead.

**Installation**  

Download the four python files and the requirements.txt 

Enter the following into terminal:  
`pip install -r requirements.txt`  

A virtual environment is highly recommended.  
If on a linux system, please ensure you have xclip or xsel installed in your distro as pyperclip requires them.  

**Running the program**  

`python main.py`  


This is a CLI password manager that stores your passwords in your local machine. Comes with the function to generate passwords as well, 
with options from alphabet only, numbers only, alphanumeric and alphanumeric with special characters. 
All passwords are encrypted using AES-256 before storing. Passwords for verification are hashed using argon2.
The create an account option on the main menu screen is a local account only. It is purely for the sake of separating users, 
if multiple users on the same local machine need to use this program.

Note: This software is provided as is. The author is not accountable for any lost of passwords or data breaches from the use of this program.
Please backup your passwords.

**Future plans**

- Different language support  
- Some way to transfer latest db file across machines on a local network  

Extra concerns/comments:
> 1. Copying passwords to clipboards is not safe.
   - Yes it's not. I do make sure to replace system clipboard contents after 30 seconds.
     Honestly this would be better as a browser extension so maybe I'll try my hand at that next time.
     However, if attackers have access to your system clipboard you probably have bigger things to worry about.
     Any application that keeps clipboard history would be problematic however as all previously copied passwords would be there.
> 2. Handling passwords as strings are unsafe as strings are immutable and will persist in memory.
   - Python unfortunately does not handle strings as character arrays so using character arrays is not an option.
     That said if would be attackers can read memory dumps on your machine you have bigger problems to worry about.
