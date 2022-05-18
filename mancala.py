##################################
# 15110 Principles of Computing  #
# PA9: Mancala                   #
# Fall 2015                      #
##################################

# ~ Imports ~ #
import tkinter
from tkinter import Canvas
from random import randint, seed
from time import sleep

# ~ Global Variables ~ #
# [ DO NOT MODIFY! ]

BOARD_WIDTH = 360
BOARD_HEIGHT = 720
BOARD_MARGIN = 30
HOUSE_WIDTH = 135
HOUSE_HEIGHT = 60
STORE_WIDTH = 300
STORE_HEIGHT = 90
X_MARGIN = 30
Y_MARGIN = 15
HOUSE_PADDING = 10
STORE_PADDING = 15
X_COUNT_MARGIN = 15
Y_COUNT_MARGIN = 30

PEBBLE_RADIUS = 10

PLAY_MESSAGE = """
###########################
# ~ Let's play Mancala! ~ #
###########################
"""

WINDOW = tkinter.Tk()
CANVAS = Canvas(WINDOW, width=BOARD_WIDTH, height=BOARD_HEIGHT)
CANVAS.pack()


# ~ Tkinter custom circle function ~ #
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


tkinter.Canvas.create_circle = _create_circle


#########
# MODEL #
#########

# Creates a list representing a new board at the start of the game.
# @return {list} Represents the start state of the board
def new_board():
    # indices 6 and 13 are stores
    return [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]


# Returns the moves available to the given player according to the state of
# the board. A player can only choose a house on his side of the board which
# is not empty.
# @param board {list} Represents pebbles in each pit on board
# @param player {int} Player, can either be 0 or 1
# @return {list} Pits available for the player to pick
def get_available_moves(board, player):
    avail_moves = []
    if player == 0:
        if board[0] != 0:
            avail_moves = avail_moves + [0]
        if board[1] != 0:
            avail_moves = avail_moves + [1]
        if board[2] != 0:
            avail_moves += [2]
        if board[3] != 0:
            avail_moves += [3]
        if board[4] != 0:
            avail_moves += [4]
        if board[5] != 0:
            avail_moves += [5]
        return avail_moves

    elif player == 1:
        if board[7] != 0:
            avail_moves += avail_moves + [7]
        if board[8] != 0:
            avail_moves += [8]
        if board[9] != 0:
            avail_moves += [9]
        if board[10] != 0:
            avail_moves += [10]
        if board[11] != 0:
            avail_moves += [11]
        if board[12] != 0:
            avail_moves += [12]
        return avail_moves

    # Returns True if pit is a house on the player's side of the board


# @param player {int} Player, can either be 0 or 1
# @param pit {int} Pit index to evaluate
# @return {bool} True if pit is a house on player's side of the board
def is_plyr_house(player, pit):
    if player == 0:
        if pit == 0 or pit == 1 or pit == 2 or pit == 3 or pit == 4 or pit == 5:
            return True
        return False
    if player == 1:
        if pit == 7 or pit == 8 or pit == 9 or pit == 10 or pit == 11 or pit == 12:
            return True
        return False


# Returns False if there are no pebbles in any of the houses on the player's
# side of the board.
# @param board {list} Mancala board model
# @param player {int} Player, can only be 0 or 1
# @return {bool} False if player has no valid move to make
def has_move(board, player):
    avail_moves_lst = get_available_moves(board, player)
    if len(avail_moves_lst) != 0:
        return True
    return False


# Returns True if the match has ended.
# @param board {list} Board model
# @return {bool} True if match has ended
def is_end_match(board):
    player1_plays, player2_plays = False, False
    for i in range(0, 6):
        if board[i] != 0:
            player1_plays = True
    for i in range(7, 13):
        if board[i] != 0:
            player2_plays = True
    return not (player1_plays and player2_plays)


# Returns True if finished game ended in a win, False if ended in a tie
# @param board {list} Board model
# @return {bool} True if match has ended in a win
def is_win(board):
    for i in range(0, 6):
        board[6] += board[i]
        board[i] = 0
    for i in range(7, 13):
        board[13] += board[i]
        board[i] = 0
    display_board(board)
    if board[6] == board[13]:
        print("It's a tie")
        return False
    elif board[6] > board[13]:
        print("Player 0 wins!")
        return True
    elif board[6] < board[13]:
        print("Player 1 wins!")
        return True


