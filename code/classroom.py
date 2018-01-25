#!/usr/bin/python
# -*- coding: utf-8 -*-
# Please open readme.txt for information regarding using this program

""" This script is intended for use as a classroom tool.
Prerequiites:
    * Rename `check_in_out.txt` to `borrowed_log.txt`
    * Rename `all_qrs.txt` to `all_qrs.json`
    * Rename `borrowed_items.txt` to `borrowed_items.json`
    * Run `convert_students.py` and follow it's instructions

To use it, run on a command line:
    $ python classroom.py

If python is not in your path, this command will not work.
In that case the word python should be replaced by your system's
path for your installation of Python 3.6.4.

Todo:
    * User action frame implementation.
    * Accurate and informative comments and Docstrings.
    * Full testing for bugs.
    * Overal vetting of code.
        - Code style.
        - Performance checking.
        - Minification(to a seperate file).
        - Splitting this script into more modules.

"""

# Import Statements

from tkinter import * # Tkinter is a gui library.
import json # Allows more proper file manipulation.
import time

# Import Module Dependencies

from CreateFrame import CreateFrame # A Tkinter frame.

# Global Variables(default at this level)
students = {}
all_qrs = []
items = {}
br_pass_IDs = []
ticket_IDs = []
used_IDs = []
used_tickets = []
checked_out_tickets = {}
unused_tickets = []
used_br_pass = []
checked_out_br_passes = {}
unused_br_pass = []
used_items = []
options = None
qrid = ''
submitted = None

# Convert files into dictonaries
with open("./json/students.json", "r") as f:
    students = json.load(f)

with open("./json/all_qrs.json", "r") as f:
    all_qrs = json.load(f)

with open("./json/items.json", "r") as f:
    items = json.load(f)

    bathroom_passes = items["bathroom_passes"]
    # keys, values = dictonary.items() will not work in this case because
    # unpacking the keys and values when the diconary is empty errors.
    checked_out_br_passes = bathroom_passes["checked_out"]
    used_br_pass = list(checked_out_br_passes.keys())
    br_pass_IDs = list(checked_out_br_passes.values())

    unused_br_pass = bathroom_passes["available"]

    tickets = items["tickets"]
    checked_out_tickets = tickets["checked_out"]
    used_tickets = list(checked_out_tickets.keys())
    ticket_IDs = list(checked_out_tickets.values())
    unused_tickets = tickets["available"]

    used_IDs = br_pass_IDs + ticket_IDs

tk = Tk()
tk.state("zoomed") # Full Screen mode
tk.resizable(0, 0) # Don't allow resizing
pad = 3
tk.geometry(
    "{0}x{1}+0+0".format(
        tk.winfo_screenwidth() - pad,
        tk.winfo_screenheight() - pad
    )
) # Set the geometry size to the screen size
tk.grid_columnconfigure(0, weight=1) # Fill width, to center content horizontally

tk.title("QrClassroom")
tk.iconbitmap("./images/qr_code.ico")

# Begin Program
def main():
    """Create the main login page."""

    global qrid
    global submitted

    submitted = False

    scan_qr = CreateFrame(tk)
    text = scan_qr.add_text(
        label="Scan Science ID QR code",
        font=("Times New Roman", 20),
        pady=10,
        columnspan=2
    )
    qr_code_input = scan_qr.add_input(
        callback=lambda qrid: submit_qr(scan_qr, qrid, error_text),
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
        callback=lambda: submit_qr(scan_qr, qr_code_input.get("1.0", "end-1c"), error_text),
        row=1,
        column=1,
        padx=3,
        sticky=W
    )

    scan_qr.create()

def submit_qr(frame, student_qrid, error_text):
    """Submit the qr code.

    Arguments:
        frame {CreateFrame} -- The source frame that has to be cleared.
        student_qrid {Integer} -- The student QR ID code
        error_text {String} -- The passed in error.
    """

    global qrid
    global all_qrs

    qrid = student_qrid
    if qrid not in all_qrs:
        if qrid == "":
            error_text.config(text="Please scan Your Science ID")
        else:
            error_text.config(text="Invalid ID. Please rescan Your Science ID")
    else:
        frame.destroy()
        if qrid not in students:
            add_user()
        else:
            User_Actions()

def add_user():
    """Add a user."""

    add_user_frame = CreateFrame(tk)
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
    first_name.bind(
        "<FocusOut>",
        lambda event: Check_User_Errors(first_name, last_name, period_number, error_text)
    )
    first_name.bind(
        "<KeyRelease>",
        lambda event: Check_User_Errors(first_name, last_name, period_number, error_text) if event.keysym not in ("Tab", "Shift_L", "Shift_R") else None
    )

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
    last_name.bind(
        "<FocusOut>",
        lambda event: Check_User_Errors(first_name, last_name, period_number, error_text)
    )
    last_name.bind(
        "<KeyRelease>",
        lambda event: Check_User_Errors(first_name, last_name, period_number, error_text) if event.keysym not in ("Tab", "Shift_L", "Shift_R") else None
    )

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
    period_number.bind(
        "<Return>",
        lambda event: Create_User(add_user_frame, first_name, last_name, period_number, error_text)
    )

    error_text = add_user_frame.add_text("", color="red", sticky=W, font=("Times New Roman", 12))

    submit_button = add_user_frame.add_button(
        "Submit",
        lambda: Create_User(add_user_frame, first_name, last_name, period_number, error_text),
        sticky=W
    )

    Create_Back(frame=add_user_frame)
    add_user_frame.create()

