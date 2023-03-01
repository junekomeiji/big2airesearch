'''
Contains global constants for ease of access from other modules.
'''
filenames = ["player1", "player2", "player3", "player4"]
"""
filenames for player saves
"""
cardsinorder = ['1 1', '1 2', '1 3', '1 4', '1 5', '1 6', '1 7', '1 8', '1 9', '1 10', '1 11', '1 12', '1 13',
                '2 1', '2 2', '2 3', '2 4', '2 5', '2 6', '2 7', '2 8', '2 9', '2 10', '2 11', '2 12', '2 13',
                '3 1', '3 2', '3 3', '3 4', '3 5', '3 6', '3 7', '3 8', '3 9', '3 10', '3 11', '3 12', '3 13',
                '4 1', '4 2', '4 3', '4 4', '4 5', '4 6', '4 7', '4 8', '4 9', '4 10', '4 11', '4 12', '4 13']
"""
Cards in ascending order of power
Note that the type starts from 3, not ace.
"""
# 1-4 for card suit (diamond, heart, spade, club)
# 1-13 for card type (3-10, J, Q, K, 1, 2) NOTE THAT THE TYPE STARTS FROM 3. '1 1' IS THE 3 OF DIAMONDS, NOT ACE.
# this way of naming might be useful (direct comparisons?)

cardpowerdict = {'1 1' : 0, '1 2' : 1, '1 3' : 2, '1 4' : 3, '1 5' : 4, '1 6' : 5, '1 7' : 6, '1 8' : 7, '1 9' : 8, '1 10' : 9, '1 11' : 10, '1 12' : 11, '1 13' : 12,
                '2 1' : 13, '2 2' : 14, '2 3' : 15, '2 4' : 16, '2 5' : 17, '2 6' : 18, '2 7' : 19, '2 8' : 20, '2 9' : 21, '2 10' : 22, '2 11' : 23, '2 12' : 24, '2 13' : 25,
                '3 1' : 26, '3 2' : 27, '3 3' : 28, '3 4' : 29, '3 5' : 30, '3 6' : 31, '3 7' : 32, '3 8' : 33, '3 9' : 34, '3 10' : 35, '3 11' : 36, '3 12' : 37, '3 13' : 38,
                '4 1' : 39, '4 2' : 40, '4 3' : 41, '4 4' : 42, '4 5' : 43, '4 6' : 44, '4 7' : 45, '4 8' : 46, '4 9' : 47, '4 10' : 48, '4 11' : 49, '4 12' : 50, '4 13' : 51}
"""
Dictionary of cards and their numerical power.
"""
# useful for finding cards of the same type, suit, etc. (modulo is very useful)