########
# VIEW #
########

# Returns drawing bounds of given pit.
# @param {int} Pit index
# @return {list} Drawing bounds of pit as [left, top, right, bottom]
def get_pit_coors(pit):
    # If pit is in right column
    # CALCULATE PIT DIMENSIONS FROM BOTTOM UP
    if (0 <= pit <= 5):
        # Left side of right column
        left = BOARD_MARGIN + HOUSE_WIDTH + X_MARGIN
        right = left + HOUSE_WIDTH
        # Bottom edge of player0 side of board, i.e. the bottom edge of the
        # houses at the bottom of the board
        side0_baseline = BOARD_HEIGHT - (BOARD_MARGIN + STORE_HEIGHT + Y_MARGIN)
        # If pit is in bottom half (side0) of board
        if (pit <= 2):  # (pits 0-2)
            bottom = side0_baseline - (HOUSE_HEIGHT * pit) - (Y_MARGIN * pit)
            top = bottom - HOUSE_HEIGHT
        # If pit is in top half (side1) of board
        else:  # (pits 3-5)
            # Subtract extra Y_MARGIN to previous calculation
            bottom = (side0_baseline - Y_MARGIN) - (HOUSE_HEIGHT * pit) - (Y_MARGIN * pit)
            top = bottom - HOUSE_HEIGHT
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif (7 <= pit <= 12):
        left = BOARD_MARGIN
        right = left + HOUSE_WIDTH
        side1_topline = BOARD_MARGIN + STORE_HEIGHT + Y_MARGIN
        if (pit <= 9):  # pits 7-9
            pit -= 7
            top = side1_topline + (HOUSE_HEIGHT * pit) + (Y_MARGIN * pit)
            bottom = top + HOUSE_HEIGHT
        else:  # pits 10-12
            pit -= 7
            top = (side1_topline + Y_MARGIN) + (HOUSE_HEIGHT * pit) + (Y_MARGIN * pit)
            bottom = top + HOUSE_HEIGHT
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    else:
        left = BOARD_MARGIN
        right = left + STORE_WIDTH
        if (pit == 6):
            top = BOARD_MARGIN
            bottom = top + STORE_HEIGHT
        else:  # pit == 13
            bottom = BOARD_HEIGHT - BOARD_MARGIN
            top = bottom - STORE_HEIGHT
    return [left, top, right, bottom]


# Returns random drawing center coordinates of a pebble placed within bounds of
# given pit.
# @param {int} Pit index
# @return {list} Random center coordinates as [center_x, center_y]
def get_pebble_coors(pit):
    pitlst = get_pit_coors(pit)
    if pit in range(0, 6) or pit in range(7, 13):
        L = pitlst[0] + 20
        to = pitlst[1] + 20
        R = pitlst[2] - 20
        bot = pitlst[3] - 20
        return [randint(L, R), randint(to, bot)]
    elif pit == 6 or pit == 13:
        L = pitlst[0] + 25
        to = pitlst[1] + 25
        R = pitlst[2] - 25
        bot = pitlst[3] - 25
        width = randint(L, R)
        height = randint(to, bot)
        return [width, height]


