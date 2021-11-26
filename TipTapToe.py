"""
Date: 25/11/2021
Author: Matteo Nunziante

Description: Tip Tap Toe game

Example of reinforcement learning applied to a game:
    -> it's possible to train 2 players (one that start first and one that start for second)
    -> the training can be between the 2 artificial player and also during the game with a human player
"""
import sys

import numpy as np

from pathlib import Path

from numpy.random import rand

from Enumerations import CellState, GameState

from Player import ArtificialPlayer, HumanPlayer

from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Message , Menu

# Dimension of the game board
BOARD_COLS = 3
BOARD_ROWS = 3

# For rebuild the path of the images
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./Files/Images")

# Starting coordinates of the board in the gui
X_ZERO_POSITION = 160
Y_ZERO_POSITION = 150

# Dimension of each button (cell) in the gui
DIM_CELL_X = 75
DIM_CELL_Y = 75


def relative_to_assets(path: str) -> Path:
    """
    Method that rebuilds the path of all the pictures
    :param path: picture name
    :return: complete path
    """
    return ASSETS_PATH / Path(path)


class Client:

    def showBoard(self):
        """
        Method that shows the game board
        :return: nothing
        """
        pass

    def showResult(self , message):
        """
        Print the result of the game
        :param message: is the message to print (with the winner)
        :return: nothing
        """
        pass


class GUI(Client):
    def __init__(self , g , w):

        # Save the game
        self.game = g

        # Create the main window
        self.mainWindow = w

        # Create the workspace
        self.canvas = Canvas(
            self.mainWindow,
            height=550,
            width=550,
            bd=0,
            bg="#FAF8F5",
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(
            x=0,
            y=0
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
            self.mainWindow,
            text=self.error,
            width=200,
            foreground="red",
            bg = "#FAF8F5"
        )
        errorMessage.place(
            x=225,
            y=475
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
            self.mainWindow,
            text="Welcome in Tip Tap Toe Game!",
            bg="#FAF8F5",
            width=200
        )
        welcomeMessage.place(
            x=180,
            y=30
        )

        self.elementsInThePage.append(welcomeMessage)

        self.canvas.create_image(
            120,
            90,
            image=tris_image,
            anchor="nw"
        )

        # Create the entry for the player's name under the image
        nameMessage = Message(
            self.mainWindow,
            width=50,
            bg="#FAF8F5",
            text="Name:"
        )
        nameMessage.place(
            x=190,
            y=450
        )

        self.elementsInThePage.append(nameMessage)

        nameEntry = Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )
        nameEntry.place(
            x=270,
            y=450,
            width=91.0,
            height=17.0
        )

        self.elementsInThePage.append(nameEntry)

        # Add the start game button
        startGame_button = Button(
            borderwidth=100,
            highlightthickness=0,
            text="Start Game",
            command=lambda: self.startGame(nameEntry),
            relief="flat"
        )
        startGame_button.place(
            x=220,
            y=500,
            width=114,
            height=30
        )

        self.elementsInThePage.append(startGame_button)

    def startGame(self, nameEntry):
        """
        Method called clicking on startGame_button in the starting page
        If the user inserted the name, the game will start , otherwise show the error
        :return: nothing
        """
        # Get the name inserted before deleting the elements
        nameInserted = nameEntry.get()

        # Delete elements in the current page
        self.canvas.delete("all")
        for i in range(len(self.elementsInThePage)):
            self.elementsInThePage[i].destroy()
        self.elementsInThePage = []

        # Check if the name is valid, otherwise show an error
        if nameInserted is None or not nameInserted:
            self.error = "Insert your name!"
            self.init_starting_page()
            return
        self.error = None

        # print("Name inserted: ", nameInserted)

        # Update the name of the human player
        if type(self.game.player1) == HumanPlayer:
            self.game.player1.name = nameInserted
        else:
            self.game.player2.name = nameInserted

        # Stop the mainloop
        mainWindow.quit()

    def showBoard(self):
        """
        Print the board
        :return: nothing
        """
        # Stop the previous mainloop
        mainWindow.quit()

        # Delete all the previous elements
        for i in range(len(self.elementsInThePage)):
            self.elementsInThePage[i].destroy()
        self.elementsInThePage = []

        # Show the error if present
        if self.error is not None:
            self.showError()

        # Build the message with players and their symbols
        messageToShow = str(game.player1.name) + "(X)      VS      " + str(game.player2.name) + "(O)"

        infoMessage = Message(
            self.mainWindow,
            text=messageToShow,
            font="Helvetica 12 bold",
            width=400,
            foreground="black",
            bg = "#FAF8F5"
        )
        infoMessage.place(
            x=160,
            y=40
        )
        self.elementsInThePage.append(infoMessage)

        # Build the board with CellButton elements
        for row in range(len(self.game.board)):
            for col in range(len(self.game.board[0])):
                cell = CellButton(self, row, col, self.game.board[row][col])
                self.elementsInThePage.append(cell)

    def actionChose(self, x, y):
        """
        Method called when a button cell is clicked
        :param x: is the coordinate x of the button in the board
        :param y: is the coordinate y of the button in the board
        :return: nothing
        """
        if self.game is not None:
            self.error = self.game.setActionChose(x, y)
            # If the action was valid
            if self.error is None:
                mainWindow.quit()
            else:
                self.showBoard()
                mainWindow.mainloop()

    def showResult(self , message):
        mainWindow.quit()
        resultMessage = Message(
            self.mainWindow,
            text=message,
            font="Helvetica 12 bold",
            width=200,
            foreground="red",
            bg = "#FAF8F5"
        )
        resultMessage.place(
            x=230,
            y=475
        )
        self.elementsInThePage.append(resultMessage)


