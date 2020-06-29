import re
import random
import operator as op


def init_new_game():
    global end_game, list_str_game, list_num_game

    end_game = False
    list_str_game = [" "] * 9
    list_num_game = [num_codes[c] for c in list_str_game]


def print_game():
    print("---------")
    for i in range(3):
        print("| " + " ".join(list_str_game[(3 * i):(3 * i + 3)]) + " |")
    print("---------")
    test_result_game()


def get_random_ai_position():
    free_positions = [i for i, val in enumerate(list_num_game) if not val]
    return random.choice(free_positions)


def get_medium_ai_position():
    win_pos = None
    for positions in test_positions:
        sum_line = sum(list_num_game[pos] for pos in positions)
        if abs(sum_line) == 2:
            win_pos = sum(pos for pos in positions if not list_num_game[pos])
            break

    return win_pos


def get_hard_ai_position():

    best_move = min_max_search(list_num_game[:], ai_player)
    return best_move[1]


def min_max_search(list_game, player):

    def check_win():
        win_sum = 0
        for positions in test_positions:
            sum_line = sum(list_game[pos] for pos in positions)
            if abs(sum_line) == 3:
                win_sum = sum_line
                break

        win_player = win_sum / 3
        return win_player

    player_win = check_win()
    if player_win == ai_player:
        return (100, )
    elif player_win == -1 * ai_player:
        return (-100, )
    elif all(list_game):
        return (0, )

    moves_list = []
    for free_pos in (i for i, val in enumerate(list_game) if val == 0):
        new_list_game = list_game[:]
        new_list_game[free_pos] = player

        move = min_max_search(new_list_game, player * -1)
        moves_list.append((move[0], free_pos))

    if player == ai_player:
        best_move = max(moves_list, key=op.itemgetter(0))
    else:
        best_move = min(moves_list, key=op.itemgetter(0))

    return best_move


def get_user_position(position):
    col, row = map(int, position.split())
    flat_index = 3 * (3 - row) + (col - 1)
    return flat_index


def make_user_move():
    user_coordinates = input("Enter the coordinates: ")

    correct_move = True

    if re.match(r"[123] [123]", user_coordinates):
        user_position = get_user_position(user_coordinates)
        if not test_set_position(user_position):
            print("This cell is occupied! Choose another one!")
            correct_move = False
    elif re.match(r"\d \d", user_coordinates):
        print("Coordinates should be from 1 to 3!")
        correct_move = False
    else:
        print("You should enter numbers!")
        correct_move = False

    return correct_move


def make_easy_move():
    make_ai_move("easy")


def make_medium_move():
    make_ai_move("medium")


def make_hard_move():
    make_ai_move("hard")


def make_ai_move(level):
    ai_position = 0
    if level == "easy":
        ai_position = get_random_ai_position()
    elif level == "medium":
        ai_position = get_medium_ai_position()
        if ai_position is None:
            ai_position = get_random_ai_position()
    elif level == "hard":
        ai_position = get_hard_ai_position()

    print(f'Making move level "{level}"')
    test_set_position(ai_position)


def test_set_position(index):
    global list_str_game, list_num_game

    free_pos = False

    if list_str_game[index] == " ":
        free_pos = True
        symbol = "O" if sum(list_num_game) else "X"

        list_str_game[index] = symbol
        list_num_game[index] = num_codes[symbol]

        print_game()

    return free_pos


def test_result_game():
    global list_str_game, list_num_game, end_game

    win_pos = None
    for positions in test_positions:
        sum_line = sum(list_num_game[pos] for pos in positions)
        if abs(sum_line) == 3:
            win_pos = positions[0]
            break

    if win_pos is not None or all(list_num_game):

        end_game = True

        if win_pos is not None:
            print(f"{list_str_game[win_pos]} wins")
        else:
            print("Draw")


ai_player = None
end_game = False
num_codes = {"X": 1, "O": -1, " ": 0}
test_positions = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                  (0, 3, 6), (1, 4, 7), (2, 5, 8),
                  (0, 4, 8), (2, 4, 6))

list_str_game = []
list_num_game = []


moves = {"user": make_user_move,
         "easy": make_easy_move,
         "medium": make_medium_move,
         "hard": make_hard_move}

while True:

    user_input = input("Input command: ")

    if user_input == "exit":
        break
    elif not re.match(r"start (user|easy|medium|hard) (user|easy|medium|hard)", user_input):
        print("Bad parameters!")
    else:
        _, first_player, second_player = user_input.split()

        first_player_move = moves[first_player]
        second_player_move = moves[second_player]
        is_first = True

        init_new_game()
        print_game()

        if first_player != "user":
            ai_player = 1
        elif second_player != "user":
            ai_player = -1

        while not end_game:
            if is_first:
                first_player_move()
            else:
                second_player_move()

            is_first = not is_first

        print()