# ~ DO NOT DELETE PROVIDED LINES OF CODE ~
# Draws the entire board display based on the model.
# @param {list} Board model
# @param {int} Player, can only be 0 or 1
# return {None}
def display_board(board):
    CANVAS.delete(tkinter.ALL)  # DO NOT REMOVE
    # TODO: Draw board body
    CANVAS.create_rectangle(0, 0, BOARD_WIDTH, BOARD_HEIGHT / 2, fill='#8A5C2E', width=0)
    CANVAS.create_rectangle(0, BOARD_HEIGHT / 2, BOARD_WIDTH, BOARD_HEIGHT, fill='#996633', width=0)

    # TODO: Draw all store and house pits
    for pit in range(0, 14):
        pit_coor = get_pit_coors(pit)

        # these are the coordinates for left, top, right, and bot
        L = pit_coor[0]
        top = pit_coor[1]
        R = pit_coor[2]
        bot = pit_coor[3]
        if pit == 6 or pit == 13:
            pad = 15
        else:
            pad = 10
        draw_pit(L, top, R, bot, pad)

    # TODO: Draw pebble counts for each pit
    for pit in range(0, len(board)):
        draw_pebble_count(board, pit)

    # TODO: Draw pebbles in each pit
    for pit in range(0, len(board)):
        seed(pit)  # DO NOT REMOVE; pit must be defined before
        num = board[pit]
        while num > 0:  # number of pebbles in pit
            peb_coor = get_pebble_coors(pit)
            x = peb_coor[0]
            y = peb_coor[1]
            draw_pebble(x, y)
            num = num - 1
    sleep(0.3)  # DO NOT REMOVE
    WINDOW.update()  # DO NOT REMOVE


# GRAPHICAL ELEMENT DRAW FUNCTIONS - DO NOT EDIT THIS CODE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Draw one pit.
# @params left, top, right, bottom {int} Dimensions of pit
# @param padding {int} Width of pit padding (HOUSE_PADDING or STORE_PADDING)
# @return {None}
def draw_pit(left, top, right, bottom, padding):
    CANVAS.create_rectangle(left, top, right, bottom, fill='#634321', width=0)
    CANVAS.create_line(left, top, left + padding, top + padding, fill='#4F361A')
    CANVAS.create_line(right, bottom, right - padding, bottom - padding, fill='#4F361A')
    CANVAS.create_line(right, top, right - padding, top + padding, fill='#4F361A')
    CANVAS.create_line(left, bottom, left + padding, bottom - padding, fill='#4F361A')
    CANVAS.create_rectangle(left, top, right, bottom, fill=None, outline='#966C43')
    CANVAS.create_rectangle(left + padding, top + padding, right - padding, bottom - padding, fill='#704B25',
                            outline='#4F361A')


# Draw one pebble.
# @params center_x, center_y {int} Center coordinates for pebble
# return {None}
def draw_pebble(center_x, center_y):
    CANVAS.create_circle(center_x, center_y, PEBBLE_RADIUS, fill='#A01F1F', outline='DarkRed')
    CANVAS.create_circle(center_x, center_y, PEBBLE_RADIUS, fill='FireBrick', width=0)
    CANVAS.create_circle(center_x + 4, center_y - 4, 1.5, fill='GhostWhite', width=0)


# Draw one pebble count for pit next to pit on board.
# @param board {list} Board model
# @param pit {pit} Pit for which to draw count
# return {None}
def draw_pebble_count(board, pit):
    pit_coors = get_pit_coors(pit)
    (left, top) = (pit_coors[0], pit_coors[1])
    (right, bottom) = (pit_coors[2], pit_coors[3])
    if (pit < 7):  # Pits in the right column have pebble counts drawn on right
        # of pit
        x = right + X_COUNT_MARGIN
        y = top + Y_COUNT_MARGIN
    else:  # Pits in left column have pebble counts drawn on left of pit
        x = left - X_COUNT_MARGIN
        y = top + Y_COUNT_MARGIN
    count = str(board[pit])
    CANVAS.create_text(x, y, text=count, anchor="center")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# END GRAPHICAL ELEMENT DRAW FUNCTIONS


##############
# CONTROLLER #
##############

# Allows players to interact with the terminal to pick the pits
def pick_pit(board, player):
    while True:
        print("-----It is player " + str(player) + "'s turn.-----")
        valid_pits = get_available_moves(board, player)
        pit = input("Pick a pit number {} to sow pebbles: ".format(valid_pits))
        if (pit == "quit"):
            break
        else:
            try:
                pit = int(pit)
            except:
                print("Please provide a valid integer.")
                continue
        if (not is_plyr_house(player, pit)):
            print("Input is not a valid pit. Pick a pit {}.".format(valid_pits))
        elif (board[pit] == 0):
            print("There are no pebbles in the pit that you have chosen. Please pick a valid pit.")
        else:
            break
    return pit


