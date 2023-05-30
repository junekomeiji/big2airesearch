# Function for excecuting moves
from init import Card

def nextplayer(num):
    if num == 4:
        return 1
    else:
        return num + 1

def execute_move(hand: list, player: int): #given a valid hand, changes the gamestate to reflect the new move
    file = open("gamestate", "r")
    save = file.readlines()
    file.close()
    deck = []
    for cardstr in save[player].split(','):
        deck.append(int(cardstr))

    used_deck = [map(int,hand)]
    for cardstr in save[5].split(','):
        used_deck.append(int(cardstr))
    used_deck.sort()
    
    for card in hand:
        deck.remove(card.number)
    file = open("gamestate", "w")
    for x in range(5): # writes the various decks
        if x == player:
            file.write(','.join(map(str,deck)))
        else:
            file.write(save[x]) 
        file.write("\n")
    file.write(','.join(map(str,used_deck)))
    file.write("\n")
    file.write(','.join(map(str,map(int,hand))))
    file.write("\n")
    file.write(str(nextplayer(player)))
    file.close()