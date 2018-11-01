#!/usr/bin/env python3

import re
import os
import sys
import argparse

import compare_bots

"""hlt_gym.py: An enhanced Halite II gym for comparing bots."""

__author__ = "Ryan Lee"
__copyright__ = "Copyright 2017, Two Sigma and Ryan Lee"
__credits__ = ["David M. Li", "Jaques Clapauch", "Ryan Lee"]
__date__ = "August 1, 2017"
__license__ = "MIT"
__status__ = "Production"
__version__ = "1.5"

help_str=""
usage_str=""

def _parse_arguments():
    """
    Simple argparser
    :return: parsed arguments if any. Prints help otherwise
    """
    parser = argparse.ArgumentParser(description="A Halite III gym for comparing bots.\nPrints wins in a table and marks terminated bots with a \"!T!\" next to the number.")
    # .Modes.Gym
    # parser = add_parser('gym', help='Train your Bot(s)!')
    parser.add_argument('-r', '--run-command', dest='run_commands', action='append', type=str, required=True,
                            help="The command to run a specific bot. You may pass either 2 or 4 of these arguments")
    parser.add_argument('-b', '--binary', dest='halite_binary', action='store', type=str,
                            help="The halite executable/binary path, used to run the games. If unspecified it will default to looking in the current directory")

    parser.add_argument('-W', '--width', dest='map_width', action='store', type=int, default=0,
                            help="The map width the simulations will run in. If unspecified, the gym will sample randomly from the size distribution used on the game servers")
    parser.add_argument('-H', '--height', dest='map_height', action='store', type=int, default=0,
                            help="The map height the simulations will run in")
    parser.add_argument('-i', '--iterations', dest='iterations', action='store', type=int,  default=200,
                            help="Number of games to be run")
    parser.add_argument('-t', '--no-timeout', dest='timeouts', action='store_true',
                            help="Disable timeouts for bots")
    parser.add_argument('--no-replay', dest='noreplay', action='store_true',
                            help="Disable saving of replays and logs")
    return_result=parser.parse_args()
    global help_str
    global usage_str
    help_str=parser.format_help()
    usage_str=parser.format_usage()
    return return_result


def main():
    """
    Main function gets the args input and determines which method to call to handle. Handles exceptions from
    malformed input.
    :return: Nothing
    """
    args = _parse_arguments()
    if not(len(args.run_commands)==2 or len(args.run_commands)==4):
        sys.stderr.write("Error: You must specify 2 or 4 bots to compare.\n")
        exit(-1)
    if args.halite_binary is None:
        if sys.platform=="win32":
            args.halite_binary="halite.exe"
        else:
            args.halite_binary="./halite"
    if not os.path.isfile(args.halite_binary):
        sys.stderr.write(usage_str)
        sys.stderr.write("Error: Unable to locate halite binary.\n")
        sys.stderr.write("If it is not in the current directory, did you forget to specify a -b option?")
        exit(-1)
    if (args.map_width==0) != (args.map_height==0):
        sys.stderr.write(usage_str)
        sys.stderr.write("Error: Map width and height "
                         "must be specified together.\n")
        exit(-1)
    add_args=list()
    if args.timeouts:
        add_args.append("--no-timeout")
    if args.map_height!=0 and args.map_width!=0:
        add_args.append("--width {} --height {}".format(
            args.map_width, args.map_height))
    if args.noreplay:
        add_args.append("--no-replay")
        add_args.append("--no-logs")
    # Random unsigned int
    compare_bots.play_games(args.halite_binary, ".", args.run_commands,
                            args.iterations, add_args)


if __name__ == "__main__":
    main()