# Given a valid pit, distribute the pebbles in pit one at a time to subsequent
# pits taking into account the player, meaning that the function should skip
# the opponent's store.
# @param pit {int} Pit from which pebbles are distributed
# @param board {list} Board model
# @param player {int} Player (0 or 1)
# @param ai_opt {bool} True if AI is on
# @return {pit} Last pit to receive a pebble
def distr_pebbles(pit, board, player, ai_opt):
    stones = board[pit]
    board[pit] = board[pit] - stones
    if ai_opt == False:
        display_board(board)
    while stones > 0:
        pit = pit + 1
        stones = stones - 1
        if player == 0:
            if pit == 13:
                pit = pit + 1
        else:
            if pit == 6:
                pit = pit + 1
        if pit > 13:
            pit = pit % 14
        board[pit] = board[pit] + 1
        if ai_opt == False:
            display_board(board)
    return pit


# Runs a turn for one player move.
# @param pit {int} Pit index at which to start turn (i.e. start by distributing)
#                   pebbles from this pit
# @param board {list} Board model at the start of the turn
# @param player {int} Player, can only be 0 or 1
# @param ai_opt {bool} True if AI is on for the current game
# @return {list} Board model at the end of the turn
def run_turn(pit, board, player, ai_opt):
    # TODO
    if ai_opt == False:
        ##ADDED DEEP COPY
        new_board = board[:]
        board = new_board
        lasthouse = distr_pebbles(pit, new_board, player, ai_opt)
        # makes sure not to take all pebbles from store if lastpit = store
        """if lasthouse == 6:
            return board
        elif lasthouse == 13:
            return board
        else:
            # check if last house to receive pebbles contains more pebbles
            # not including the pebble you dropped into it
            # while board[lasthouse] - 1 != 0:
            newlasthouse = distr_pebbles(lasthouse, new_board, player, ai_opt)
            # updates last pit
            board = new_board
            lasthouse = newlasthouse
            if lasthouse == 6:
                return board
            if lasthouse == 13:
                return board"""
        return board, lasthouse

    else:  # AI is running
        new_board = board[:]
        board = new_board
        lasthouse = distr_pebbles(pit, new_board, player, ai_opt)
        """if lasthouse == 6:
            return board
        elif lasthouse == 13:
            return board
        else:
            # check if last house to receive pebbles contains more pebbles
            # not including the pebble you dropped into it
            while board[lasthouse] - 1 != 0:
                newlasthouse = distr_pebbles(lasthouse, new_board, player, ai_opt)
                # updates last pit
                board = new_board
                lasthouse = newlasthouse
                if lasthouse == 6:
                    return board
                if lasthouse == 13:
                    return board"""
        return board, lasthouse


# Switches current player to opponent if opponent has move to make and returns
# new current player.
# @param board {list} Board model
# @param player {int} Original player
# @return {int} New current player (0 or 1)
def switch_plyr(board, player):
    if player == 1:
        if has_move(board, 0) == False:
            print("Player 0 cannot move because there are no pebbles on the player's side of the board")
            return 1
        else:
            return 0
    elif player == 0:
        if has_move(board, 1) == False:
            print("Player 1 cannot move because there are no pebbles on the player's side of the board")
            return 0
        else:
            return 1


# Quits the game by printing feedback to user and destroying Tkinter window.
# @return {None}
def quit_game():
    print("Goodbye!")
    try:
        WINDOW.destroy()
    except:
        return None


################################################################################
# DO NOT MODIFY BELOW THIS LINE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
################################################################################

####################################
# Minimax: Artificial Intelligence #
####################################

def min_move_list(board):  # for humans
    move_list = []
    for i in range(0, 3):
        if board[i] != 0:
            move_list.append(i)
    for i in range(10, 13):
        if board[i] != 0:
            move_list.append(i)
    return move_list


def max_move_list(board):  # for ai
    move_list = []
    for i in range(3, 6):
        if board[i] != 0:
            move_list.append(i)
    for i in range(7, 10):
        if board[i] != 0:
            move_list.append(i)
    return move_list