class CellButton:
    def __init__(self, gui, x, y, cellSymbol):
        """
        Initialize the object CellButton
        :param gui: is the gui in which the object is
        :param x: is the x position of the button in the board
        :param y: is the y position of the button in the board
        :param cellSymbol: is the value of the cell corresponding to the button
        """
        self.x = x
        self.y = y
        self.gui = gui

        if cellSymbol == CellState.X_Value:
            self.symbol = "X"
        elif cellSymbol == CellState.O_Value:
            self.symbol = "O"
        else:
            self.symbol = ""

        self.cell = Button(
            borderwidth=2,
            highlightthickness=3,
            relief="solid",
            text = self.symbol,
            font = "bold",
            command=lambda: self.gui.actionChose(self.x, self.y)
        )
        self.cell.place(
            x=X_ZERO_POSITION + x * DIM_CELL_X,
            y=Y_ZERO_POSITION + y * DIM_CELL_Y,
            width=DIM_CELL_X,
            height=DIM_CELL_Y
        )

    def destroy(self):
        """
        Method used to destroy the CellButton object as it was a tkinter object
        :return: nothing
        """
        self.cell.destroy()


class CLI(Client):
    def __init__(self , g):
        self.game = g

    def showBoard(self):
        """
        Print the board in the command line
        :return: nothing
        """
        for i in range(0, len(self.game.board)):
            print('-------------')
            out = '| '
            for j in range(0, len(self.game.board[0])):
                if self.game.board[i, j] == CellState.X_Value:
                    token = 'x'
                elif self.game.board[i, j] == CellState.O_Value:
                    token = 'o'
                else:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')

    def showResult(self , message):
        print(message)


