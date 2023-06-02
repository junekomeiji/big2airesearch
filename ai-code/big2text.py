import random
import math
import os

# Composite of every script in ./big2-text/ for importing in other modules. 

class Card:
    def num_to_vector(num: int):
        cd = Card(num)
        return cd.to_vector()
    
    def __init__(self, number):
        self.number = number
        self.suit = number % 4
        self.value = math.floor(number/4)
        match self.value:
            case 12:
                self.ppValue = 2
            case 11:
                self.ppValue = 'A'
            case 10:
                self.ppValue = 'K'
            case 9:
                self.ppValue = 'Q'
            case 8: 
                self.ppValue = 'J'
            case _:
                self.ppValue = self.value + 3
            
        match self.suit:
            case 3:
                self.colour = 'spades'
            case 2:
                self.colour = 'hearts'
            case 1:
                self.colour = 'clubs'
            case 0:
                self.colour = 'diamonds'
                
    def to_vector(self):
        out = []
        out.append(self.value + 1)
        out.append(self.suit + 1)
        return out
        
    def __str__(self):
        return str(self.colour) + " " + str(self.ppValue)
    
    def __int__(self):
        return self.number
    
    def __repr__(self):
        return str(self.colour) + " " + str(self.ppValue)
    
    def __lt__(self, other):
        return self.number < other.number
    def __eq__(self, other):
        return self.number == other.number
    def __gt__(self, other):
        return self.number > other.number

def init():
    print("Initializing game...")
    print("Creating deck...")
    deck = []
    # Creating the deck of cards
    # 0-3 for card suit (diamond, heart, spade, club)
    # 0-12 for card type (3-10, J, Q, K, A, 2)

    for x in range(52):
        deck.append(Card(x))

    print(deck)
    print("Distributing cards...")
    # Distributing cards
    # Cards are distributed like in a real game, randomly in order from the main deck.

    deck1 = []
    deck2 = []
    deck3 = []
    deck4 = []
    i = 0
    firstplayer = -1 # The first player is determined during distribution. Loop checks for the three of diamonds. 

    while len(deck) > 0:
        select = random.choice(deck)
        if select.ppValue == 3 and select.colour == 'diamonds':
            firstplayer = i + 1
        deck.remove(select)
        if i == 0:
            deck1.append(select)
            i += 1
        elif i == 1:
            deck2.append(select)
            i += 1
        elif i == 2:
            deck3.append(select)
            i += 1
        else:
            deck4.append(select)
            i = 0
    # Sorts the cards in an ascending order. Possible use later on?
    # Right now just for internal aesthetic purposes.
    deck1.sort()
    deck2.sort()
    deck3.sort()
    deck4.sort()

    # Print for debug.
    print(deck)
    print(deck1)
    print(deck2)
    print(deck3)
    print(deck4)
    print(firstplayer)
    try:
        os.mkdir("saved_data")
    except FileExistsError:
        print("folder already exists.")
    os.chdir("saved_data")

    gameStateSave = open("gamestate", "w")
    gameStateSave.write(','.join(map(str,map(int,deck))))
    gameStateSave.write("\n")
    gameStateSave.write(','.join(map(str,map(int,deck1))))
    gameStateSave.write("\n")
    gameStateSave.write(','.join(map(str,map(int,deck2))))
    gameStateSave.write("\n")
    gameStateSave.write(','.join(map(str,map(int,deck3))))
    gameStateSave.write("\n")
    gameStateSave.write(','.join(map(str,map(int,deck4))))
    gameStateSave.write("\n")
    gameStateSave.write("-1\n") # no played cards
    gameStateSave.write("-1\n") # no current card
    gameStateSave.write(str(firstplayer))
    gameStateSave.write("0") # no skips yet
    gameStateSave.close()
    
# Takes a given hand and makes sure it is valid to play.
# This includes checking if the player has the cards, and also whether the hand is of a higher power.
# All methods return 0 when hand is valid.
# Assumtion that cards are sorted according to value.

"""
Return Codes:
0 - Hand is OK!
1 - Hand is not in player inventory!
2 - Hand is not of same type!
3* - Hand is of lower power!
4* - Hand is not correct!
5 - Hand does not contain 3 of diamonds
"""

# hand, prev_hand, and inventory are all lists of Card objects

def verify_firsthand(hand: list) -> int:
    if 0 not in hand:
        return 5
    else:
        return 0
        
    

def verify_inventory(hand: list, inventory: list) -> int:
    # checks if player has the cards in their inventory.
    for card in hand:
        if card not in hand:
            return 1
    return 0