def Create_User(add_user_frame, first_name, last_name, period_number, error_text):
    """Add a user.
    
    Arguments:
        add_user_frame {CreateFrame} -- The previous frame to clear.
        first_name {String} -- The user's first name.
        last_name {String} -- The user's last name.
        period_number {Integer} -- The user's period.
        error_text {String} -- Any errors.
    """

    global submitted
    global qrid
    global students

    submitted = True
    error = Check_User_Errors(first_name, last_name, period_number, error_text)

    if error is None:
        first_name_text = first_name.get("1.0", "end-1c")
        last_name_text = last_name.get("1.0", "end-1c")
        period_number_text = period_number.get()

        user_dict = {
            "first_name": first_name_text,
            "last_name": last_name_text,
            "period": period_number_text
        }

        students[qrid] = user_dict

        with open("./json/students.json", "w+") as f:
            f.write(json.dumps(students, indent=4))

        add_user_frame.destroy()
        User_Actions()

def User_Actions():
    """The available actions."""

    global qrid
    global students

    student = students.get(qrid)
    actions_frame = CreateFrame(tk)

    first_name, last_name, period = student.values()

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
        lambda: submit_action(actions, action_text, error_text),
        sticky=E
    )

    actions_button = actions_frame.add_button(
        label="Submit",
        callback=lambda: submit_action(actions, action_text, error_text),
        sticky=W,
        row=2,
        column=1
    )

    actions.bind("<FocusIn>", lambda event: actions.config(bg="white"))
    actions.bind("<FocusOut>", lambda event: Check_Action_Errors(actions.get("1.0", "end-1c"), error_text))
    actions.bind("<KeyRelease>", lambda event: Check_Action_Errors(actions.get("1.0", "end-1c"), error_text) if event.keysym not in ("Tab", "Shift_L", "Shift_R") else None)

    actions.focus()

    error_text = actions_frame.add_text("", color="red", sticky=W, font=("Times New Roman", 12))

    action_text = actions_frame.add_text("")
    action_text.config(wraplength=125)

    Create_Back(frame=actions_frame)
    actions_frame.create()

