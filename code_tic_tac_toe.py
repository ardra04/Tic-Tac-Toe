import math
import numpy as np
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None
def initial_state():                                   
    return [[EMPTY, EMPTY, EMPTY],   
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def fetch_daiag(board):
    return [[board[0][0], board[1][1], board[2][2]],
            [board[0][2], board[1][1], board[2][0]]]

def fetch_col(board):
    columns = []
    for i in range(3):
        columns.append([row[i] for row in board])
    return columns

def fetchthreeinrow(row):
    return True if row.count(row[0]) == 3 else False            

def player(board):
    ct_x=0    
    ct_y=0
    for i in board:
        for j in i:
            if(j=="O"):
                ct_y=ct_y+1
            if(j=="X"):
                ct_x=ct_x+1    
    return O if ct_x > ct_y else X


def actions(board):           
    action=set()
    for i, row in enumerate(board):
        for j , val2 in enumerate(row):
            if(val2==EMPTY):
                action.add((i,j))
    return action



def result(board, action):                    
    i,j=action
    if(board[i][j]!=EMPTY):
        raise Exception("Invalid Move ")
    move_next=player(board)
    board_dc=deepcopy(board)
    board_dc[i][j]=move_next
    return board_dc


def winner(board):                  
   
    rows=board+fetch_daiag(board) +fetch_col(board)                
    for row in rows:
        current_palyer=row[0]           
        if current_palyer is not None and fetchthreeinrow(row):
            return current_palyer
    return None

def terminal(board):     
    winx=winner(board)
    if(winx is  not None):
        return True
    if(all(all(j!=EMPTY for j in i) for i in board)):    
        return True
    return False


def utility(board):       
    winx=winner(board)
    if(winx==X):
        return 1
    elif(winx==O):
        return -1
    else:
        return 0 

def max_ab_pruning(board ,alpha,beta):
    if(terminal(board)== True):
        return utility(board) , None
    val2=float("-inf")
    best=None
    for action in actions(board):
        min_val=min_ab_pruning(result(board ,action), alpha, beta)[0]
        if( min_val > val2):
            best=action
            val2=min_val
        alpha=max(alpha,val2)
        if (beta <= alpha):
            break
    return val2,best

def min_ab_pruning(board ,alpha,beta): 
    if(terminal(board)== True):
        return utility(board) , None
    val2=float("inf")
    best=None
    for action in actions(board):
        max_val=max_ab_pruning(result(board ,action), alpha, beta)[0]
        if( max_val < val2):
            best=action
            val2=max_val
        beta=min(beta,val2)
        if (beta <= alpha):
            break
    return val2,best


def mini_max(board):
    if terminal(board):
        return None
    if(player(board)==X):          
        return max_ab_pruning(board ,float("-inf") ,float("inf"))[1]
    elif(player(board) == O):     
        return min_ab_pruning(board , float("-inf"), float("inf"))[1]
    else:
        raise Exception("Error")
