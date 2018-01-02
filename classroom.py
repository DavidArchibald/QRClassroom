#!/usr/bin/python
# -*- coding: utf-8 -*-
# Please open readme.txt for information regarding using this program

# Import Statements

import tkinter # Tkinter is a gui library.
from tkinter import *
import ast # Ast includes a safer version of eval(ast.literalEval) that doesn't allow malicous code.
import time

# Variables Defined

global students
global useditem
global all_used_items
global per_num
global br_pass
global submitted
global options

# lists defined

ID_list = []
useditem = []
all_used_items = []
usedticket = []
qr_ID_unused = []
qr_ID_new = []
list_borrow = []
usedID = []
used_qr_codes = []
assigned_qr_codes = []
lst_name = []
item_from_dict = []

unused_br_pass = [
    ") bathroom pass #1",
    ") bathroom pass #2",
    ") bathroom pass #3"
]
used_br_pass = []

# dictionaries defined

students = {}
my_atten_dict = {}
dict_in_out = {}
dict_qr_whom = {}
dict_qr_who = {}
qr_to_who_dict = {}
qr_to_whom_dict = {}
item_out_to_name_dict = {}
students_item_to_name = {}
item_from_dict = []
qr_to_pn_dict = {}

time_start_MTHF_dict = {
    "per_1": "8:30",
    "per_2": "10:08",
    "per_3": "12:20",
    "per_4": "1:58",
    "per_5": "8:30",
    "per_6": "10:08",
    "per_7": "12:20",
    "per_8": "1:58",
}

time_end_MTHF_dict = {
    "per_1": "10:02",
    "per_2": "11:44",
    "per_3": "1:52",
    "per_4": "3:30",
    "per_5": "10:02",
    "per_6": "11:44",
    "per_7": "1:52",
    "per_8": "3:30",
}

time_start_W_dict = {
    "per_1": "9:00",
    "per_2": "10:31",
    "per_3": "12:34",
    "per_4": "3:30",
    "per_5": "9:00",
    "per_6": "10:31",
    "per_7": "12:34",
    "per_8": "3:30",
}

time_end_W_dict = {
    "per_1": "10:25",
    "per_2": "11:58",
    "per_3": "1:59",
    "per_4": "3:30",
    "per_5": "10:25",
    "per_6": "11:58",
    "per_7": "1:59",
    "per_8": "3:30",
}

options = None

# Convert files into dictonaries
with open("./all_qrs.txt", "r") as inf:
    all_qrs = ast.literal_eval(inf.read())

with open("./unusedticket.txt", "r") as inf:
    unusedticket = ast.literal_eval(inf.read())

with open("./students.txt", "r") as inf:
    students = ast.literal_eval(inf.read())


# Tkinter Wrapper Class to simplify later code
class Create_Frame(Frame):
    def __init__(self, root): #, title=None, icon=None):
        Frame.__init__(self, root)
        #if title != None:
        #    self.winfo_toplevel().title(title)
        #if icon != None:
        #    root.iconbitmap(icon)
    def add_input(self, callback, font=("Garamond", 12), width=15, height=1, **args):
        text = Text(self, font=font, width=width, height=height)
        text.grid(args)
        text.bind("<Return>", lambda event: self.submit(callback, text))
        text.bind("<Shift-Tab>", self.focus_prev)
        text.bind("<Tab>", self.focus_next)
        return text
    def add_button(self, label, callback, image=None, **args):
        button = Button(self, text=label, command=callback, image=image)
        button.grid(args)
        return button
    def add_text(self, label, color="black", font=("Garmond", 13), **args):
        text = Label(self, text=label, fg=color, font=font)
        text.grid(args)
        return text
    def add_option(self, from_, to, state="readonly", width=18, borderwidth=2, wrap=True, **args):
        option = Spinbox(self, from_=from_, to=to, state=state, width=width, bd=borderwidth, wrap=wrap, command=lambda: option.focus())
        if state == "readonly":
            default_color = option.cget("readonlybackground")
            option.bind("<FocusIn>", lambda event: option.config(readonlybackground="GhostWhite"))
            option.bind("<FocusOut>", lambda event: option.config(readonlybackground=default_color))
        option.grid(**args)
        return option
    def add_image(self, file, **args):
        photo = PhotoImage(file=file)
        return photo
    def focus_prev(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"
    def focus_next(self, event):
        event.widget.tk_focusNext().focus()
        return "break"
    def submit(self, callback, text):
        if callback.__code__.co_argcount == 1:
            callback(text.get(1.0, "end-1c"))
        else:
            callback()
        return "break"
    def create(self):
        self.grid(padx=10, pady=10)
        self.place(anchor="c", relx=0.5, rely=0.5)
        Frame.mainloop(self)
    def destroy(self):
        Frame.destroy(self)

root = Tk()
root.state("zoomed") # Full Screen mode
root.resizable(0,0) # Don't allow resizing
pad = 3
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth() - pad, root.winfo_screenheight() - pad)) # Set the geometry size to the screen size
root.grid_columnconfigure(0, weight=1) # Fill width, to center content horizontally

