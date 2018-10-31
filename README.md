# Halite-III-Bot-Comparator
An enhanced bot comparator for Halite III that is equivalent to the `play` module of the hlt client tool. This tool does not have external dependencies besides of Python.

## Usage

Change directory into the `hlt_gym` folder and run the `hlt_gym.py` file.
If you would like to run the gym from any directory, you can add this directory into the PATH environmental variable.

Example usage:

```
./hlt_gym.py -r "python3 MyBotA.py" -r "python3 MyBotB.py" # Minimal usage
./hlt_gym.py -b /halite/path -r "python3 MyBotA.py" -r "python3 MyBotB.py" #Manually specify path to halite executable
```

Run `./hlt_gym.py --help` for a full list of options.

*Tip: If you are running Java bots from another directory, specify the directory using the `-cp` or `-classpath` option and specify the class file relative to that directory.*