def minimax(depth, player, board):
    # print("The player number is {}".format(player))
    # print("The depth of the tree is {}".format(depth))
    if depth > 5 or is_end_match(board):
        # print("The match ended with the result, {}".format((board[6] - board[13], None)))
        return (board[6] - board[13], None)  # no next move since match ended
    if player == 1:  # AI = maximizing player = 1
        bestValue = (-48, None)  # min num of pebble difference
        # print("The max moves possible is {}".format(max_move_list(board)))
        max_moves = max_move_list(board)
        if max_moves == []:
            val = minimax(depth + 1, 0, board)
            if val[0] > bestValue[0]:
                bestValue = (val[0], None)
        for move in max_move_list(board):  # for every possible move of AI
            val = minimax(depth + 1, 0, run_turn(move, board, 1, True)[0])
            if val[0] > bestValue[0]:
                bestValue = (val[0], move)
        return bestValue
    else:
        bestValue = (48, None)  # max num of pebble difference
        # print("The min moves possible is {}".format(min_move_list(board)))
        min_moves = min_move_list(board)
        if min_moves == []:
            val = minimax(depth + 1, 1, board)
            if val[0] < bestValue[0]:
                bestValue = (val[0], None)
        for move in min_moves:  # for every possible move of human
            val = minimax(depth + 1, 1, run_turn(move, board, 0, True)[0])
            if val[0] < bestValue[0]:
                bestValue = (val[0], move)
        return bestValue


def run_with_ai(board):
    player = 0
    while not is_end_match(board):
        if player == 0:
            while True:
                move = pick_pit(board, player)
                if move == 'quit':
                    break
                else:
                    board, lasthouse = run_turn(move, board, player, False)
                    if lasthouse != 6:
                        break
        elif player == 1:
            print("-----It is now the computer's turn-----")
            move = minimax(0, 1, board)[1]
            if move:  # if there's a next move
                print("The computer has chosen pit number {}".format(move))
                board, lasthouse = run_turn(move, board, player, False)
        player = switch_plyr(board, player)
        display_board(board)
    if is_end_match(board):
        is_win(board)
        ans = input("Press enter to continue or type 'quit' to quit.")
        if ans == 'quit':
            quit_game()
            return None
        else:
            run_game(True)
    else:
        quit_game()
        return None


################################################################################
# BOT PLAY ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
################################################################################

## start first ##
def end_in_place(board):
    for i in range(6):
        if board[5 - i] == i + 1:
            return 5 - i
    return None


## start second ##
def end_in_place_sec(board):
    for i in range(6):
        if board[12 - i] == i + 1:
            return 12 - i
    return None


# checks if a we can eat the opponent#
def possible_eat(board):
    for i in range(6):
        if board[11 - i] == 1:
            return i
    return None


def possible_eat_sec(board):
    for i in range(6):
        if board[i] == 1:
            return 11 - i
    return None


# if wasn't succeeded, check if we can score
def last_option(board):
    max = -1
    for i in range(6):
        if ((6 - i) - board[i]) < max and (6 - board[i]) <= 0:
            max = i
    if max == -1:
        return None
    return max


def last_option_sec(board):
    max = -1
    for i in range(6):
        if ((6 - i) - board[i + 6]) < max and (6 - board[i]) <= 0:
            max = i
    if max == -1:
        return None
    return max + 6


# choose one
def no_option(board):
    for i in range(6):
        if board[i] != 0:
            return i


def no_option_sec(board):
    for i in range(6):
        if board[i + 7] != 0:
            return i + 7


def if_bot(player, board):
    if player == 0:
        pit = end_in_place(board)
        if pit and board[pit] != 0:
            print(1)
            return pit
        else:
            pit = possible_eat(board)
            if pit and board[pit] != 0:
                print(2)
                return pit
            else:
                pit = last_option(board)
                if pit and board[pit] != 0:
                    print(3)
                    return pit
        # print(no_option(board))
        # print(4)
        return no_option(board)
    if player == 1:
        pit = end_in_place_sec(board)
        if pit and board[pit] != 0:
            return pit
        else:
            pit = possible_eat_sec(board)
            if pit and board[pit] != 0:
                return pit
            else:
                pit = last_option_sec(board)
                if pit and board[pit] != 0:
                    return pit
        return no_option_sec(board)


