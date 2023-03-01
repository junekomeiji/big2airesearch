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

cardpowerdict = {'1 1' : 1, '1 2' : 2, '1 3' : 3, '1 4' : 4, '1 5' : 5, '1 6' : 6, '1 7' : 7, '1 8' : 8, '1 9' : 9, '1 10' : 10, '1 11' : 11, '1 12' : 12, '1 13' : 13,
                '2 1' : 14, '2 2' : 15, '2 3' : 16, '2 4' : 17, '2 5' : 18, '2 6' : 19, '2 7' : 20, '2 8' : 21, '2 9' : 22, '2 10' : 23, '2 11' : 24, '2 12' : 25, '2 13' : 26,
                '3 1' : 27, '3 2' : 28, '3 3' : 29, '3 4' : 30, '3 5' : 31, '3 6' : 32, '3 7' : 33, '3 8' : 34, '3 9' : 35, '3 10' : 36, '3 11' : 37, '3 12' : 38, '3 13' : 39,
                '4 1' : 40, '4 2' : 41, '4 3' : 42, '4 4' : 43, '4 5' : 44, '4 6' : 45, '4 7' : 46, '4 8' : 47, '4 9' : 48, '4 10' : 49, '4 11' : 50, '4 12' : 51, '4 13' : 42}
"""
Dictionary of cards and their numerical power.
"""
# useful for finding cards of the same type, suit, etc. (modulo is very usefuls)