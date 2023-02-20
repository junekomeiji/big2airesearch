import os
import sys

playernum = int(sys.argv[1]) # accepts an int representing the player to be checked (0-3)
filenames = ["player1", "player2", "player3", "player4"]

playerfile = open(filenames[playernum])
thing = playerfile.readline()
cards = thing.split(',')

