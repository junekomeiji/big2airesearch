import random
import math
import os
import globals as gl

class Card:
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

def main():
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
    gameStateSave.close()

if __name__ == "__main__":
    main()