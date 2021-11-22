"""
Date: 21/10/2021
Author: Matteo Nunziante

Description: GUI for Tip Tap Toe game
"""
from pathlib import Path

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, StringVar, OptionMenu, END, Message, Frame
from PIL import Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./Files/Images")


def relative_to_assets(path: str) -> Path:
    """
    Method that rebuilds the path of all the pictures
    :param path: picture name
    :return: complete path
    """
    return ASSETS_PATH / Path(path)


class GUI:
    def __init__(self):
        # Create the main window
        self.mainWindow = Tk()
        # Set the title
        self.mainWindow.title('Tip Tap Toe Game')
        # Take the position in the middle of the screen
        screenPositionRight = int(self.mainWindow.winfo_screenwidth() / 2 - 700 / 2)
        screenPositionDown = int(self.mainWindow.winfo_screenheight() / 2 - 500 / 2)
        # Set the size of the window and its position
        self.mainWindow.geometry("550x550" + "+{}+{}".format(screenPositionRight, screenPositionDown))

        # Create the workspace
        self.canvas = Canvas(
            self.mainWindow,
            height = 550,
            width = 550,
            bd = 0,
            bg="#FAF8F5",
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(
            x = 0 ,
            y = 0
        )

        # List of elements in the page
        self.elementsInThePage = []

        # Variable that contains the error, if there is one
        self.error = None

        # Initialize the starting page
        self.init_starting_page()

    def showError(self):
        """
        Method that shows the error
        :return: nothing
        """
        errorMessage = Message(
            self.mainWindow ,
            text = self.error ,
            width = 200,
            foreground = "red"
        )
        errorMessage.place(
            x = 225 ,
            y = 475
        )
        self.elementsInThePage.append(errorMessage)

    def init_starting_page(self):
        """
        Method that inits the starting page
        :return: nothing
        """

        if self.error is not None:
            self.showError()

        welcomeMessage = Message(
            self.mainWindow ,
            text = "Welcome in Tip Tap Toe Game!" ,
            width = 200
        )
        welcomeMessage.place(
            x = 180 ,
            y = 30
        )

        self.elementsInThePage.append(welcomeMessage)

        # Create the image of the starting phase
        image = PhotoImage(
            file = relative_to_assets("tris_image.png")
        )

        self.canvas.create_image(
            120 ,
            90 ,
            image = image ,
            anchor = "nw"
        )

        # Create the entry for the player's name under the image
        nameMessage = Message(
            self.mainWindow ,
            width = 50 ,
            text = "Name:"
        )
        nameMessage.place(
            x = 190 ,
            y = 450
        )

        self.elementsInThePage.append(nameMessage)

        nameEntry = Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0
        )
        nameEntry.place(
            x = 270 ,
            y = 450 ,
            width = 91.0 ,
            height = 17.0
        )

        self.elementsInThePage.append(nameEntry)

        # Add the start game button
        startGame_button = Button(
            borderwidth = 100 ,
            highlightthickness = 0 ,
            text = "Start Game" ,
            command = lambda: self.startGame(nameEntry) ,
            relief = "flat"
        )
        startGame_button.place(
            x = 220 ,
            y = 500 ,
            width = 114 ,
            height = 30
        )

        self.elementsInThePage.append(startGame_button)

        self.mainWindow.mainloop()

    def startGame(self , nameEntry):
        """
        Method called clicking on startGame_button in the starting page
        If the user inserted the name, the game will start , otherwise show the error
        :return: nothing
        """
        # Get the name inserted before deleting the elements
        name = nameEntry.get()

        # Delete elements in the current page
        self.canvas.delete("all")
        for el in self.elementsInThePage:
            el.destroy()

        # Check if the name is valid, otherwise show an error
        if name is None or not name:
            self.error = "Insert your name!"
            self.init_starting_page()
            return
        self.error = None
        print("Name inserted: " , name)

        # Create the game board
        self.printInitialBoard()

    def printInitialBoard(self , player1 = None , player2 = None):

        cell00 = Button(
            borderwidth = 70 ,
            highlightthickness = 3,
            relief = "flat"
        )
        cell00.place(
            x = 220 ,
            y = 150 ,
            width = 50 ,
            height = 47
        )
        self.elementsInThePage.append(cell00)

        cell01 = Button(
            borderwidth = 100 ,
            highlightthickness = 0 ,
            relief = "flat"
        )
        cell01.place(
            x = 270 ,
            y = 150 ,
            width = 50 ,
            height = 47
        )
        self.elementsInThePage.append(cell01)

        cell02 = Button(
            borderwidth = 100 ,
            highlightthickness = 0 ,
            relief = "flat"
        )
        cell02.place(
            x = 320 ,
            y = 150 ,
            width = 50 ,
            height = 47
        )
        self.elementsInThePage.append(cell02)

        cell10 = Button(
            borderwidth = 100 ,
            highlightthickness = 0 ,
            relief = "flat"
        )
        cell10.place(
            x = 220 ,
            y = 197 ,
            width = 50 ,
            height = 47
        )
        self.elementsInThePage.append(cell10)

        cell11 = Button(
            borderwidth = 100 ,
            highlightthickness = 0 ,
            relief = "flat"
        )
        cell11.place(
            x = 270 ,
            y = 197 ,
            width = 50 ,
            height = 47
        )
        self.elementsInThePage.append(cell11)

        cell12 = Button(
            borderwidth = 100 ,
            highlightthickness = 0 ,
            relief = "flat"
        )
        cell12.place(
            x = 320 ,
            y = 197 ,
            width = 50 ,
            height = 47
        )
        self.elementsInThePage.append(cell12)

        cell20 = Button(
            borderwidth = 100 ,
            highlightthickness = 0 ,
            relief = "flat"
        )
        cell20.place(
            x = 220 ,
            y = 244 ,
            width = 50 ,
            height = 47
        )
        self.elementsInThePage.append(cell20)

        cell21 = Button(
            borderwidth = 100 ,
            highlightthickness = 0 ,
            relief = "flat"
        )
        cell21.place(
            x = 270 ,
            y = 244 ,
            width = 50 ,
            height = 47
        )
        self.elementsInThePage.append(cell21)

        cell22 = Button(
            borderwidth = 100 ,
            highlightthickness = 0 ,
            relief = "flat"
        )
        cell22.place(
            x = 320 ,
            y = 244 ,
            width = 50 ,
            height = 47
        )
        self.elementsInThePage.append(cell22)


if __name__ == '__main__':
    gui = GUI()