class Game:
    def __init__(self, p1, p2):
        """
        Initialize the game
        :param p1: fist player -> the one that will do the first move (X)
        :param p2: second player (O)
        """
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.player1 = p1
        self.player2 = p2
        self.isEnd = False
        # Init player1 plays first
        self.activePlayer = self.player1

        self.actionChose = None

    def getHash(self):
        """
        :return: the hash of the current board
        """
        boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS))
        return boardHash

    def availablePositions(self):
        """
        Check which positions are available
        :return: a list containing all the available position for perform an action
        """
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i , j] == CellState.empty_Value:
                    # Append the tuple
                    positions.append((i , j))
        return positions

    def updateState(self , position):
        """
        Add the value of the player (his symbol)
        :param position: position chose to perform the action
        :return: nothing
        """
        self.board[position] = int(self.activePlayer.symbol)

    def updateActivePlayer(self):
        """
        Update the active player
        :return: nothing
        """
        if self.activePlayer is self.player1:
            self.activePlayer = self.player2
        else:
            self.activePlayer = self.player1

    def winner(self):
        """
        Check the board and search for end game conditions
        :return: a GameState value referred to the first player (self.player1)
        """
        # Rows
        for i in range(BOARD_ROWS):
            if sum(self.board[i , :]) == BOARD_COLS:
                self.isEnd = True
                return GameState.WIN
            if sum(self.board[i , :]) == -BOARD_ROWS:
                self.isEnd = True
                return GameState.LOOSE

        # Columns
        for i in range(BOARD_COLS):
            if sum(self.board[: , i]) == BOARD_COLS:
                self.isEnd = True
                return GameState.WIN
            if sum(self.board[: , i]) == -BOARD_COLS:
                self.isEnd = True
                return GameState.LOOSE

        # Diagonals
        diag1_sum = sum([self.board[i , i] for i in range(BOARD_COLS)])
        diag2_sum = sum([self.board[i, BOARD_COLS - i - 1] for i in range(BOARD_COLS)])
        diag_sum_max = max(abs(diag1_sum) , abs(diag2_sum))

        if diag_sum_max == 3:
            self.isEnd = True
            if diag1_sum == BOARD_COLS or diag2_sum == BOARD_COLS:
                return GameState.WIN
            else:
                return GameState.LOOSE

        # Tie -> no available position
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return GameState.DRAW

        # Not end
        self.isEnd = False
        return GameState.UNDEFINED

    def giveRewards(self):
        """
        According to the result send the reward to the player in  the game
        :return: nothing
        """
        result = self.winner()
        # Back propagate rewards
        if result == GameState.WIN:
            self.player1.feedReward(2)
            self.player2.feedReward(-1)
        elif result == GameState.LOOSE:
            self.player1.feedReward(-5)
            self.player2.feedReward(5)
        else:
            self.player1.feedReward(-0.5)
            self.player2.feedReward(0.5)

    def reset(self):
        """
        Reset the variable to start a new game
        :return: nothing
        """
        self.board = np.zeros((BOARD_ROWS , BOARD_COLS))
        self.isEnd = False
        self.activePlayer = self.player1

    def play(self , client , rounds = 100):
        """
        Method that handles the game both in case of ArtificialPlayer against artificialPlayer and
            ArtificialPlayer against HumanPlayer
        :param client: generic client for the interaction with the user (cli or gui)
        :param rounds: number of game to play in case of training games
        :return: nothing
        """
        if type(self.player1) == ArtificialPlayer and type(self.player2) == ArtificialPlayer:
            # If training play
            for i in range(rounds):
                while not self.isEnd:
                    # Take the available positions
                    positions = self.availablePositions()
                    # Choose the action
                    action = self.activePlayer.chooseAction(positions , self.board)
                    # Update the board
                    self.updateState(action)
                    self.activePlayer.addState(self.getHash())

                    # Check if the active player won
                    winner = self.winner()
                    if winner is not GameState.UNDEFINED:
                        # The game ended with win or tie
                        self.giveRewards()
                        self.player1.reset()
                        self.player2.reset()
                        self.reset()
                        break
                    else:
                        # Update the active player for the next turn
                        self.updateActivePlayer()
        else:
            # If the is a humanPlayer
            while not self.isEnd:
                # Take the available positions
                positions = self.availablePositions()
                if type(self.activePlayer) == HumanPlayer:
                    if type(client) == CLI:
                        client.showBoard()
                        action = self.activePlayer.chooseAction(positions)
                    else:
                        client.showBoard()
                        # Update the window
                        mainWindow.mainloop()

                        if self.actionChose == "exit":
                            return

                        # Read the action chose and reset it for the next turn
                        action = self.actionChose
                        self.actionChose = None
                else:
                    # If artificial player
                    action = self.activePlayer.chooseAction(positions , self.board)
                # Update the board
                self.updateState(action)

                # Check if the active player won
                winner = self.winner()
                if winner is not GameState.UNDEFINED:
                    client.showBoard()
                    if winner is GameState.WIN:
                        message = str(self.player1.name) + " won!"
                    elif winner is GameState.LOOSE:
                        message = str(self.player2.name) + " won!"
                    else:
                        message = "Tie!"
                    # Show the result on the client (cli or gui)
                    client.showResult(message)
                    if type(client) == GUI:
                        # If gui, update the window to visualize the message
                        mainWindow.mainloop()
                    # Back propagate the reward
                    self.giveRewards()
                    break
                else:
                    # Update the active player for the next turn
                    self.updateActivePlayer()

    def setActionChose(self , x , y):
        """
        Method called by the GUI when the player selects a position(an action)
        :param x: is the coordinate x chose
        :param y: is the coordinate y chose
        :return: None if the position is valid, an string error otherwise
        """
        positions = self.availablePositions()
        if (x , y) in positions:
            self.actionChose = (x , y)
        else:
            self.actionChose = None
            return "Invalid position"


