import sys
import random

symbols = ['X','O']

def score(state,max_piece,player,level):
    """
    state is the current game state.
    max_piece is the player who is trying to maximize the score/ Bot's piece.
    player is the one whose turn going on.
    level represents the level in recurrsion tree.
    """
    min_piece = symbols[1-symbols.index(max_piece)]
    if  state[0]==state[1]==state[2]== max_piece or state[3]==state[4]==state[5]==max_piece or state[6]==state[7]==state[8]==max_piece or \
        state[0]==state[3]==state[6]== max_piece or state[1]==state[4]==state[7]==max_piece or state[2]==state[5]==state[8]==max_piece or \
        state[0]==state[4]==state[8]== max_piece or state[2]==state[4]==state[6]==max_piece:
        return 1
    elif state[0]==state[1]==state[2]== min_piece or state[3]==state[4]==state[5]==min_piece or state[6]==state[7]==state[8]==min_piece or \
        state[0]==state[3]==state[6]== min_piece or state[1]==state[4]==state[7]==min_piece or state[2]==state[5]==state[8]==min_piece or \
        state[0]==state[4]==state[8]== min_piece or state[2]==state[4]==state[6]==min_piece:
        return -1
    elif state.count(0) == 0:
        return 0
    else:
        return move(state,symbols[1-symbols.index(player)],player!=max_piece,level+1)

def move(state,piece,maximizer=True,level=0):
    """
    state is the current game state.
    piece is the player's piece.
    maximizer represents whether player is maximizer or minimizer.
    level represents the level in recurrsion tree.
    """

    if state.count(0) == 9:
        return random.randint(0,8)

    scores = list()
    for i in range(9):
        if state[i] == 0:
            temp = state.copy()
            temp[i] = piece
            if maximizer == False:
                scores.append(score(temp,symbols[1-symbols.index(piece)],piece,level))
            else:
                scores.append(score(temp,piece,piece,level))
    if maximizer == True:
        if level == 0:
            max_index = scores.index(max(scores))
            iter = -1
            for _ in range(9):
                if state[_] == 0:
                    iter = iter +1
                    if iter == max_index:
                        return _

        else:
            return max(scores)
    else:
        return min(scores)
