'''
 X | O | X
---+---+---
 O | O | X    
---+---+---
   | X | 
'''

import random


def print_board_and_legend(board):
    for i in range(3):
        line1 = " " +  board[i][0] + " | " + board[i][1] + " | " +  board[i][2]
        line2 = "  " + str(3*i+1)  + " | " + str(3*i+2)  + " | " +  str(3*i+3) 
        print(line1 + " "*5 + line2)
        if i < 2:
            print("---+---+---" + " "*5 + "---+---+---")
        
    
    
def make_empty_board():
    board = []
    for i in range(3):
        board.append([" "]*3)
    return board

def num_to_coords(sq):
    return [(sq - 1) // 3, (sq - 1) % 3]

def put_in_board(board, mark, square_num):
    coords = num_to_coords(square_num)
    board[coords[0]][coords[1]] = mark

def play():  # we dont check for wins thus doesnt end
    board = make_empty_board()
    turn = "X"
    while True:
        print_board_and_legend(board)
        print(f"{turn}'s turn. Pick your spot.")
        sq = int(input())
        put_in_board(board, turn, sq)
        turn = "O" if turn == "X" else "X"

def get_free_squares(board):
    res = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                res.append([i, j])
    return res

def make_random_move(board, mark):
    free = get_free_squares(board)
    i = int(len(free)*random.random())
    coords = free[i]
    board[coords[0]][coords[1]] = mark

def make_better_move(board, mark):
    free = get_free_squares(board)
    for i, j in free:
        new_board = [row.copy() for row in board] # deep copy
        new_board[i][j] = mark
        if is_win(new_board, mark):
            board[i][j] = mark
            return
    else:
        make_random_move(board, mark)


def make_best_move(board, mark):
    opponent = "O" if mark == "X" else "X"

    def score(position, turn, depth):
        if is_win(position, mark):
            return 10 - depth
        if is_win(position, opponent):
            return depth - 10
        free = get_free_squares(position)
        if not free:
            return 0

        scores = []
        next_turn = opponent if turn == mark else mark
        for i, j in free:
            trial = [row.copy() for row in position]
            trial[i][j] = turn
            scores.append(score(trial, next_turn, depth + 1))
        return max(scores) if turn == mark else min(scores)

    if is_win(board, mark) or is_win(board, opponent):
        return

    best_score = float("-inf")
    best_move = None
    for i, j in get_free_squares(board):
        trial = [row.copy() for row in board]
        trial[i][j] = mark
        move_score = score(trial, opponent, 1)
        if move_score > best_score:
            best_score = move_score
            best_move = (i, j)

    if best_move is not None:
        i, j = best_move
        board[i][j] = mark


def play_against_computer(computer_move):
    board = make_empty_board()
    print("Who starts?")
    print("1. You")
    print("2. Clanker")
    starter = int(input())
    player = "X" if starter == 1 else "O"
    clanker = "O" if starter == 1 else "X"
    turn = "X"
    while get_free_squares(board):
        if turn == player:
            print_board_and_legend(board)
            print(f"{turn}'s turn. Pick your spot.")
            sq = int(input())
            put_in_board(board, turn, sq)
            if is_win(board, turn):
                print_board_and_legend(board)
                print(f"Game over. {turn} wins!")
                return
            turn = clanker
        else:
            computer_move(board, turn)
            if is_win(board, turn):
                print_board_and_legend(board)
                print(f"Game over. {turn} wins!")
                return
            turn = player
    print_board_and_legend(board)
    print("Game over. Draw!")

def is_row_all_marks(board, row_i, mark):
    for m in board[row_i]:
        if m != mark:
            return False
    return True

def is_col_all_marks(board, col_i, mark):
    col = [board[i][col_i] for i in range(3)]
    for c in col:
        if c != mark:
            return False
    return True

def is_win(board, mark):
    for i in range(3):
        if is_row_all_marks(board, i, mark):
            return True
        if is_col_all_marks(board, i, mark):
            return True
    for i in range(3):
        if board[i][i] != mark:
            break
    else:
        return True
    for i in range(3):
        if board[i][2 - i] != mark:
            break
    else:
        return True
    return False




if __name__ == '__main__':
    # board = make_empty_board()
    # print_board_and_legend(board)    
    #
    # print("\n\n")
    #
    board = [["O", "X", "X"],
             [" ", "X", " "],
             [" ", "O", " "]]

    # print_board_and_legend(board)
    print(get_free_squares(board))
    print("LEVEL ONE: STUPID CLANKER")
    play_against_computer(make_random_move)
    print("LEVEL TWO: LESS STUPID CLANKER")
    play_against_computer(make_better_move)
    print("LEVEL THREE: OPTIMAL CLANKER")
    play_against_computer(make_best_move)

