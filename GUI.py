"""
Date: 21/10/2021
Author: Matteo Nunziante

Description: GUI for Tip Tap Toe game
"""

import tkinter as tk


class GUI:
    def __init__(self):
        # Create the main window
        self.mainWindow = tk.Tk()
        # Set the title
        self.mainWindow.title = 'Tip Tap Toe Game'
        # Set the size of the window
        self.mainWindow.geometry("400x200")
        # Add widgets
        # Add a label
        self.label = tk.Label(self.mainWindow , text = "Click the button to increase the count!")
        # Add a button: window , text, callBack function
        self.button = tk.Button(self.mainWindow , text = "0" , command = self.randomFunction)
        # Add a menu
        self.menu = tk.Menu(self.mainWindow)
        self.mainWindow.config(menu = self.menu)
        self.fileMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label = "Menu" , menu = self.fileMenu)
        self.fileMenu.add_command(label = "New game" , command = self.reset)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Quit" , command = self.mainWindow.quit)
        self.helpMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label = "Help" , menu = self.helpMenu)
        self.helpMenu.add_command(label = "Info" , command = self.info)
        # Add a message
        self.message = tk.Message(self.mainWindow , text = "Limit reached (10)! Reset the game to play again!" ,
                                  foreground = "red" , width = 300)

        # Prepare the temporary button and label to be shown when the user select 'Help'
        self.temporaryLabel = tk.Label(self.mainWindow , text = "Go to 'Menu -> New game' to start a new game of "
                                                                "Tip Tap Toe!")
        self.temporaryButton = tk.Button(self.mainWindow , text = "Back" , command = self.back)

        # Show the main widgets
        self.label.pack()  # To show the label
        self.button.pack()  # To show the button
        self.mainWindow.mainloop()

    def randomFunction(self):
        num = int(self.button['text'])
        if num == 10:
            self.message.pack()
            return
        self.button['text'] = str(num + 1)

    def reset(self):
        self.button['text'] = str(0)
        self.message.pack_forget()

    def info(self):
        # Hide the main widgets
        self.label.pack_forget()
        self.button.pack_forget()
        # Show the help label and button
        self.temporaryLabel.pack()
        self.temporaryButton.pack()

    def back(self):
        # Hide the help label and button
        self.temporaryLabel.pack_forget()
        self.temporaryButton.pack_forget()
        # Show the main widgets
        self.label.pack()
        self.button.pack()


if __name__ == '__main__':
    gui = GUI()