def start_game():
    """
    Method called for starting a re-starting the game
    :return: nothing
    """
    # If the game is already started
    if game.player1.name != "" and game.player2.name != "":
        game.player1.reset()
        game.player2.reset()
        game.reset()
        game.play(client)


def exit_game():
    """
    Method called when the user select the "Exit" option from the Menu
    :return: nothing
    """
    game.actionChose = "exit"
    mainWindow.destroy()


def on_quit():
    """
    Method called when the window is closed
    :return: nothing
    """
    exit()


if __name__ == '__main__':

    # Read the input arguments to decide if gui, cli or training (plus how many training game)
    if len(sys.argv) > 1 and sys.argv[1] == "gui":
        withGui = True
        training = False
    elif len(sys.argv) > 1 and sys.argv[1] == "training":
        withGui = False
        training = True
        try:
            # If it's a integer
            numberOfGames = int(sys.argv[2])
        except :
            numberOfGames = 1000
    else:
        withGui = False
        training = False

    if training:
        """Training Mode"""
        player1 = ArtificialPlayer("U-0318", CellState.X_Value)
        player2 = ArtificialPlayer("U-0314", CellState.O_Value)

        # If the file exists, upload it
        my_file = Path("Files/policy_U-0318")
        if my_file.is_file():
            player1.loadPolicy("Files/policy_U-0318")
        # If the file exists, upload it
        my_file = Path("Files/policy_U-0314")
        if my_file.is_file():
            player2.loadPolicy("Files/policy_U-0314")

        # Create the game
        game = Game(player1, player2)

        print("Training...")
        game.play(numberOfGames)

        # Save the configurations
        player1.savePolicy()
        player2.savePolicy()
    else:
        """With Human Player Mode"""
        if withGui:
            # The name will be set later through the GUI
            name = ""
        else:
            print("Tic Tac Toe!")
            name = input("Insert your name: ")
            print("Starting the game...")

        # Choose randomly the first player
        if rand() < 0.5:
            player1 = ArtificialPlayer("U-0318" , CellState.X_Value , 0)
            player2 = HumanPlayer(name , CellState.O_Value)
            player1.loadPolicy("Files/policy_U-0318")
            if not withGui:
                print("Your symbol is: O")
        else:
            player1 = HumanPlayer(name, CellState.X_Value)
            player2 = ArtificialPlayer("U-0314" , CellState.O_Value , 0)
            player2.loadPolicy("Files/policy_U-0314")
            if not withGui:
                print("Your symbol is: X")

        # Create and start the game
        game = Game(player1 , player2)

        if withGui:
            # Create the main window
            mainWindow = Tk()
            # Set the title
            mainWindow.title('Tip Tap Toe Game')
            # Take the position in the middle of the screen
            screenPositionRight = int(mainWindow.winfo_screenwidth() / 2 - 700 / 2)
            screenPositionDown = int(mainWindow.winfo_screenheight() / 2 - 500 / 2)
            # Set the size of the window and its position
            mainWindow.geometry("550x550" + "+{}+{}".format(screenPositionRight, screenPositionDown))
            # Set the window not resizable
            mainWindow.resizable(False , False)

            # Create the image of the starting phase
            tris_image = PhotoImage(
                file=relative_to_assets("tris_image.png")
            )

            client = GUI(game , mainWindow)

            # Add menu to the window
            menubar = Menu(mainWindow)
            fileMenu = Menu(menubar, tearoff=0)
            # Add the "New Game" option
            fileMenu.add_command(label="New Game", command= lambda : start_game())

            fileMenu.add_separator()

            # Add the "Exit" option
            fileMenu.add_command(label="Exit", command= lambda : exit_game())

            menubar.add_cascade(label="File", menu=fileMenu)
            mainWindow.config(menu=menubar)

            # Set the action in case of closure -> close the entire application
            mainWindow.protocol("WM_DELETE_WINDOW", on_quit)

            # Start the GUI
            mainWindow.mainloop()
        else:
            client = CLI(game)

        # Start the game
        start_game()


        """
        Uncomment to train the algorithm when it's playing with you
        # Save the result of the game with the human player
        if type(player1) == ArtificialPlayer:
            player1.savePolicy()
        else:
            player2.savePolicy()
        """