def run_with_bot(board, bot_play):
    if bot_play == 1:
        player = 0
        while not is_end_match(board):
            if player == 0:
                while True:
                    move = pick_pit(board, player)
                    if move == 'quit':
                        break
                    else:
                        board, lasthouse = run_turn(move, board, player, False)
                        if lasthouse != 6:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            elif player == 1:
                print("-----It is now the computer's turn-----")
                while True:
                    move = if_bot(1, board)
                    if move:  # if there's a next move
                        print("The computer has chosen pit number {}".format(move))
                        board, lasthouse = run_turn(move, board, player, False)
                        if lasthouse != 13:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            player = switch_plyr(board, player)
            # display_board(board)
        if is_end_match(board):
            is_win(board)
            ans = input("Press enter to continue or type 'quit' to quit.")
            if ans == 'quit':
                quit_game()
                return None
            else:
                run_game(True)
        else:
            quit_game()
            return None
    else:
        player = 0
        while not is_end_match(board):
            if player == 0:
                print("-----It is now the computer's turn-----")
                while True:
                    move = if_bot(0, board)
                    if move + 1:  # if there's a next move
                        print("The computer has chosen pit number {}".format(move))
                        board, lasthouse = run_turn(move, board, player, False)
                        print(lasthouse)
                        if lasthouse != 6:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            elif player == 1:
                while True:
                    move = pick_pit(board, player)
                    if move == 'quit':
                        break
                    else:
                        board, lasthouse = run_turn(move, board, player, False)
                        if lasthouse != 13:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            player = switch_plyr(board, player)
            # display_board(board)
        if is_end_match(board):
            is_win(board)
            ans = input("Press enter to continue or type 'quit' to quit.")
            if ans == 'quit':
                quit_game()
                return None
            else:
                run_game(True)
        else:
            quit_game()
            return None


################################################################################
# GENETIC ALGORITHM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
################################################################################
import main as algo


def run_genetic_with_ai(board, bot, bot_play):
    if bot_play == 0:
        player = 0
        while not is_end_match(board):
            if player == 0:
                while True:
                    move = algo.choose_move(bot, board, 0)
                    if move + 1:  # if there's a next move
                        board, lasthouse = run_turn(move, board, player, False)
                        print(lasthouse)
                        if lasthouse != 6:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            elif player == 1:
                move = minimax(0, 1, board)[1]
                if move:  # if there's a next move
                    board, lasthouse = run_turn(move, board, player, False)
            player = switch_plyr(board, player)
            # if is_end_match(board):
            #     return board
            # else:
            #     quit_game()
            #     return board
        return board
    else:
        player = 0
        while not is_end_match(board):
            if player == 0:
                move = minimax(0, 0, board)[1]
                if move:  # if there's a next move
                    board, lasthouse = run_turn(move, board, player, False)
            elif player == 1:
                while True:
                    ## here ##
                    ## here ##
                    move = algo.choose_move(bot, board, 1)
                    if move:  # if there's a next move
                        board, lasthouse = run_turn(move, board, player, False)
                        if lasthouse != 13:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            player = switch_plyr(board, player)
        if is_end_match(board):
            return board
        else:
            quit_game()
            return board


def run_genetic_with_if(board, bot, bot_play):
    if bot_play == 0:
        player = 0
        while not is_end_match(board):
            if player == 0:
                while True:
                    move = algo.choose_move(bot, board, 0)
                    if move + 1:  # if there's a next move
                        board, lasthouse = run_turn(move, board, player, False)
                        print(lasthouse)
                        if lasthouse != 6:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            elif player == 1:
                while True:
                    move = if_bot(1, board)
                    if move:  # if there's a next move
                        board, lasthouse = run_turn(move, board, player, False)
                        if lasthouse != 13:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            player = switch_plyr(board, player)
            # if is_end_match(board):
            #     return board
            # else:
            #     quit_game()
            #     return board
        return board
    else:
        player = 0
        while not is_end_match(board):
            if player == 0:
                while True:
                    move = if_bot(0, board)
                    if move + 1:  # if there's a next move
                        board, lasthouse = run_turn(move, board, player, False)
                        if lasthouse != 6:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            elif player == 1:
                while True:
                    ## here ##
                    ## here ##
                    move = algo.choose_move(bot, board, 1)
                    if move:  # if there's a next move
                        board, lasthouse = run_turn(move, board, player, False)
                        if lasthouse != 13:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            player = switch_plyr(board, player)
        if is_end_match(board):
            return board
        else:
            quit_game()
            return board


