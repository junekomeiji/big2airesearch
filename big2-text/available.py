import os
import sys
import globals as gl
import itertools as iter

def HighestCard(hand):
    power = -1
    for cd in hand:
        if gl.cardpowerdict[cd] > power:
            power = gl.cardpowerdict[cd]
    return power

def SingleHands(beat, card):
    """Returns a list of single card hands with a higher power.

    Args:
        beat (int): The value of the card to beat.
        card (string[]): The cards available in hand.

    Returns:
        string[[]]: A nested list containing all valid single card hands.
    """
    hands = []
    if beat == -1:
        for cd in card: # adds every card as a single hand
            hand = [cd]
            hands.append(hand)
    else:
        for cd in card:
            if gl.cardpowerdict[cd] > beat: # compares the currents card with each card in hand, adds as a single hand if larger
                hand = [cd]
                hands.append(hand)
    return hands
            
def SameHands(beat, card, match):
    """Returns a list of pairs with a higher power.

    Args:
        beat (int): The power of the pair to beat. (value of the highest card)
        card (string[]): The cards available in hand.
        match (int): The number of cards to match (2 is a pair, 3 is a three of a kind, etc.)

    Returns:
        string[[]]: A nested list containing all valid hands.
    """
    hands = []
    if beat == -1:
        for x in range (13): # iterates through every card type
            elig = []
            for cd in cards: # checks through each card in hand if it is the same card type, adds to eligible cards if true
                if gl.cardpowerdict[cd] % 13 == x:
                    elig.append(cd)
            if len(elig) > match - 1: # if there is at least one hand, create list of all hand, add each hand to hands
                for hand in list(iter.combinations(elig,match)):
                    hands.append(hand)
    else: #first check for pairs of same type, then of larger types
        elig_same = []
        for cd in cards:
            if gl.cardpowerdict[cd] % 13 == beat % 13:
                elig_same.append(cd)
        if len(elig_same) > match - 1:
            for hand in list(iter.combinations(elig_same,match)):
                bigger_power = False
                for cd in hand: # checks if the hand is bigger than the current hand (possibility for optimization?)
                    if gl.cardpowerdict[cd] > beat:
                        bigger_power = True
                if bigger_power:
                    hands.append(hand)
        for x in range(beat+1, 13): # cards of higher power (a repeat of the -1 case)
            elig = []
            for cd in cards:
                if gl.cardpowerdict[cd] % 13 == x:
                    elig.append(cd)
            if len(elig) > match - 1:
                for hand in list(iter.combinations(elig, match)):
                    hands.append(hand)
    return hands

def Straights(beat, card): #straights
    hands = []
    if beat
    

playernum = 1 #testing
#playernum = int(sys.argv[1]) # accepts an int representing the player to be checked (0-3)
filenames = ["player1", "player2", "player3", "player4"]
os.chdir("saved_data")

playerfile = open(gl.filenames[playernum])
thing = playerfile.readline()
cards = thing.split(',')

playerfile.readline()
playedCard = playerfile.readline()
playedHand = playedCard.split(',')

""" if playedHand[0] == '-1': """
if len(playedHand) == 1: # single hands
    SingleHands(playedHand[0], cards)
elif len(playedHand) < 5: # pairs, triples, four of a kinds
    SameHands(HighestCard(playedHand),cards, len(playedHand))