root.title("QrClassroom")
root.iconbitmap("qr_code.ico")

# Begin Program
def Main():
    global used_qr_ID
    global qrid
    global pn    
    global get_index
    global submitted

    submitted = False

    scan_qr = Create_Frame(root)
    text = scan_qr.add_text(
        label="Scan Science ID QR code",
        font=("Times New Roman", 20),
        pady=10,
        columnspan=2
    )
    qr_code_input = scan_qr.add_input(
        callback=lambda qrid: Submit_Qr(scan_qr, qrid, error_text),
        width=20,
        sticky=E
    )
    qr_code_input.focus()

    error_text = scan_qr.add_text(
        "",
        color="red",
        font=("Times New Roman", 12),
        sticky=W,
        columnspan=4
    )
    submit = scan_qr.add_button(
        label="Submit",
        callback=lambda: Submit_Qr(scan_qr, qr_code_input.get("1.0", "end-1c"), error_text),
        row=1,
        column=1,
        padx=3,
        sticky=W
    )

    scan_qr.create()

def Submit_Qr(frame, student_qrid, error_text):
    global qrid

    qrid = student_qrid
    if qrid not in all_qrs:
        if qrid == "":
            error_text.config(text="Please scan Your Science ID")
        else:
            error_text.config(text="Invalid ID. Please rescan Your Science ID")
    else:
        frame.destroy()
        if qrid not in students:
            Add_User()
        else:
            User_Actions()

def Add_User():
    add_user_frame = Create_Frame(root)
    add_user_frame.add_text(
        "You're a first time user, please input some details to get started",
        columnspan=2
    )

    first_name_label = add_user_frame.add_text(
        "First Name: ",
        sticky=E
    )

    first_name = add_user_frame.add_input(
        lambda text: Create_User(add_user_frame, first_name, last_name, period_number, error_text),
        sticky=W,
        row=1,
        column=1
    )
    first_name.focus()

    first_name.bind("<FocusIn>", lambda event: first_name.config(bg="white"))
    first_name.bind("<FocusOut>", lambda event: Check_User_Errors(first_name, last_name, period_number, error_text))
    first_name.bind("<KeyRelease>", lambda event: Check_User_Errors(first_name, last_name, period_number, error_text) if event.keysym not in ("Tab", "Shift_L", "Shift_R") else None)

    last_name_label = add_user_frame.add_text(
        "Last Name: ",
        sticky=E
    )

    last_name = add_user_frame.add_input(
        lambda text: Create_User(add_user_frame, first_name, last_name, period_number, error_text),
        sticky=W,
        row=2,
        column=1
    )
    last_name.bind("<FocusIn>", lambda event: last_name.config(bg="white"))
    last_name.bind("<FocusOut>", lambda event: Check_User_Errors(first_name, last_name, period_number, error_text))
    last_name.bind("<KeyRelease>", lambda event: Check_User_Errors(first_name, last_name, period_number, error_text) if event.keysym not in ("Tab", "Shift_L", "Shift_R") else None)

    period_number_label = add_user_frame.add_text(
        "Period Number: ",
        sticky=E
    )

    period_number = add_user_frame.add_option(
        from_=1,
        to=8,
        sticky=W,
        row=3,
        column=1
    )
    period_number.bind("<Return>", lambda event: Create_User(add_user_frame, first_name, last_name, period_number, error_text))

    error_text = add_user_frame.add_text("", color="red", sticky=W, font=("Times New Roman", 12))

    submit_button = add_user_frame.add_button(
        "Submit",
        lambda: Create_User(add_user_frame, first_name, last_name, period_number, error_text),
        sticky=W
    )

    Create_Back(frame=add_user_frame)
    add_user_frame.create()

