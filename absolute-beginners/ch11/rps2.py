import random
import json
import os
import datetime
from colorama import Fore
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, Completer, Completion

rolls = {}


def main():
    print(Fore.WHITE)
    log("App starting up ...")
    load_rolls()
    show_header()
    show_leaderboard()
    player1, player2 = get_players()
    log(f"{player1} has logged in.")
    play_game(player1, player2)
    log("Game over!")


def show_header():
    print(Fore.LIGHTMAGENTA_EX)
    print("--------------------------")
    print("-   Rock Paper Scissors  -")
    print("- Error Handling Edition -")
    print("--------------------------")
    print(Fore.WHITE)


def show_leaderboard():
    leaders = load_leaders()
    sorted_leaders = list(leaders.items())
    sorted_leaders.sort(key=lambda l: l[1], reverse=True)

    print()
    print("---------------------------")
    print("LEADERS")
    for name, wins in sorted_leaders[0:5]:
        print(f"{wins:,} -- {name}")
    print()
    print("---------------------------")
    print()


def get_players():
    p1 = input("Player 1, what is your name? ")
    p2 = "Computer"
    return p1, p2


def play_game(player_1, player_2):
    log(f"New game starting between {player_1} and {player_2}.")
    wins = {player_1: 0, player_2: 0}
    roll_names = list(rolls.keys())

    while not find_winner(wins, wins.keys()):

        roll1 = get_roll(player_1, roll_names)
        roll2 = random.choice(roll_names)

        if not roll1:
            print(Fore.LIGHTRED_EX + "Try again!")
            print(Fore.WHITE)
            continue

        log(f"{player_1} rolls {roll1} and {player_2} rolls {roll2}")
        print(Fore.YELLOW + f"{player_1} rolls {roll1}")
        print(Fore.LIGHTBLUE_EX + f"{player_2} rolls {roll2}")
        print(Fore.WHITE)

        winner = check_for_winning_throw(player_1, player_2, roll1, roll2)

        if winner is None:
            msg = "This round was a tie!"
            print(msg)
            log(msg)
        else:
            msg = f"{winner} takes the round!"
            print(Fore.GREEN + msg)
            print(Fore.WHITE)
            log(msg)
            wins[winner] += 1

        msg = f"Score is {player_1}: {wins[player_1]} and {player_2}: {wins[player_2]}."
        print(msg)
        log(msg)
        print()

    overall_winner = find_winner(wins, wins.keys())
    msg = f"{overall_winner} wins the game!"
    fore = Fore.GREEN if overall_winner == player_1 else Fore.LIGHTRED_EX
    print(fore + msg)
    print(Fore.WHITE)
    log(msg)
    record_win(overall_winner)


def find_winner(wins, names):
    best_of = 3
    for name in names:
        if wins.get(name, 0) >= best_of:
            return name
    return None


def check_for_winning_throw(player_1, player_2, roll1, roll2):
    winner = None
    if roll1 == roll2:
        print("The play was tied!")
    outcome = rolls.get(roll1, {})
    if roll2 in outcome.get('defeats'):
        return player_1
    elif roll2 in outcome.get('defeated_by'):
        return player_2
    return winner


def get_roll(player_name, roll_names):
    print(f"Available rolls: {','.join(roll_names)}")
    #    for index, r in enumerate(rolls, start=1):
    #        print(f"{index}. {r}")

    #    selected_index = int(input(f"{player_name}, what is your roll? ")) - 1
    # word_comp = WordCompleter(roll_names)
    word_comp = PlayComplete()

    roll = prompt(f"{player_name}, what is your roll: ", completer=word_comp)

    if not roll or roll not in roll_names:
        print(f"Sorry {player_name}, {roll} is not valid!")
        return None

    return roll


# def get_roll(player_name, roll_names):
#    print("Available rolls:")
#    for index, r in enumerate(rolls, start=1):
#        print(f"{index}. {r}")
#
#    selected_index = int(input(f"{player_name}, what is your roll? ")) - 1
#    if selected_index < 0 or selected_index >= len(rolls):
#        print(f"Sorry {player_name}, {selected_index + 1} is out of bounds!")
#        return None
#
#    return roll_names[selected_index]

def load_rolls():
    global rolls

    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'rolls.json')

    # filename = 'rolls.json'
    # fin = open(filename, 'r', encoding='utf-8')
    # rolls = json.load(fin)
    # fin.close()

    with open(filename, 'r', encoding='utf-8') as fin:
        rolls = json.load(fin)

    log(f"Loaded rolls: {list(rolls.keys())} from {os.path.basename(filename)}.")


def load_leaders():
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'leaderboard.json')

    if not os.path.exists(filename):
        return {}

    with open(filename, 'r', encoding='utf-8') as fin:
        return json.load(fin)


def record_win(winner_name):
    leaders = load_leaders()

    leaders[winner_name] = leaders.get(winner_name, 0) + 1

    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'leaderboard.json')

    with open(filename, 'w', encoding='utf-8') as fout:
        json.dump(leaders, fout)


def log(msg):
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'rps.log')

    with open(filename, 'a', encoding='utf-8') as fout:
        prefix = f"[{datetime.datetime.now().isoformat()}] - "
        fout.write(prefix + msg + "\n")


class PlayComplete(Completer):
    def get_completions(self, document, complete_event):
        roll_names = list(rolls.keys())
        word = document.get_word_before_cursor()
        complete_all = not word if not word.strip() else word == '.'
        completions = []

        for roll in roll_names:
            is_substring = word in roll
            if complete_all or is_substring:
                completion = Completion(
                    roll,
                    start_position=- len(word),
                    style="fg:white bg:darkgreen",
                    selected_style="fg:yellow bg:green")
                completions.append(completion)

        return completions


if __name__ == '__main__':
    main()
