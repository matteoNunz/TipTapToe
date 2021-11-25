"""
Date: 25/11/2021
Author: Matteo Nunziante

Description: Tip Tap Toe game

Example of reinforcement learning applied to a game:
    -> it's possible to train 2 players (one that start first and one that start for second)
    -> the training can be between the 2 artificial player and also during the game with a human player
"""

import pickle
from pathlib import Path

import numpy as np


class Player:
    def __init__(self, name, symbol):
        """
        Initialize name and symbol of the player
        :param name: name of the player
        :param symbol: symbol of the player: 'X' if first player, 'O' otherwise
        """
        self.name = name
        self.symbol = symbol

    def setName(self , name):
        """
        Set the name of the player
        :param name: the name of the player
        :return: nothing
        """
        self.name = name

    def addState(self, state):
        pass

    def feedReward(self, reward):
        pass

    def reset(self):
        pass


class ArtificialPlayer(Player):

    def __init__(self, name, symbol, exp_rate=0.4):
        """
        Initialize the artificial player
        :param name: name of the player
        :param symbol: symbol of the player
        :param exp_rate: constant indicating the probability of performing a random action
        """
        super().__init__(name, symbol)
        self.states = []  # To save all positions taken
        self.states_value = {}  # State -> value
        # Epsilon-greedy method to balance between exploration and exploitation
        self.exp_rate = exp_rate
        self.lr = 0.5  # learning rate
        self.gamma = 0.9

    def getHash(self, board, board_rows=3, board_cols=3):
        """
        Get the hash of a board
        :param board: the board of whom calculate the hash
        :param board_rows: number of rows in the board
        :param board_cols: number of columns in the board
        :return: the hah of the board
        """
        boardHash = str(board.reshape(board_rows * board_cols))
        return boardHash

    def chooseAction(self, positions, board):
        """
        Method that chooses the action of the artificial player:
            - random action (40% of the actions during the training game , never otherwise)
            - action related to his experience
        :param positions: is a list containing all the positions in which is possible perform an action
        :param board: is the board of the game
        :return: a tuple containing the coordinates of the board on which do the action (add the symbol of the player)
        """
        if np.random.uniform(0, 1) < self.exp_rate:
            # Take a random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            # If start action, choose the best one
            if (1, 1) in positions:
                action = (1, 1)
                return action
            # Evaluating what the player learned until now
            valueMax = -999
            action = None
            for p in positions:
                # Make a copy of the board
                next_board = board.copy()
                # Add the symbol in a possible position
                next_board[p] = self.symbol
                # Take the next board hash
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None \
                    else self.states_value.get(next_boardHash)
                # print("Value: " , value)
                if value >= valueMax:
                    valueMax = value
                    action = p
        # print("{} takes action {}".format(self.name, action))
        return action

    def addState(self, state):
        """
        Add the new state in the list
        :param state: is the new state after the action
        :return: nothing
        """
        self.states.append(state)

    def feedReward(self, reward):
        """
        Back propagation of the reward received during the current game
        :param reward: is the reward sent after the end of the game accordingly to the result
        :return: nothing
        """
        for state in reversed(self.states):
            # If it's a new state never visited before
            if self.states_value.get(state) is None:
                self.states_value[state] = 0
            # Update the existing value using reinforcement learning formula
            self.states_value[state] = (1 - self.lr) * self.states_value[state] \
                                       + self.lr * (reward + self.gamma * self.states_value[state])

    def reset(self):
        """
        Reset the states of the current game for the next game
        :return: nothing
        """
        self.states = []

    def savePolicy(self):
        """
        Method that saves the new updated policy of the player
        :return: nothing
        """
        print("Saving configuration...")
        file = open('Files/policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, file)
        file.close()
        print("Configuration saved!")

    def loadPolicy(self, f):
        """
        Method that loads the policy of the player before starting the game
        :param f: is the path of the file
        :return: nothing
        """
        print("Loading policy...")
        if Path(f).is_file():
            file = open(f, 'rb')
            self.states_value = pickle.load(file)
            file.close()
            print("Policy loaded")
        else:
            print("Error in uploading the policy")


class HumanPlayer(Player):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)

    def chooseAction(self, positions):
        """
        Method that asks the HumanPlayer to choose the board's coordinates on which perform the action
        :param positions: is the list with all the available positions
        :return: the action chose -> a tuple containing the coordinates the player chose
        """
        while True:
            try:
                row = int(input("Input your action row: "))
                col = int(input("Input your action col: "))
                if type(row) != int or type(col) != int:
                    raise Exception()
            except Exception:
                print("Wrong format, insert again!")
                continue

            action = (row, col)
            if action in positions:
                return action
