import tkinter
from tkinter import *

# Tkinter Wrapper Class to simplify later code
class CreateFrame(Frame):
    """Creates a object-oriented wrapper for Tkinter's functions."""
    def __init__(self, root):
        Frame.__init__(self, root)
    def add_input(self, callback, font=("Garamond", 12), width=15, height=1, **args):
        """Create a Tkinter Text widget

        Arguments:
            callback {Function} -- A callback function for when the user submits the input.
            font {Tuple(String, Integer)} -- The font name and font size for the input text.

        Keyword Arguments:
            width {Integer} -- The width of the input widget. (default: {15})
            height {Integer} -- The height of the input widget. (default: {1})
            **args {Any} -- Text.grid arguments.

        Returns:
            tkText -- A Tkinter Text widget.
        """

        text = Text(self, font=font, width=width, height=height)
        text.grid(args)
        text.bind("<Return>", lambda event: self.__submit(callback, text))
        text.bind("<Shift-Tab>", self.__focus_prev)
        text.bind("<Tab>", self.__focus_next)
        return text
    def add_button(self, label, callback, image=None, **args):
        """Create a Tkinter Button widget

        Arguments:
            label {String} -- The button's text.
            callback {Function} -- The function to run when the button is pressed.

        Keyword Arguments:
            image {String} -- A path to an image for the button. (default: {None})
            **args {Any} -- Button.grid options.

        Returns:
            tkButton -- A Tkinter Button arguments.
        """


        button = Button(self, text=label, command=callback, image=image)
        button.grid(args)
        return button
    def add_text(self, label, color="black", font=("Garmond", 13), **args):
        """Create a Tkinter Label widget.

        Arguments:
            label {String} -- The text that will be displayed

        Keyword Arguments:
            color {String} -- The color the text will be. (default: {"black"})
            font {Tuple(String, Integer)} -- The font name and font size for the input text.
            **args {Any} -- Label.grid arguments.

        Returns:
            tkLabel -- A Tkinter Label widget.
        """

        text = Label(self, text=label, fg=color, font=font)
        text.grid(args)
        return text
    def add_option(self, from_, to, state="readonly", width=18, borderwidth=2, wrap=True, **args):
        """Create a Tkinter Spinbox widget with customized focus events.

        Arguments:
            from_ {Integer} -- The lower bound the value can go to.
            to {Integer} -- The upper bound the value can go to.

        Keyword Arguments:
            state {String} -- The  (default: {"readonly"})
            width {Integer} -- The width of the widget. (default: {18})
            borderwidth {Integer} -- The border width of the widget. (default: {2})
            wrap {Boolean} --  (default: {True})
            **args {Any} -- Spinbox.grid arguments.

        Returns:
            tkSpinbox -- A Tkinter Spinbox widget
        """

        option = Spinbox(self, from_=from_, to=to, state=state, width=width, bd=borderwidth, wrap=wrap)
        option.config(command=option.focus)
        if state == "readonly":
            default_color = option.cget("readonlybackground")
            option.bind("<FocusIn>", lambda event: option.config(readonlybackground="GhostWhite"))
            option.bind("<FocusOut>", lambda event: option.config(readonlybackground=default_color))
        option.grid(**args)
        return option
    def add_image(self, file):
        """Creates a Tkinter PhotoImage widget.

        Arguments:
            file {String} -- The path to the image.

        Returns:
            tkPhotoImage -- A Tkinter PhotoImage widget.
        """

        photo = PhotoImage(file=file)
        return photo
    def create(self):
        """Create and display the frame."""
        self.grid(padx=10, pady=10)
        self.place(anchor="c", relx=0.5, rely=0.5)
        Frame.mainloop(self)
    def destroy(self):
        """Remove the frame."""
        Frame.destroy(self)
    def __focus_prev(self, event):
        """Focus the previous widget.

        Arguments:
            event {tkEvent} -- A generic Tkinter event.

        Returns:
            "Break" -- Stops the default event's action.
        """

        event.widget.tk_focusPrev().focus()
        return "break"
    def __focus_next(self, event):
        """Focus the next widget.

        Arguments:
            event {tkEvent} -- A generic Tkinter event.

        Returns:
            "break" -- Stops the default event's action.
        """

        event.widget.tk_focusNext().focus()
        return "break"
    def __submit(self, callback, text):
        """Calls a callback function with.

        Arguments:
            callback {Function} -- The function to run.
            text {tkLabel} -- The source widget.

        Returns:
            "break" -- Stops the default event's action.
        """

        if callback.__code__.co_argcount == 1:
            callback(text.get(1.0, "end-1c"))
        else:
            callback()
        return "break"
