# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 21:57:09 2026

@author: Sienna (Nen) Segura
IFT 360 AI Applications
Project: Connect 4 AI Agent
"""
import numpy as np
import random
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4
WINDOW_EMPTY = 0

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, column, piece):
    board[row][column] = piece

def valid_location(board, column):
    return board[ROW_COUNT-1][column] == 0

            

def get_next_open_row(board, column):
    for r in range(ROW_COUNT):
        if board[r][column] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    #Check for Horizontal wins
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    
    #Check for Vertical wins
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    
    #Check for Increasing Diagonal wins
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    
    #Check for Decreasing Diagonal wins
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
            
            
def window_update(window, piece):
    score = 0
    
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE
        
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(WINDOW_EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(WINDOW_EMPTY) == 2:
        score += 5
    

    if window.count(opponent_piece) == 3 and window.count(WINDOW_EMPTY) == 1:
        score += -80
        
    return score
            
def score_position (board, piece):
   
    score = 0
    
    #Prefer Center Columns
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 6
    
    #Count the Horizontal Score

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            
            score += window_update(window, piece)
                
     #Count the Vertical Score
    for c in range(COLUMN_COUNT):
        column_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = column_array[r:r+WINDOW_LENGTH]
             
            score += window_update(window, piece)
                 
    #Count Increasing Diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            
            score += window_update(window, piece)
                 
    #Count for Decreasing Diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            
            score += window_update(window, piece)
                
    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(open_location_list(board)) == 0

def minmax(board, depth, maximizingPlayer):
    open_locations = open_location_list(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
            value = -math.inf
            best_column = random.choice(open_locations)
            for column in open_locations:
                row = get_next_open_row(board, column)
                b_copy = board.copy()
                drop_piece(b_copy, row, column, AI_PIECE)
                new_score = minmax(b_copy, depth-1, False)[1]
                if new_score > value:
                    value = new_score
                    best_column = column
            return best_column, value
    else:
        value = +math.inf
        best_column = random.choice(open_locations)
        for column in open_locations:
            row = get_next_open_row(board, column)
            b_copy = board.copy()
            drop_piece(b_copy, row, column, PLAYER_PIECE)
            new_score = minmax(b_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                best_column = column
        return best_column, value


def open_location_list(board):
    open_locations = []
    for column in range(COLUMN_COUNT):
        if valid_location(board, column):
            open_locations.append(column)
    return open_locations

def select_best(board, piece):
    
    open_locations = open_location_list(board)
    best_score = -100
    best_column = random.choice(open_locations)
    for column in open_locations:
        row = get_next_open_row(board, column)
        temp_board = board.copy()
        drop_piece(temp_board, row, column, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_column = column
            
   
            
    return best_column
        

board = create_board()
print_board(board)
game_over = False
turn = random.randint(PLAYER, AI)

while not game_over:
    #Ask for player 1 input
    if turn == PLAYER:
        column = int(input("Player 1's Turn (0-6):"))
        
        if valid_location(board, column):
                row = get_next_open_row(board, column)
                drop_piece(board, row, column, PLAYER_PIECE)
                
                if winning_move(board, 1):
                    print("Winner: Player 1!")
                    print(print_board(board))
                    game_over =True
                    
                turn += 1
                turn = turn % 2
        
       
    #AI Move
    if turn == AI and not game_over:
        #column = random.randint(0, COLUMN_COUNT-1)
        #column = select_best(board, AI_PIECE)
        column, minimax_score = minmax(board, 2, True)
        
        if valid_location(board, column):
                row = get_next_open_row(board, column)
                drop_piece(board, row, column, AI_PIECE)
                
                if winning_move(board, 2):
                    print("Winner: Player 2!")
                    print(print_board(board))
                    game_over =True
                    break
                
                print(print_board(board))
    
                turn += 1
                turn = turn % 2