from init import Card

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
"""

# hand, prev_hand, and inventory are all lists of Card objects

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
    else:
        return 0 # check for 5-card hands is in verify_power

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
            
def verify(hand, inventory, prev_hand, prev_empty = False):
    ret = verify_inventory(hand, inventory)
    if ret != 0:
        return ret
    ret =verify_type(hand)
    if ret != 0:
        return ret
    ret = verify_power(hand, prev_hand, prev_empty)
    return ret