#!/usr/bin/python3
###
# Above line makes the file executable with Python3
# To make the file fully execuatble wite:" ./py_pwm.py " command in terminal do the following
# in terminal "chmod 755 py_pwm.py"
# ALTERNATIVLY you can always just type "python3 py_pwm.py"
###
import json

# PySimpleGUI has to be installed "pip3 install pysimplegui"
import PySimpleGUI as sg

# The library rncryptor has to be installed "pip3 install rncryptor"
import rncryptor
cryptor = rncryptor.RNCryptor()

# The encrypted file that contains the password, call it something else if you wish.
# It has to reside in the same folder as this script
data_file = 'my_manager.dat'

# Change the colorsheme of the GUI ref: https://www.geeksforgeeks.org/themes-in-pysimplegui/
sg.theme('DarkBlack1')

# Not logged in yet
login = False

# Figure out if passwordfile exists
def startup_check():
    try:
        with open(data_file, "rb") as fc:
            ready = "Password file found!"
            sub_pass = "Master Password: "
    except FileNotFoundError:
        ready = "No password file found! If this is first use, don't worry! Else look for a file named \"my_manager.dat\" and place it in the script folder."
        sub_pass = "Please enter a Master: "
    return ready, sub_pass

def open_pw_file(password):
    global login
    try:
        with open(data_file, "rb") as fc: # Opens file
            enc_data = fc.read() # Read the encrypted file
            try:
                data = json.loads(cryptor.decrypt(enc_data, password)) # Try to decrypt
            except:
                return {}, "Probably wrong passwords"
            login = True
            return data, "Success"
    except FileNotFoundError:
        login = True
        with open(data_file, 'wb') as fp:
            encrypt = cryptor.encrypt("", password)
            write_pw_file(encrypt)
        return {}, "New data file created. The new password file will reside in the current directory and is called 'my_manager.dat'"
    except AssertionError as error:
        print(error)
        return {}, "Maybe wrong password ". error


def write_pw_file(data):
    try:
        with open(data_file, "wb") as cf:
            cf.write(data)
    except:
        print("Error while writing to file!")


def append_data(password, data, res, pword, res_url = "", user=""):
    if data == "":
        this_dict = {}
        this_dict[res] = {"URL": res_url, "User": user, "Password": pword}
        data = this_dict
    else:
        data[res] = {"URL": res_url, "User": user, "Password": pword}
    data_to_ecrypt = json.dumps(data)
    encrypt = cryptor.encrypt(data_to_ecrypt, password)
    write_pw_file(encrypt)

def edit_data(password, data, res, pword, res_url = "", user=""):
    if res == "":
        print("no data to edit")
    else:
        data.update({res : {"URL": res_url, "User": user, "Password": pword}})
    data_to_ecrypt = json.dumps(data)
    encrypt = cryptor.encrypt(data_to_ecrypt, password)
    write_pw_file(encrypt)

def delete_data(password, data, res):
    if res == "":
        print("No data")
    else:
        data.pop(res)
    data_to_ecrypt = json.dumps(data)
    encrypt = cryptor.encrypt(data_to_ecrypt, password)
    write_pw_file(encrypt)

def update_list(password):
    file, msg = open_pw_file(password)
    rlist = []
    for key, value in file.items():
        rlist.append(key)
    return msg, rlist, file


###
# Layout format used by PySimpleGUI
###

# Get default vars
ready, sub_pass = startup_check()

file_list_column = [
    [
        sg.Text("Search access: "),
        sg.In(size=(20, 1), enable_events=True, key="-SEARCH-"),
    ],
    [
        sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-LIST-")
    ],
]

image_viewer_column = [
    [sg.Text(ready, size=(60, 2), key="heading")],
    [sg.Text("Account name:", key="acc_name", size=(30, 1), text_color="gray", visible=False), sg.Text('', size=(30, 2), key="-account-", visible=False)],
    [sg.Text("URL:", key="url_name", size=(30, 1), text_color="gray", visible=False), sg.InputText('', size=(30, 2), key="-url-", visible=False)],
    [sg.Text("Username:", key="usr_name", size=(30, 1), text_color="gray", visible=False), sg.InputText('', size=(30, 2), key="-user-", visible=False)],
    [sg.Text("Password:", key="pas_name", size=(30, 1), text_color="gray", visible=False), sg.InputText('', size=(30, 2), key="-pass-", text_color='black', background_color='white', visible=False)],
    [sg.Submit('Delete Record', key="delete_rec"), sg.Submit('Edit Record', key="edit_rec")],
    [sg.Submit('Login', key="mas_pass")],
]