def run_with_genetic(board, bot, bot_play, ai_opt, bot_opt):
    if ai_opt == True:
        run_genetic_with_ai(board, bot, bot_play)
    if bot_opt == True:
        run_genetic_with_if(board, bot, bot_play)

    if bot_play == 1:
        player = 0
        while not is_end_match(board):
            if player == 0:
                while True:
                    move = pick_pit(board, player)
                    if move == 'quit':
                        break
                    else:
                        board, lasthouse = run_turn(move, board, player, False)
                        if lasthouse != 6:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            elif player == 1:
                print("-----It is now the computer's turn-----")
                while True:
                    ## here ##
                    ## here ##
                    move = algo.choose_move(bot, board, 1)
                    if move:  # if there's a next move
                        print("The computer has chosen pit number {}".format(move))
                        board, lasthouse = run_turn(move, board, player, False)
                        if lasthouse != 13:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            player = switch_plyr(board, player)
            # display_board(board)
        if is_end_match(board):
            return board
        else:
            quit_game()
            return board
    else:
        player = 0
        while not is_end_match(board):
            if player == 0:
                print("-----It is now the computer's turn-----")
                while True:
                    move = algo.choose_move(bot, board, 0)
                    if move + 1:  # if there's a next move
                        print("The computer has chosen pit number {}".format(move))
                        board, lasthouse = run_turn(move, board, player, False)
                        if lasthouse != 6:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            elif player == 1:
                while True:
                    move = pick_pit(board, player)
                    if move == 'quit':
                        break
                    else:
                        board, lasthouse = run_turn(move, board, player, False)
                        if lasthouse != 13:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            player = switch_plyr(board, player)
            # display_board(board)
        if is_end_match(board):
            return board
        else:
            quit_game()
            return board


################################################################################
# DO NOT MODIFY ABOVE THIS LINE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
################################################################################

def steal_pebbles(player, board, lasthouse):
    if is_plyr_house(player, lasthouse) and board[lasthouse] == 1:
        mirrored_house = 12 - lasthouse
        opp_pebbles = board[mirrored_house]
        if opp_pebbles != 0:
            house = 6 + 7 * player
            board[house] += (1 + opp_pebbles)
            board[lasthouse] = 0
            board[mirrored_house] = 0
    return board


# Starts and runs game until player quits.
# @param ai_opt {bool} True if AI is on for this game, False for two player game
# @return {None}
def run_game(ai_opt, bot_opt, bot_play, bot=None):
    board = new_board()
    display_board(board)
    if bot:
        run_with_genetic(board, bot, bot_play, ai_opt, bot_opt)
    if ai_opt == True:
        run_with_ai(board)
    if bot_opt == True:
        run_with_bot(board, 0)
    elif ai_opt == False:
        print(PLAY_MESSAGE)  # game start message
        player = 0
        while not is_end_match(board):  # while there are still moves left
            if player == 0:
                while True:
                    move = pick_pit(board, player)
                    if move == 'quit':
                        break
                    else:
                        board, lasthouse = run_turn(move, board, player, False)
                        if lasthouse != 6:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            elif player == 1:
                while True:
                    moves = pick_pit(board, player)
                    if moves == "quit":
                        break
                    else:
                        board, lasthouse = run_turn(moves, board, player, False)
                        if lasthouse != 13:
                            board = steal_pebbles(player, board, lasthouse)
                            display_board(board)
                            break
            # switches players once one player has finished their move
            player = switch_plyr(board, player)
        if is_end_match(board) == True:
            is_win(board)  # checks if there is a win
            ans = input("Press enter to continue or type 'quit' to quit.")
            if ans == 'quit':
                quit_game()
                return None


if __name__ == '__main__':
    run_game(False, True)
