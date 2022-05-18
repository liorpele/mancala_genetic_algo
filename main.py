import random
import itertools
import mancala as man

NUM_BOT_GEN = 10
NUM_GEN = 20
class MancalaGenetic:
    def __init__(self):
        self.gen_zero = []
        for i in range(NUM_BOT_GEN):
            a = random.random()
            b = random.uniform(0, 1-a)
            c = random.uniform(0, 1-a-b)
            d = 1-a-b-c
            self.gen_zero.append([a,b,c,d])

    def get_gen_zero(self):
        return self.gen_zero

    ## this part generate the new generation
    def fitness(self):
        pass

    # def crossover(self, bot_1, bot_2):
    #     ## this method switch between the two parents
    #     num = random.randint(0,3)
    #     child = bot_1[:num] + bot_2[num:]
    #     return child

    def crossover(self, bot_1, bot_2):
        ## this method randomly choose the new argoment in the middle of the two parents
        child = []
        for i in range(3):
            child.append(random.uniform(bot_1[i], bot_2[i]))
        return child

    def next_gen(self, gen):
        next_gen = []

        ####  MARRIAGE
        fitness_dict = {}
        fitness_lst = []
        for ob in gen:
            fit = self.fittness_play(ob)
            fitness_dict[fit] = ob
            fitness_lst.append(fit)
        fitness_lst.sort()
        fitness_lst.reverse()
        sorted_gen = []
        for i in range(len(gen)):
            sorted_gen.append(fitness_dict[fitness_lst[i]])

        ## the best 10% go on to the next gen.
        ## the best 40% create 50% of the cuple. and the other choosen randomly
        best_10 = len(gen)//10
        next_gen.append(sorted_gen[:best_10])

        # for i in range(best_10*4):
        combination = list(itertools.combinations(sorted_gen[:best_10*4], 2))
        random_lst = random.sample(range(0, len(combination)), best_10*5)
        for i in range(len(random_lst)):
            next_gen.append(self.crossover(combination[random_lst[i]][0],combination[random_lst[i]][1]))
        combination = list(itertools.combinations(sorted_gen, 2))
        random_lst = random.sample(range(0, len(combination)), best_10 * 4)
        for i in range(len(random_lst)):
            next_gen.append(self.crossover(combination[random_lst[i]][0],combination[random_lst[i]][1]))

        ###  MUTATION
        num_mut = random.random()
        random_lst = random.sample(range(0, len(next_gen)), int(num_mut*len(next_gen)))
        for i in range(len(random_lst)):
            next_gen[random_lst[i]] = self.mutation(next_gen[random_lst[i]])

        return next_gen

    def mutation(self, ob):
        sigma = 0.25
        new_ob = []
        for i in range(4):
            new_ob.append(random.gauss(ob[i], sigma))
        return new_ob


    ## this part play the game
    def fittness_play(self, bot):
        ### play first ###
        "to add if you cant do the move the score is 0"
        score = 0
        board = man.run_game(False, True, 0, bot)
        score += board[6]
        # board = mancala.run_game(False, False, 1, bot)
        # score += board[13]
        print(score)
        return score



def choose_move(args, board, first):
    "go over all the function and choose the "
    best_move = 0
    max_score = 0
    if first == 0:
        for move in range(6):
            score = score_of_one_move(board, move, args, first)
            if max_score < score:
                best_move = move
                max_score = score
    else:
        for move in range(6):
            score = score_of_one_move(board, move + 7, args, first)
            if max_score < score:
                best_move = move + 7
                max_score = score
    return best_move


def score_of_one_move(board, move, args, first):
    new_board = simulate_turn(board, move)
    score = args[0] *num_in_my_side(new_board) + args[1] *num_marb_in_place(new_board) +  args[2]*eating_score(board,move, first)+ args[3]*more_turns(board,move,first)
    return score


def num_in_my_side(board):
    "return the number of marbles in his side"
    sum = 0
    for i in range(6):
        sum += board[i]
    return sum


def num_marb_in_place(board):
    "return the number of marbles in the big pit"
    return board[6]

def eating_score(board, move, starter):
    if board[(board[move] + move)%12] == 0:
        if board[12 - board[board[move] + move]] == 1:
            return 10
    return 0
    # def possible_eat_sec(board):
    #     if board[board[move] + move] == 0:
    #         if board[12 - board[board[move] + move]] == 1:
    #             return 10
    #     return None

def more_turns(board, move, starter):
    board_copy = simulate_turn(board, move)
    counter = 0
    if starter == 1:
        for i in range(5, -1):
            if board_copy[i] == 6 - i:
                counter += 1
        return counter

    elif starter == 0:
        for i in range(12, 6):
            if board_copy[i] == 13 - i:
                counter += 1
        return counter

def simulate_turn(board, move):
    board_copy = []
    for i in range(13):
        board_copy.append(board[i])
    for i in range(move + 1, move + 1 + board[move]):
        board_copy[i % 12] += 1
    return board_copy


if __name__ == '__main__':
    mancala = MancalaGenetic()
    gen = mancala.get_gen_zero()
    for generation in range(NUM_GEN):
        gen = mancala.next_gen(gen)
    save_gen = gen

