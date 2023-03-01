import os
import sys
import globals as gl

def SingleHands(beat, card):
    hands = []
    if beat == '-1':
        for cd in card:
            hand = [cd]
            hands.append(hand)
    else:
        for cd in card:
            if cd > beat:
                hand = [cd]
                hands.append(hand)
            
def PairHands(beat, card):
    hands = []
    if beat == '-1':
        for x in range (1,14):
            elig = []
            for cd in cards:
                if gl.cardpowerdict[cd] % 14 == x:
                    
                    
        
playernum = 1 #testing
#playernum = int(sys.argv[1]) # accepts an int representing the player to be checked (0-3)
filenames = ["player1", "player2", "player3", "player4"]
os.chdir("saved_data")

playerfile = open(filenames[playernum])
thing = playerfile.readline()
cards = thing.split(',')

playerfile.readline()
playedCard = playerfile.readline()
playedHand = playedCard.split(',')

""" if playedHand[0] == '-1': """
if len(playedHand) == 1:
    SingleHands(playedHand[0], cards)