# This function has not been fully tested.
def submit_action(actions, action_text, error_text):
    """Run the possible actions.
    
    Arguments:
        actions {tkText} -- The text input for the actions.
        action_text {String} -- The action input.
        error_text {String} -- Any previous errors.
    """

    global qrid
    global students
    global used_IDs

    goto_main_screen = False
    action_result = None
    error = Check_Action_Errors(actions.get("1.0", "end-1c"), error_text)

    if error != None:
        return

    action = actions.get("1.0", "end-1c")
    actions.config(bg="white")
    error_text.config(text="")

    localtime = time.asctime(time.localtime(time.time()))

    student = students.get(qrid)
    first_name, last_name, period = student.values()
    period = int(period)

    student_info = f"{first_name} {last_name}(period {period})"

    if action[0] == "(":
        global br_pass_IDs

        borrow = action

        # "(" it is an item to be checked (in or out) to a valid qr id user

        # if name and item checked out, check it in.
        # elif name and item not linked, checkout item
        # else item not checked in and is being checked out

        if borrow in used_items and qrid in br_pass_IDs:

            used_IDs.remove(qrid)
            used_items.remove(borrow)

            with open("./logs/borrowed_log.txt", "a+") as f:
                f.write(f"{student_info}, returned {borrow} on {localtime}\n")

            action_result = f"{student_info} returned {borrow} on {localtime}\n"
        elif borrow in used_items and qrid not in {used_IDs, }:
            action_error = "This item has already been checked out.\n"
        elif borrow not in used_items and qrid not in used_IDs:

            used_IDs.append(qrid)
            used_items.append(borrow)
            with open("./logs/borrowed_log.txt", "a+") as f:
                f.write(f"{student_info} checked out {borrow} on {localtime}\n")

            action_result = f"You checked out {borrow}"

    # ifthe qr code starts with "#" it is an interactive notebook code

    if action[0] == "#":
        global used_tickets
        global unused_tickets
        global checked_out_tickets

        ticket = "%s INB ticket" % action.strip()
        tickets = items["tickets"]
        
        used_tickets = list(checked_out_tickets.keys())
        ticket_IDs = list(checked_out_tickets.values())
        if ticket in unused_tickets:
            tickets["checked_out"][ticket] = qrid
            
            used_tickets.append(ticket)
            unused_tickets.remove(ticket)
            
            ticket_IDs.append(qrid)

            with open("./logs/INB_work_log.txt", "a+") as f:
                f.write(f"{first_name} did work on {localtime} ({ticket})\n")

            action_result = f"You did work on {ticket}\n"

            items["tickets"] = tickets
            checked_out_tickets = tickets["checked_out"]

            with open("./json/items.json", "w+") as f:
                f.write(json.dumps(items, indent=4))
        elif ticket in used_tickets:
            if qrid in ticket_IDs:
                del tickets["checked_out"][ticket]
                ticket_IDs.remove(qrid)

                used_tickets.remove(ticket)
                unused_tickets.append(ticket)

                action_result = f"You checked in {ticket}\n"
                checked_out_tickets = tickets["checked_out"]
                with open("./json/items.json", "w+") as f:
                    f.write(json.dumps(items, indent=4))
            else:
                action_result = "INB ticket has been used."
        else:
            action_result = "INB ticket is not valid."


    # if the qr code starts with ")" it a bathroom pass QR code
    if action[0] == ")":
        br_pass = action.strip()
        global used_br_pass
        global unused_br_pass

        bathroom_passes = items["bathroom_passes"]
        unused_br_pass = bathroom_passes["available"]
        used_br_pass = list(bathroom_passes["checked_out"].keys())
        br_pass_IDs = list(bathroom_passes["checked_out"].values())
        br_ID = action[1:]
        br_pass = ") bathroom pass #" + br_ID

        if br_pass in unused_br_pass:
            bathroom_passes["checked_out"][br_pass] = qrid
            bathroom_passes["available"].remove(br_pass)

            used_br_pass.append(br_pass)

            with open("./logs/bathroom_in_out.txt", "a+") as f:
                f.write(f"{first_name} {last_name}(period {period}) left on {localtime} with {br_pass}.\n")

            action_result = f"You checked out at {localtime} with {br_pass}.\n"
            goto_main_screen = True
        elif br_pass in used_br_pass:
            del bathroom_passes["checked_out"][br_pass]
            bathroom_passes["available"].append(br_pass)

            used_br_pass.remove(br_pass)

            with open("./logs/bathroom_in_out.txt", "a+") as f:
                f.write(f"{first_name} {last_name}(period {period}) returned on {localtime} with {br_pass}.\n")

            action_result = f"You returned {br_pass}.\n"
        else:
            action_error = f"Invalid bathroom pass."

        items["bathroom_passes"] = bathroom_passes

        with open("./json/items.json", "w+") as f:
            f.write(json.dumps(items, indent=4))

    # if the qr code starts with "!" it is an admin code

    # This admin function is to re-activate used tickets

    if action[0] == "!":
        while action[0] == "!":
            renew = input("Reactivate used tickets now.  When done scan Purple Admin QR code")
            if renew in used_tickets:
                used_tickets.remove(renew)
                unused_tickets.append(renew)
                action_result = "Ticket\t {renew} is ready for reuse.\nUsed tickets are: {used_ticket}"

            #if renew == str("! Teacher Administrator"):
            #    Main()

    if action_result != None:
        action_text.config(text=action_result)

def Check_User_Errors(first_name, last_name, period_number, error_text):
    """Check for invalid inputs.
    
    Arguments:
        first_name {String} -- The user's first name.
        last_name {String} -- The user's last name.
        period_number {Integer} -- The user's period number.
        error_text {String} -- Any previous errors.
    
    Returns:
        String -- Any errors
    """

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
    """Check for any invalid inputs.
    
    Arguments:
        action {String} -- The action text.
        error_text {String} -- The error text.
    
    Returns:
        String -- Any errors
    """

    error = None

    if action == None or action == "":
        error = "Please input Action Card."
        return error

    if action[0] not in {"!", "(", "#", ")"}:
        error = "Invalid Action Card."

    error_text.config(text=error)
    return error

def Create_Back(frame=None):
    """Create a back button.
    
    Keyword Arguments:
        frame {CreateFrame} -- The frame to clear (default: {None})
    """

    global options

    if options == None:
        options = CreateFrame(tk)
        options.place(x=0)
        back_arrow = PhotoImage(file="./images/back_arrow.png")
        back_button = options.add_button(
            label="",
            callback=lambda: Back(frame),
            image=back_arrow
        )
        back_button.image = back_arrow

def Back(frame=None):
    """The callback function.
    
    Keyword Arguments:
        frame {CreateFrame} -- The frame to clear (default: {None})
    """

    global options

    if frame != None:
        frame.destroy()
    options.destroy()
    options = None
    main()

def natural_sort(string_):
    """Sort a list with with "natural" sorting.
    
    Arguments:
        string_ {String} -- an element of the list.
    
    Returns:
        String -- the parsed string
    """

    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

#testing purposes
if __name__ == "__main__":
    main()