def verify_type(hand: list) -> int:
    # checks if hand is correct for its type (pairs, triples match, etc.)
    if len(hand) < 2:
        return 0
    elif len(hand) < 4:
        for card in hand:
            if card.value != hand[0].value:
                return 40 + len(hand)
        return 0
    elif len(hand) == 4:
        return 44
    elif len(hand) == 5:
        return 0 # check for 5-card hands is in verify_power\
    else:
        return 4 + len(hand)

def verify_power(hand: list, prev_hand: list, prev_empty: bool = False) -> int:
    # checks if hand is of higher power
    if prev_empty and len(hand) != 5:
        return 0
    
    if not prev_empty and len(hand) != len(prev_hand):
        return 2
    
    if len(hand) == 0:
        return 0
    elif len(hand) < 5:
        if prev_hand[-1] < hand[-1]:
            return 0
        else:
            return 30 + len(hand)
    else:
        def rank(fivecards):
            if fivecards == []:
                return 0
            else:
                def value(quintuple):
                    va = []
                    for card in quintuple:
                        va.append(card.value - quintuple[0].value)
                    return va
                def suit(quintuple):
                    su = []
                    for card in quintuple:
                        su.append(card.suit)
                    return su
                v = value(fivecards)
                s = suit(fivecards)
                if v == [0,1,2,3,4]: # straight
                    if s[0] == s[1] == s[2] == s[3] == s[4]: # straight flush
                        return 5
                    else: 
                        return 1
                elif s[0] == s[1] == s[2] == s[3] == s[4]: # flush
                    return 2 
                elif (v[0] == v[1]) and (v[3] == v[4]) and (v[2] == v[1] or v[2] == v[3]): # full house
                    return 4
                elif (v[0] == v[1] == v[2] == v[3]) or (v[1] == v[2] == v[3] == v[4]): # four of a kind
                    return 5
                else:
                    return -1
        if rank(hand) < rank(prev_hand):
            if rank(hand) == -1:
                return 45
            else:
                return 35
        elif rank(hand) > rank(prev_hand):
            return 0
        else: # hands of equal rank
            if rank(hand) == 2 or rank(hand) == 5: # comparing straight or straight flush
                if hand[0].suit > prev_hand[0].suit:
                    return 0
                elif hand[0].suit < prev_hand[0].suit:
                    return 350 + rank(hand)
            if hand[4] > prev_hand[4]:
                return 0
            else:
                return 350 + rank(hand)
            
def verify(hand, inventory, prev_hand, prev_empty = False, first_hand = False):
    
    if first_hand:
        ret = verify_firsthand(hand)
        if ret != 0:
            return ret
    
    ret = verify_inventory(hand, inventory)
    if ret != 0:
        return ret
    ret = verify_type(hand)
    if ret != 0:
        return ret
    ret = verify_power(hand, prev_hand, prev_empty)
    return ret

def nextplayer(num):
    if num == 4:
        return 1
    else:
        return num + 1

def execute_move(hand: list, player: int): #given a valid hand, changes the gamestate to reflect the new move
    file = open("gamestate", "r")
    save = file.readlines()
    file.close()
    deck = [] # old player deck
    for cardstr in save[player].split(','):
        deck.append(int(cardstr))

    used_deck = [map(int,hand)]
    for cardstr in save[5].split(','): # adds used cards to the used deck
        used_deck.append(int(cardstr))
    used_deck.sort()
    
    for card in hand:
        deck.remove(card.number) # removes used cards from deck
    deck.sort()
    file = open("gamestate", "w")
    for x in range(5): # writes the various decks
        if x == player:
            file.write(','.join(map(str,deck)))
            file.write("\n")
        else:
            file.write(save[x])
    file.write(','.join(map(str,used_deck)))
    file.write("\n")
    file.write(','.join(map(str,map(int,hand))))
    file.write("\n")
    file.write(str(nextplayer(player)))
    file.write("\n")
    skip = int(save[8].strip(" \n"))
    if len(hand) == 0:
        skip += 1
        file.write(str(skip))
    else:
        file.write(save[8])
    file.close()
    
    if skip >= 3:
        reset_hand()
    
def reset_hand(): #resets the hand when a full skip has been done
    file = open("gamestate", "r")
    save = file.readlines()
    file.close()
    
    save[5] = "-1\n"
    save[8] = "0\n"
    file = open("gamestate", "w")
    file.writelines(save)
    file.close()

def are_we_done_yet() -> int: # returns player number when a player has won, else, return zero
    file = open("gamestate", "r")
    save = file.readlines()
    if "\n" in save:
        return save.index("\n")
    return 0
    
if __name__ == "__main__":
    pass