def Create_User(add_user_frame, first_name, last_name, period_number, error_text):
    global submitted
    global qrid

    submitted = True
    error = Check_User_Errors(first_name, last_name, period_number, error_text)

    if error == None:
        first_name_text = first_name.get("1.0", "end-1c")
        last_name_text = last_name.get("1.0", "end-1c")
        period_number_text = period_number.get()

        user_dict = {
            "first_name": first_name_text,
            "last_name": last_name_text,
            "period": period_number_text
        }

        students[qrid] = user_dict

        f = open("./students.txt", "w+")
        f.write(str(students))
        f.close()

        add_user_frame.destroy()
        User_Actions()

def User_Actions():
    global qrid
    global students

    student = students.get(qrid)
    actions_frame = Create_Frame(root)

    first_name = student["first_name"]
    last_name = student["last_name"]
    period = student["period"]

    
    title_text = actions_frame.add_text(
        "Your Account",
        font=("Times New Roman", 20),
        pady=10,
        columnspan=2
    )
    #body_text = actions_frame.add_text(
    #    f"Welcome {first_name} {last_name} period number {period}.\nIf your details are incorrect contact your teacher. ",
    #    font=("Garmond",12),
    #    columnspan=2
    #)


    actions_label = actions_frame.add_text(
        "Action: ",
        sticky=W
    )

    actions = actions_frame.add_input(
        lambda: Submit_Action(actions, error_text),
        sticky=E
    )
    
    actions_button = actions_frame.add_button(
        label="Submit",
        callback=lambda: Submit_Action(actions, error_text),
        sticky=W,
        row=2,
        column=1
    )

    actions.bind("<FocusIn>", lambda event: actions.config(bg="white"))
    actions.bind("<FocusOut>", lambda event: Check_Action_Errors(actions.get("1.0", "end-1c"), error_text))
    actions.bind("<KeyRelease>", lambda event: Check_Action_Errors(actions.get("1.0", "end-1c"), error_text) if event.keysym not in ("Tab", "Shift_L", "Shift_R") else None)

    actions.focus()

    error_text = actions_frame.add_text("", color="red", sticky=W, font=("Times New Roman", 12))

    Create_Back(frame=actions_frame)
    actions_frame.create()

