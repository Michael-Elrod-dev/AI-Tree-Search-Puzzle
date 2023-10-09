# AI-Tree-Search-Puzzle

This project consists of a program that aims to solve or analyze the 3x3 sliding puzzle, often referred to as the "8-puzzle". The program provides functionalities to generate puzzle states, get neighboring states, and search for solutions.

## Usage

Run the program in a Python environment:

```
python script.py
```

## Program Structure

- `script.py`: This file contains all the necessary functions to analyze and solve the sliding puzzle.

## Functions

This project consists of a program that aims to solve or analyze the 3x3 sliding puzzle, often referred to as the "8-puzzle". The program provides the following functionalities:

1. **View All States**: Display all possible states of the board.
2. **Random States with Conditions**: Show 10 random states with the condition that no two odd numbers are adjacent.
3. **Input & Action**: Users can input the initial state of the puzzle and then take an action to move the empty space.
4. **Modify for Division**: The program attempts to modify the state until all rows, when read as numbers, are divisible by 3.
5. **BFS & DFS**: Perform Breadth-First Search (BFS) and Depth-First Search (DFS) to reach a specific goal state.
6. **Uniform Cost Search**: Execute Uniform Cost Search (UCS) with two different cost structures to find a path to the goal state.

During execution, users will interact with a menu that provides these options, labeled from a to h.

- `next_state(state, action, directions)`: Determines the next state of the puzzle given the current state and an action (direction of movement).
- `check_odds(state, directions)`: Checks if there are no neighboring odd numbers in the provided state.
- `random_states(all_states, picks)`: Prints 10 randomly selected states that have no neighboring odd numbers.
- `get_neighbors(state, directions)`: Finds all possible states reachable from the current state through a single move.
- `find_all_states(start_state, search, directions, order=False, goal_state=None, state_list=None)`: Performs a search (either BFS or DFS) to find all possible states or a path to a goal state from the initial state.
- `uniform_cost_search(start_state, goal_state, directions, costs, state_list)`: Executes the Uniform Cost Search (UCS) algorithm to find the shortest path to a goal state considering various cost structures.
- `get_division(state, directions)`: Modifies the state until all rows are divisible by 3.
- `get_state()`: Prompts the user to input the initial state of the puzzle.
- `print_state(state)`: Displays the given puzzle state in a readable format.
- `initialize_logger()`: Prepares a log file to store state transitions.
- `logger(bfs_states, dfs_states, g1_states, g2_states)`: Logs the state transitions for BFS, DFS, and the two UCS approaches.