top_row2 = [
    [sg.Text("New resource name:", key="new_ressource_text"), sg.InputText('', key="-NRESSOURCE-", size=(10, 1)),
     sg.Text("URL:", key="new_ressource_url"), sg.InputText('', key="-NRESURL-", size=(10, 1)),
     sg.Text("Username:", key="username_text"), sg.InputText('', key="-NUSER-", size=(10, 1)),
     sg.Text("Password", key="new_pass_text"), sg.InputText('', key="-NPASS-", size=(10, 1)),
     sg.Submit('Add new', key="add_button")]
]

# ----- Full layout -----
layout = [
        [
            sg.Column(top_row2, key="top_bar2", size=(760, 35), visible=False)
        ],
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column)],
    ]

window = sg.Window("Python Password Manager", layout)

# GUI function to change layout when logged in
def login_true():
        window["heading"].update("Welcome")
        window["top_bar2"].update(visible=True)

def remove_acc_fields():
        window['acc_name'].update(visible=False)
        window['url_name'].update(visible=False)
        window["usr_name"].update(visible=False)
        window['pas_name'].update(visible=False)
        window['-account-'].update(visible=False)
        window['-url-'].update(visible=False)
        window['-user-'].update(visible=False)
        window['-pass-'].update(visible=False)
        window['delete_rec'].update(visible=False)
        window['edit_rec'].update(visible=False)
        window['mas_pass'].update(visible=False)

def show_acc_fields():
        window['acc_name'].update(visible=True)
        window['url_name'].update(visible=True)
        window["usr_name"].update(visible=True)
        window['pas_name'].update(visible=True)
        window['-account-'].update(visible=True)
        window['-url-'].update(visible=True)
        window['-user-'].update(visible=True)
        window['-pass-'].update(visible=True)
        window['delete_rec'].update(visible=True)
        window['edit_rec'].update(visible=True)



while True:
    event, values = window.read()
    if login:
        login_true()
        remove_acc_fields()
    else:
        text = ready + '\n' + sub_pass
        password = sg.popup_get_text(text, password_char='*')
        msg, file, full_dict = update_list(password)
        if login:
            login_true()
            window["-LIST-"].update(file)
            window['delete_rec'].update(visible=False)
            window['edit_rec'].update(visible=False)
            window['mas_pass'].update(visible=False)
        window["heading"].update(msg)

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == 'delete_rec':
        text = "You are about to delete record:"
        rec = values["-LIST-"][0]
        print(rec)
        if sg.popup_get_text(text, default_text=rec):
            delete_data(password, full_dict, rec)
            msg, file, full_dict = update_list(password)
            window["-LIST-"].update(file)

    if event == 'edit_rec':
        text = "You are about to delete record:"
        rec = values["-LIST-"][0]
        print(rec, values['-url-'], values['-user-'])
        edit_data(password, full_dict, rec, values['-pass-'], values['-url-'], values['-user-'])
        msg, file, full_dict = update_list(password)
        window["-LIST-"].update(file)
        window["heading"].update("Record changed!")

    if event == 'add_button':
        try:
            append_data(password, full_dict, values['-NRESSOURCE-'], values['-NPASS-'], values['-NRESURL-'], values['-NUSER-'])
            msg, file, full_dict = update_list(password)
            window["heading"].update("Data appended!")
            remove_acc_fields()
            window["-LIST-"].update(file)
            window["-NRESSOURCE-"].update('')
            window["-NUSER-"].update('')
            window["-NRESURL-"].update('')
            window["-NPASS-"].update('')
        except:
            window["heading"].update("Error while adding")
    # Search for account
    if event == "-SEARCH-":
        term = values["-SEARCH-"]
        try:
            new_values = [x for x in file if term in x]
        except:
            new_values = file

        window["-LIST-"].update(new_values)

    elif event == "-LIST-":  # A row was chosen from the listbox
        try:
            account = values["-LIST-"][0]
            url = full_dict[account]['URL']
            ruser = full_dict[account]['User']
            rpass = full_dict[account]['Password']
            window["heading"].update("Resource info:")
            window["-account-"].update(account)
            window["-url-"].update(url)
            window["-user-"].update(ruser)
            window["-pass-"].update(rpass)
            show_acc_fields()
        except:
            pass

window.close()
