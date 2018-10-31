import json
import os
import subprocess

_SPACE_DELIMITER = ' '
_BOT_ID_POSITION = 1

def _determine_winner(results):
    """
    From the game result string, extract the winner's id.
    :param game_result: The result of running a game on the Halite binary
    :return:
    """
    for player_id, stats in results["stats"].items():
        if stats["rank"] == 1:
            return player_id


def _play_game(binary, bot_commands, flags):
    """
    Plays one game considering the specified bots and the game and map constraints.
    :param binary: The halite binary
    :param bot_commands: The commands to run each of the bots
    :return: The game's result string
    """
    command = [
        binary,
        "--results-as-json"
    ]
    command.extend(flags)
    for bot_command in bot_commands:
        command.append(bot_command)
#    print(command)
    return subprocess.check_output(command).decode()


def play_games(binary, game_output_dir, bot_commands, number_of_runs, flags):
    """
    Runs number_of_runs games using the designated bots and binary, recording the tally of wins per player
    :param binary: The Halite binary.
    :param game_output_dir: Where to put replays and log files.
    :param map_width: The map width, set to None for engine random choice
    :param map_height: The map height, set to None for engine random choice
    :param bot_commands: The commands to run each of the bots (must be either 2 or 4)
    :param number_of_runs: How many runs total
    :return: Nothing
    """

    binary = os.path.abspath(binary)

    print("Comparing Bots!")
    result = {}
    if not(len(bot_commands) == 4 or len(bot_commands) == 2):
        raise IndexError("The number of bots specified must be either 2 or 4.")
    bot_names=[" #{}: '{}' ".format(i+1,cmd) for i,cmd in enumerate(bot_commands)]
    bot_names.insert(0, " #    ") # four spaces after #
    string_title="|".join(bot_names)
    string_title="|"+string_title+"|"
    print("-"*len(string_title))
    print(string_title)
    print("="*len(string_title))
    len_table_row=sum([len(b) for b in bot_commands])
    for current_run in range(0, number_of_runs):
        flags_with_rand=flags+["-s "+str(random.randint(0,4294967295))
        match_output = _play_game(binary, bot_commands, flags_with_rand)
        results = json.loads(match_output)
        winner = _determine_winner(results)
        result[winner] = result.setdefault(winner, 0) + 1
        print("| {}|".format(str(current_run+1).ljust(5)), end="")
        for i in range(1, len(bot_names)):
            print(" {}".format(result.get(str(i-1),0)).ljust(len(bot_names[i])),
                    end="")
            print("|", end="")
        print("")
    print("="*len(string_title))

#     bot_parser.add_argument('--output-dir',
#                             dest='game_output_dir',
#                             action='store',
#                             type=str, required=False,
#                             help="A path to a directory where logs and replays will be stored. If provided, use absolute paths in any bot commands.")
# 
