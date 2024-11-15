import initial_data
from tkinter import *
import random_data
import os
import sys
import json
from random import choice
from tkinter import messagebox
from tkinter import simpledialog
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import pyperclip

build_password = []
password_result = ''
RED = "#D4483B"
BACK_GROUND = "black"

# Determine the base path
if getattr(sys, 'frozen', False):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(".venv"))
else:
    base_path = os.path.abspath(".venv")

initial_data = initial_data.new_user
# Load configuration
config_path = os.path.join(base_path, "config.json")
with open(config_path, "r") as config_file:
    config = json.load(config_file)

# Use paths from configuration
key_path = os.path.join(base_path, config.get("key_path", "vault_key.key"))
vault_data_path = os.path.join(base_path, config.get("vault_data_path", "vault_data.json"))

# Ensure the directories exist
os.makedirs(os.path.dirname(key_path), exist_ok=True)
os.makedirs(os.path.dirname(vault_data_path), exist_ok=True)

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Generate and save the key if it does not exist
if not os.path.exists(key_path):
    password = simpledialog.askstring("Password", "Enter a password to derive the key:", show='*')
    if password is None:
        raise ValueError("Password is required to generate the key.")
    salt = os.urandom(16)
    key = derive_key(password, salt)
    with open(key_path, "wb") as key_file:
        key_file.write(salt + key)
else:
    with open(key_path, "rb") as key_file:
        data = key_file.read()
        salt, key = data[:16], data[16:]
        try_loop = 3
        password = simpledialog.askstring("Password", "Enter your password to derive the key:", show='*')
        while password is None or derive_key(password, salt) != key:
            if messagebox.askyesno(title="Incorrect Password", message="Access Denied\ntry again?"):
                password = simpledialog.askstring("Password", "Enter your password to derive the key:", show='*')
                try_loop -= 1
                if password is None or derive_key(password, salt) != key and try_loop <= 0:
                    messagebox.showinfo(title="Oops..", message="To many failed attempts.\n Program is closing.")
                    exit()
        key = derive_key(password, salt)

cipher_suit = Fernet(key)


# Read the game_data.json file with error handling
try:
    with open(vault_data_path, "rb") as vault_data:
        encode_data = vault_data.read()
        if encode_data:
            try:
                decode_data = cipher_suit.decrypt(encode_data)
                json_data = json.loads(decode_data.decode('utf-8'))
            except InvalidToken:
                print("Error: Invalid token. The data may be corrupted or the key may not match.")
                json_data = {}
        else:
            json_data = {}
        print("Data loaded successfully")
except FileNotFoundError:
    print(f"Error: The file {vault_data_path} does not exist.")
    json_data = {}
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from the file.")
    json_data = {}
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    json_data = {}

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def make_password():
    global password_result,build_password
    if len(password_result) > 0:
        password_result = ''

    build_password = [
        choice(random_data.starter_words),
        choice(random_data.string_numbers),
        choice(random_data.animals),
        choice(random_data.clothes),
        choice(random_data.verbs),
        choice(random_data.symbols)
    ]
    process_password = ''.join(build_password)
    for letter in process_password:
        if letter in random_data.leet_dict:
            password_result += random_data.leet_dict[letter]
        else:
            password_result += letter

    password_entry.delete(0,END)
    password_entry.insert(0,password_result)
    pyperclip.copy(password_result)
    build_password = []


# ---------------------------- SAVE PASSWORD ------------------------------- #
def check_new_user():
    try:
        with open(vault_data_path, "rb") as vault_data:
            encode_data = vault_data.read()
            if encode_data:
                decode_data = cipher_suit.decrypt(encode_data)
                json_data = json.loads(decode_data.decode('utf-8'))
            else:
                json_data = initial_data
    except FileNotFoundError:
        json_data = initial_data
    except json.JSONDecodeError:
        json_data = initial_data
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        json_data = initial_data

    if json_data.get("mypass.master", {}).get("master", "") == "":
        set_password = simpledialog.askstring(title="Master Password", prompt="Set your Master Password", show='*')
        if set_password is None:
            messagebox.showinfo(title="Cancelled", message="Password setup was cancelled.")
            quit()
        new_pass = {
            "mypass.master": {
                "master": set_password
            }
        }
        if len(new_pass) >0:
            json_data.update(new_pass)
            with open(vault_data_path, "wb") as vault_data:
                encode_data = cipher_suit.encrypt(json.dumps(json_data).encode('utf-8'))
                vault_data.write(encode_data)
        else:
            quit()

