import random
import os

print("Initializing game...")
print("Creating deck...")
deck = []
# Creating the deck of cards
# 1-4 for card suit (diamond, heart, spade, club)
# 1-13 for card type (1-10, J, Q, K)
# this way of naming might be useful (number comparisons?)

for x in range(4):
    for y in range(13):
        card = str(x + 1) + " " + str(y + 1)
        deck.append(card)

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
    if select == "4 3":
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

os.mkdir("saved_data")
os.chdir("saved_data")

gameStateSave = open("gamestate", "w")
for card in deck:
    gameStateSave.write(card)
    gameStateSave.write(",")
gameStateSave.write("\n")
for card in deck1:
    gameStateSave.write(card)
    gameStateSave.write(",")
gameStateSave.write("\n")
for card in deck2:
    gameStateSave.write(card)
    gameStateSave.write(",")
gameStateSave.write("\n")
for card in deck3:
    gameStateSave.write(card)
    gameStateSave.write(",")
gameStateSave.write("\n")
gameStateSave.write("-1\n") # no current card
gameStateSave.write(str(firstplayer))
gameStateSave.close()