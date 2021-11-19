"""
Date: 21/10/2021
Author: Matteo Nunziante

Description: Tip Tap Toe game
"""
from pathlib import Path

import numpy as np

from numpy.random import rand

from Enumerations import CellState, GameState
from Player import ArtificialPlayer, HumanPlayer

BOARD_COLS = 3
BOARD_ROWS = 3


class Game:
    def __init__(self, p1, p2):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.player1 = p1
        self.player2 = p2
        self.isEnd = False
        self.boardHash = None
        # Init player1 plays first
        self.activePlayer = self.player1

    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS))
        return self.boardHash

    def availablePositions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i , j] == CellState.empty_Value:
                    # Append the tuple
                    positions.append((i , j))
        return positions

    def updateState(self , position):
        # Add the value of the player
        self.board[position] = int(self.activePlayer.symbol)

    def updateActivePlayer(self):
        # Update the active player
        if self.activePlayer is self.player1:
            self.activePlayer = self.player2
        else:
            self.activePlayer = self.player1

    def winner(self):
        """
        The return value are referred to the player with X_Value (player1)
        :return:
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
            self.player2.feedReward(1)

    def reset(self):
        self.board = np.zeros((BOARD_ROWS , BOARD_COLS))
        self.boardHash = None
        self.isEnd = False
        self.activePlayer = self.player1

    def play(self , rounds = 100):
        if type(self.player1) == ArtificialPlayer and type(self.player2) == ArtificialPlayer:
            # If training play
            for i in range(rounds):
                if i % 1000 == 0:
                    print("Rounds {}".format(i))
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
                    self.showBoard()
                    action = self.activePlayer.chooseAction(positions)
                else:
                    action = self.activePlayer.chooseAction(positions , self.board)
                # Update the board
                self.updateState(action)

                # Check if the active player won
                winner = self.winner()
                if winner is not GameState.UNDEFINED:
                    self.showBoard()
                    if winner is GameState.WIN:
                        print(str(self.player1.name) + " won!")
                    elif winner is GameState.LOOSE:
                        print(str(self.player2.name) + " won!")
                    else:
                        print("Tie!")
                    # Back propagate the reward
                    self.giveRewards()
                    break
                else:
                    # Update the active player for the next turn
                    self.updateActivePlayer()

    def showBoard(self):
        for i in range(0, BOARD_ROWS):
            print('-------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == CellState.X_Value:
                    token = 'x'
                if self.board[i, j] == CellState.O_Value:
                    token = 'o'
                if self.board[i, j] == CellState.empty_Value:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')


if __name__ == '__main__':
    print("Tic Tac Toe!")

    training = False

    if training:
        """Training Mode"""
        for _ in range(100):
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

            game = Game(player1, player2)

            print("Training...")
            game.play(50)

            # Save the configuration
            player1.savePolicy()
            player2.savePolicy()

            """

            player1 = ArtificialPlayer("ArtificialSlave", CellState.X_Value)
            player2 = ArtificialPlayer("ArtificialMaster", CellState.O_Value)

            # If the file exists, upload it
            my_file = Path("Files/policy_ArtificialMaster")
            if my_file.is_file():
                player2.loadPolicy("Files/policy_ArtificialMaster")

            game = Game(player1, player2)

            print("Training...")
            game.play(50)

            # Save the configuration
            player2.savePolicy()
            """
    else:
        """With Human Player Mode"""
        name = input("Insert your name: ")
        print("Starting the game...")

        if rand() < 0.5:
            player1 = ArtificialPlayer("U-0318" , CellState.X_Value , 0)
            player2 = HumanPlayer(name , CellState.O_Value)
            player1.loadPolicy("Files/policy_U-0318")
            print("Your symbol is: " + str(player2.symbol))
        else:
            player1 = HumanPlayer(name, CellState.X_Value)
            player2 = ArtificialPlayer("U-0314" , CellState.O_Value , 0)
            player2.loadPolicy("Files/policy_U-0314")
            print("Your symbol is: " + str(player1.symbol))

        game = Game(player1 , player2)
        game.play()

        # Save the result of the game with the human player
        if type(player1) == ArtificialPlayer:
            player1.savePolicy()
        else:
            player2.savePolicy()

