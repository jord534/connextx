import numpy as np
import random

# Gets board at next step if agent drops piece in selected column
def drop_piece(grid, col, piece, config):
    next_grid = grid.copy()
    for row in range(config.rows-1, -1, -1):
        if next_grid[row][col] == 0:
            break
    next_grid[row][col] = piece
    return next_grid

# Returns True if dropping piece in column results in game win
def check_winning_move(obs, config, col, piece):
    # Convert the board to a 2D grid
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    next_grid = drop_piece(grid, col, piece, config)
    # horizontal
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[row,col:col+config.inarow])
            if window.count(piece) == config.inarow:
                return True
    # vertical
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(next_grid[row:row+config.inarow,col])
            if window.count(piece) == config.inarow:
                return True
    # positive diagonal
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[range(row, row+config.inarow), range(col, col+config.inarow)])
            if window.count(piece) == config.inarow:
                return True
    # negative diagonal
    for row in range(config.inarow-1, config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
            if window.count(piece) == config.inarow:
                return True
    return False

def dist_to_win(obs, config, col, piece):
        grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        # find the column which brings me closer to config.inarow
        # count ??
        min_dist = float('inf')
        # horizontal
        for row in range(config.rows):
            window_fwd = list(grid[row,col:col+config.inarow])
        #for row in range(config.rows - config.inarow):
            window_bwd = list(grid[row,col-config.inarow:col + 1])
        min_dist = min(min_dist, config.inarow - max(window_fwd.count(piece), window_bwd.count(piece)))
        
        # vertical
        for row in range(config.rows-(config.inarow-1)):
            window_fwd = list(grid[row:row+config.inarow,col])
        for row in range(config.inarow-1, config.rows):
            window_bwd = list(grid[row-config.inarow:row+1,col])
        min_dist = min(min_dist, config.inarow - max(window_fwd.count(piece), window_bwd.count(piece)))
                           
        # positive diagonal 
        if col <= config.columns - config.inarow:
            for row in range(config.rows-(config.inarow-1)):
                window_fwd = list(grid[range(row, row+config.inarow), range(col, col+config.inarow)]) # 21 in dist_to_win
        if col >= config.inarow-1:
            for row in range(config.inarow-1, config.rows):
                window_bwd = list(grid[range(row-config.inarow+1, row+1), range(col-config.inarow+1,col+1)])
        min_dist = min(min_dist, config.inarow - max(window_fwd.count(piece), window_bwd.count(piece)))
        
        # negative diagonal
        if col <= config.columns - config.inarow:
            for row in range(config.inarow-1, config.rows):
                window_fwd = list(grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
        if col >= config.inarow-1:
            for row in range(config.inarow-1, config.rows):
                window_bwd = list(grid[range(row, row-config.inarow, -1), range(col-config.inarow+1, col+1)])
        min_dist = min(min_dist, config.inarow - max(window_fwd.count(piece), window_bwd.count(piece)))
        
        return min_dist



def my_agent(obs, config):
    # Your code here: Amend the agent!
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]

    # check if winning move
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    piece = obs.mark
    for move in valid_moves:
        if check_winning_move(obs, config, move, piece):
            return move
            
    # check if opponent has winning move
    if piece == 1:
        opp_piece = 2
    else:
        opp_piece = 1
    for move in valid_moves:
        if check_winning_move(obs, config, move, opp_piece):
            return move # block opp winning by making the agent play this move

    # find the thread closest to completion amongst threads opened by my pieces
    # ie the horizontal, vertical or diagonal (positive or negative) thread closest to config.inarow
    cur_min = float('inf')
    cur_move_idx = -1
    for i, move in enumerate(valid_moves):
        if dist_to_win(obs, config, move, piece) < cur_min:
            cur_min = dist_to_win(obs, config, move, piece)
            cur_move_idx = i

    return valid_moves[cur_move_idx]