def save_password():
    no_match = False
    global vault_data, json_data
    website = website_entry.get().lower()
    email_username = email_UN_entry.get().lower()
    password = password_entry.get().lower()
    if len(website) <= 2 or len(password) <= 4 or len(email_username) <= 3:
        messagebox.showinfo(title="Oops...",message="Looks Like your missing some info in the \nEmail or password field.")
    else:

        try:
            with open(vault_data_path, "rb") as vault_data:
                encode_data = vault_data.read()
                decode_data = cipher_suit.decrypt(encode_data)
                json_data = json.loads(decode_data.decode('utf-8'))
        except FileNotFoundError:
            json_data = {}
        except json.JSONDecodeError:
            json_data = {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            json_data = {}

        try:
            if website in json_data and email_username in json_data[website]:
                if json_data[website][email_username] == "":
                    json_data[website][email_username] = password
            data_to_check = json_data
            if data_to_check[website.lower()][email_username.lower()]:
                if messagebox.askyesnocancel(title="Oops..",message=f'Looks like you already saved\n'
                                            f'"{email_username}"\n for \n"{website}". \nClick Yes to view the password'):
                    master_pass = simpledialog.askstring(title="Master Password", prompt="Please enter your Master Password: ",show='*')
                    if master_pass == json_data["mypass.master"]["master"]:
                        return_pass = json_data[website][email_username]
                        password_entry.delete(0,END)
                        password_entry.insert(0,return_pass)
                return
        except KeyError:
            no_match = True


        if no_match:
            if website not in json_data:
                json_data[website] = {}
            json_data[website][email_username] = password
            with open(vault_data_path, "wb") as vault_data:
                encode_data = cipher_suit.encrypt(json.dumps(json_data).encode('utf-8'))
                vault_data.write(encode_data)
            messagebox.showinfo(title="Saved",message="Password was saved")
                # json.dump(json_data,vault_data, indent=4)

def search_data():
    global vault_data, json_data
    website = website_entry.get().lower()
    try:
        with open(vault_data_path, "rb") as vault_data:
            encode_data = vault_data.read()
            decode_data = cipher_suit.decrypt(encode_data)
            json_data = json.loads(decode_data.decode('utf-8'))
    except FileNotFoundError:
        json_data = {}
    except json.JSONDecodeError:
        json_data = {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        json_data = {}

    try:
        if website in json_data:
            master_pass = simpledialog.askstring(title="Master Password", prompt="Please enter your Master Password\n "
                                                                                 "to view saved data: ",
                                                 show='*')
            if master_pass == json_data["mypass.master"]["master"]:
                email_username_dict = json_data[website]
                email_username = list(email_username_dict.keys())[0]
                password = email_username_dict[email_username]
                website_entry.delete(0,END)
                website_entry.insert(0,website)
                email_UN_entry.delete(0,END)
                email_UN_entry.insert(0,email_username)
                password_entry.delete(0,END)
                password_entry.insert(0,password)
        else:
            messagebox.showinfo(title="Result",message="No account was found with that website name.\n"
                                                       "note: only use the name of the site not the url")

    except KeyError:
        messagebox.showinfo(title="Result", message="No account was found with that website name.\n"
                                                    "note: only use the name of the site not the url")



# ---------------------------- UI SETUP ------------------------------- #
check_new_user()
# Window configs
window = Tk()
window.title("Bob's PassPhrase Generator")
window.configure(bg=BACK_GROUND,borderwidth=30,padx=50,pady=50)

# Canvas
bg_image = PhotoImage(file=os.path.join(base_path, "logo.png"))
canvas = Canvas(window, width=200,height=200)
canvas.grid(row=0, column=1,padx=20,pady=20)
canvas.configure(bg="black",highlightthickness=0)
canvas.create_image(100,100,image=bg_image)

# Label
label_website = Label(text="Website: ",fg=RED,bg=BACK_GROUND,highlightthickness=0,font=("Arial",12,"bold"))
label_website.grid(row=1,column=0,padx=10,sticky="e")
label_email_UN = Label(text="Email/Username: ",fg=RED,bg=BACK_GROUND,highlightthickness=0,font=("Arial",12,"bold"))
label_email_UN.grid(row=2,column=0,padx=10,sticky="e")
label_pw = Label(text="Password: ",fg=RED,bg=BACK_GROUND,highlightthickness=0,font=("Arial",12,"bold"))
label_pw.grid(row=3,column=0,padx=10,sticky="e")

# Enter/inputs
website_entry = Entry(width=33,bg="white",highlightthickness=0,font=("Arial",12,""))
website_entry.focus()
website_entry.grid(row=1,column=1,columnspan=1,sticky="w",pady=3)
email_UN_entry = Entry(width=47,bg="white",highlightthickness=0,font=("Arial",12,""))
email_UN_entry.grid(row=2,column=1,columnspan=2,sticky="w")
password_entry = Entry(width=47,bg="white",highlightthickness=0,font=("Arial",12,""))
password_entry.grid(row=3,column=1,columnspan=2,sticky="w",pady=3)

# Buttons
gen_pw_button = Button(text="Generate Password",highlightthickness=0,command=make_password,width=17)
gen_pw_button.grid(row=4,column=2,sticky="w")
add_button = Button(text="Add",highlightthickness=0,width=42,command=save_password)
add_button.grid(row=4,column=1,sticky="w")
search_button = Button(text="Search",highlightthickness=0,width=17,command=search_data)
search_button.grid(row=1,column=2,sticky="w")










window.mainloop()