# This function has not been fully tested.
def Submit_Action(actions_frame, actions, error_text):
    global qrid
    global students

    error = Check_Action_Errors(actions, error_text)

    if(error != None):
        return
    
    action = actions.get("1.0", "end-1c")
    actions.config(bg="white")
    error_text.config(text="")


    if action[0] == "(":
        borrow = action
        localtime = time.asctime(time.localtime(time.time()))

        # "(" it is an item to be checked (in or out) to a valid qr id user

        # if name and item checked out, check it in.
        # elif name and item not linked, checkout item
        # else item not checked in and is being checked out

        if borrow in useditem and qrid in usedID:

            usedID.remove(qrid)
            useditem.remove(borrow)
            name = str(students.get(qrid))

            f = open("./borrowed_log.txt", "a+")
            f.write(f"{name}, returned {borrow} on {localtime}\n")
            f.close()

            action_result = f"{name} returned {borrow} on {localtime}\n"
        elif borrow in useditem and qrid not in usedID:
            action_result = "This item was not checked in yet, see instructor\n"
        else:

            usedID.append(qrid)
            useditem.append(borrow)
            name = students.get(qrid)
            f = open("./borrowed_log.txt", "a+")
            f.write(f"{student_text} checked out {borrow} on {localtime}\n")
            f.close()

            action_result = f"You checked out {borrow} on {localtime}\n"

    # if the qr code starts with "#" it is an interactive notebook code

    if action[0] == "#":
        ticket = action        
        localtime = time.asctime(time.localtime(time.time()))

        student = students.get(qrid)

        if ticket in unusedticket:
            usedticket.append(ticket)
            unusedticket.remove(ticket)

            f = open("./INB_work.txt", "a+")
            f.write(f"{name} did work on {localtime} ({ticket})\n")
            f.close()
            action_result = f"You did work on {localtime} ({ticket})\n"
        else:
            ticket in usedticket
            action_result  = "INB ticket is not valid and has already been used"

    # if the qr code starts with "$" it is an attendance code

    if action[0] == "$":        
        localtime = time.asctime(time.localtime(time.time()))

        action_result = f"You arrived on: {localtime}\n"

        f = open("./attendance.txt", "a+")
        f.write(f"You arrived on: {localtime} \n")
        f.close()

    # if the qr code starts with "@" it a bathroom pass QR code

    if action[0] == ")":
        br_pass = action

        # print(
        #   f"got br_pass, unused_br_pass, used _br_pass coded as )\
        #   {br_pass} {unused_br_pass} {used_br_pass}"
        # )

        localtime = time.asctime(time.localtime(time.time()))

        if str(br_pass) in str(unused_br_pass):
            used_br_pass.append(br_pass)
            unused_br_pass.remove(br_pass)

            f = open("./bathroom_in_out.txt", "a+")
            f.write(f"{student_text} left on {localtime} with {used_br_pass}\n")
            f.close()

            action_result = f"You left on {localtime} with {used_br_pass}\n"
        elif str(br_pass) in str(used_br_pass):

            f = open("./bathroom_in_out.txt", "a+")
            f.write(f"{name} returned on {localtime} with {used_br_pass}\n")
            f.close()

            action_result = f"{name} returned on {localtime} with {used_br_pass}\n"

            used_br_pass.remove(br_pass)
            unused_br_pass.append(br_pass)

    # if the qr code starts with "!" it is an admin code

    # This admin function is to re-activate used tickets

    if action[0] == "!":
        localtime = time.asctime(time.localtime(time.time()))

        while action[0] == "!":
            renew = input("Reactivate used tickets now.  When done scan Purple Admin QR code")
            if renew in usedticket:
                usedticket.remove(renew)
                unusedticket.append(renew)
                action_result = f"Ticket\t {renew} is ready for reus.\nUsed tickets are: {usedticket}"

            #if renew == str("! Teacher Administrator"):
            #    Main()
    
    if action_result != None:
        action_text = actions_frame.add_text(
            action_result
        )
        Main()

def Check_User_Errors(first_name, last_name, period_number, error_text):
    global submitted

    if submitted == False:
        return

    first_name_text = first_name.get("1.0", "end-1c")
    last_name_text = last_name.get("1.0", "end-1c")
    period_number_text = period_number.get()

    error = None

    if first_name_text == "":
        first_name.config(bg="red")
        error = "Please fill in all fields."
    else:
        first_name.config(bg="white")

    if last_name_text == "":
        last_name.config(bg="red")
        error = "Please fill in all fields."
    else:
        last_name.config(bg="white")

    if period_number_text == "":
        period_number.config(bg="red")
        error = "Please fill in all fields."
    else:
        period_number.config(bg="white")
    
    error_text.config(text=error or "")
    return error

def Check_Action_Errors(action, error_text):
    error = None

    if action == None or action == "":
        error = "Please input Action Card."
        return error

    if action[0] not in ("$", "!", "(", "#", ")"):
        error = "Invalid Action Card."
    
    error_text.config(text=error or "")
    return error

def Create_Back(frame=None):
    global options

    if options == None:
        options = Create_Frame(root)
        options.place(x=0)
        back_arrow = PhotoImage(file="back_arrow.png")
        back_button = options.add_button(
            label="",
            callback=lambda: Back(frame),
            image=back_arrow
        )
        back_button.image=back_arrow

def Back(frame=None):
    global options

    if frame != None:
        frame.destroy()
    options.destroy()
    options = None
    Main()

#testing purposes
if __name__ == "__main__":
    Main()
