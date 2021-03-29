import random

WIDTH = 8  
HEIGHT = 8

# Getting new board input
def game_board():
    board = []
    for column in range(HEIGHT):
        board.append(input())
    return board

# Selecting the player tile
def enter_player_tile():
    tile = ''
    while not (tile == 'W' or tile == 'B'):
        print('Do you want to be W or B ?')
        tile = input().upper()
    if tile == 'W':
        return['W','B','player1']
    else:
        return['B','W','player1']
    
# who gets first move
def who_goes_first():
    #random choose the player who goes first 
    if random.randint(0, 1) == 0:
        return 'player1'
    else:
        return 'player2'

# Printing the existing board
def print_board(board):
    for column in range(HEIGHT):
        print(''.join(map(str, board[column])))
    return board

#score board
def Score_Board(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'W' and 'B'.
    W_score = 0
    B_score = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'W':
                W_score += 1
            if board[x][y] == 'B':
                B_score += 1
    return {'W':W_score, 'B':B_score}

#getting the players move
def get_player_move(board, player_move):
    keys = '1 2 3 4 5 6 7 8'.split()

    while True:
         print('Enter your Move, "Q" to end the game, or "L" to available moves.')
         move = input()
         if move == 'Q':
             return 'quit'
         if move == 'L':
             return 'list'
         if move[0] == 'M' and len(move) == 3 and move[1] in keys and move[2] in keys:
             x = int(move[1])
             y = int(move[2])
             if is_valid_move(board, player_move, x, y) == False:
                 print('invalid move')
                 continue
             else:
                 break
             break
         else:
             print('That is not a valid move. Enter the column (1-8) and then the row (1-8).')
             print('For example, 81 will move on the top-right corner.')
    return [x, y]

def get_valid_moves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    valid_moves = []
    
    for x in range(8):
        for y in range(8):
            if is_valid_move(board, tile, x, y) != False:
                valid_moves.append([x, y])
    return valid_moves
def is_on_board(x, y):
    return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1

def is_valid_move(board, tile, xstart, ystart):
    dup_board = [[1 for x in range(8)] for y in range(8)]
    if board[xstart][ystart] != '-':
        return False  
    
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if i == xstart:
                if j == ystart:
                    dup_board[i][j] = tile
                else:
                    dup_board[i][j] = board[i][j]
            else:
                dup_board[i][j] = board[i][j]
    
    if tile == 'W':
        other_tile ='B'
    else :
        other_tile = 'W'
    tiles_to_flip =[]
    for xdirection, ydirection in [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if is_on_board(x,y) and board[x][y] == other_tile:
            x += xdirection
            y += ydirection
        if not is_on_board(x,y):
            continue
        while board[x][y] == other_tile:
            x += xdirection
            y += ydirection
            if not is_on_board(x,y):
                break
        if not is_on_board(x,y):
            continue
        if board[x][y]  == tile:
            while True:
                x -= xdirection
                y -= ydirection
                if x == xstart and y == ystart:
                    break
                tiles_to_flip.append([x,y])
    
    if len(tiles_to_flip) == 0:
        return False
    return [tiles_to_flip, dup_board]

def make_move(board, tile, xstart, ystart):
    tiles_to_flip, sample = is_valid_move(board, tile, xstart, ystart)
    
    if tiles_to_flip == False:
        return False
    sample[xstart][ystart] = tile
    for x , y in tiles_to_flip:
        sample[x][y] = tile
    return sample

print('welcome to Goro Hasegawa creation')
print('Enter number of games to be played ?')
value = int(input())
for game in range(value):
    new_game_board = game_board()
    player1_move, player2_move, turn = enter_player_tile()
    #turn = who_goes_first()
    print('The ' + turn + ' will start the game')
    while True:
        if turn == 'player1':
            move = get_player_move(new_game_board, player1_move)
            if move == 'quit':
                print_board(new_game_board)
                break
            elif move == 'list':
                list = get_valid_moves(new_game_board,player1_move)
                print('%s' % list)
                continue
            else:
                new_game_board = make_move(new_game_board, player1_move, move[0], move[1])
                scores = Score_Board(new_game_board)
                print('White - %s. Black = %s.' % (scores['W'], scores['B']))
                turn = 'player2'
        else:
            move = get_player_move(new_game_board, player2_move)
            if move == 'quit':
                print_board(new_game_board)
                break
            elif move == 'list':
                list = get_valid_moves(new_game_board, player2_move)
                print('%s' % list)
                continue
            else:
                new_game_board = make_move(new_game_board, player2_move, move[0], move[1])
                scores = Score_Board(new_game_board)
                print('White - %s. Black = %s.' % (scores['W'], scores['B']))
                turn = 'player1'