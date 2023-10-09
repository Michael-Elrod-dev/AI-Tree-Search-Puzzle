import time
import heapq
import random

# This function takes the current state, an action, and a list of possible directions 
# and returns the next state of the puzzle
def next_state(state, action, directions):
    # Normalize the action to be within the range of 0-3
    if action > 3:
        action = action % 4
        print("action input was greater than 3. So, it was changed to", action)
    elif action <= 0:
        action = abs(action) % 4

    # Find the index of the empty spot and convert it to 2D coordinates
    zero_pos = state.index(0)
    x, y = zero_pos // 3, zero_pos % 3
    dx, dy = directions[action]
    # Add our action to the current empty position
    nx, ny = x + dx, y + dy

    # Check if the new position is within bounds and perform the move if valid
    if 0 <= nx < 3 and 0 <= ny < 3:
        new_state = state[:]
        # Swap the empty spot with the adjacent spot in the direction of the action)
        new_state[nx * 3 + ny], new_state[x * 3 + y] = new_state[x * 3 + y], new_state[nx * 3 + ny]
        return new_state
    else:
        print("Invalid move attempted")
        return state


# This function takes the current state and a list of possible directions 
# and checks whether there are no neighboring odd numbers in the state.
def check_odds(state, directions):
    global filtered
    odds = set()

    # Find all odd numbers in the state and add their coordinates to a set 
    for index, items in enumerate(state):
        if items % 2 > 0:
            x, y = index // 3, index % 3
            odds.add((x, y))
            
    # Check if there are any neighboring odd numbers in the state
    for x, y in odds:
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3 and (dx == 0 or dy == 0):
                if state[nx * 3 + ny] % 2 > 0:
                    filtered+=1
                    return False
            else:
                filtered+=1
                
    return True
    
# This function prints 10 randomly selected states that hav no neighboring odd numbers
def random_states(all_states, picks):
        state_list = []
        visited = set()
        
        # Loop until we have found the desired number of valid states
        while picks > 0:
            index = random.randint(0, len(all_states)-1)
            
            if index not in visited and check_odds(all_states[index], directions):
                visited.add(index)
                state_list.append(all_states[index])
                picks-=1
            
        return state_list

# This function takes the current state and a list of possible directions 
# and returns a list of all possible next states
def get_neighbors(state, directions):
    # Find the index of the empty spot and convert it to 2D coordinates
    zero_pos = state.index(0)
    x, y = zero_pos // 3, zero_pos % 3
    neighbors = []
    
    # Find all possible next states
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # Check if the new position is within the boundaries of the grid and not a diagonal move
        if 0 <= nx < 3 and 0 <= ny < 3 and (dx == 0 or dy == 0):
            new_state = state[:]
            # Swap the empty spot with the adjacent spot in the direction of (dx, dy)
            new_state[nx * 3 + ny], new_state[x * 3 + y] = new_state[x * 3 + y], new_state[nx * 3 + ny]
            neighbors.append(new_state)
    
    return neighbors

# This function performs a search (either BFS or DFS) to find all possible states 
# or a path to a goal state from the initial state
def find_all_states(start_state, search, directions, order=False, goal_state=None, state_list=None):
    visited = set()
    group = [(start_state, [], 0)]
    all_states = []
    start_time = time.time()
    states = 0

    # Loop until there are no more states to explore
    while group:
        states+=1
        # Check if the time limit has been reached
        if time.time() - start_time > 30:
            return None, None, states, True

        # Explore the next state
        if search == 'bfs':
            current_state, path, moves = group.pop(0)
        else:  # dfs
            current_state, path, moves = group.pop()
        current_state_tuple = tuple(current_state)
        
        if state_list is not None and search == 'bfs':
            state_list.append(current_state)
        elif state_list is not None and search == 'dfs':
            state_list.append(current_state)

        # Check if the goal state has been reached
        if order and current_state_tuple == tuple(goal_state):
            print("The goal state is:")
            print_state(current_state)
            return path + [current_state], moves, states, False

        # Explore the current state's neighbors
        if current_state_tuple not in visited:
            visited.add(current_state_tuple)
            all_states.append(current_state)

            neighbors = get_neighbors(current_state, directions)
            for neighbor in neighbors:
                group.append((neighbor, path + [current_state], moves + 1))

    if order:
        return None, None, states, False
    else:
        return all_states
    
def uniform_cost_search(start_state, goal_state, directions, costs, state_list):
    visited = set()
    priority_queue = [(0, start_state, [], 0)]  # Initialize moves to 0
    start_time = time.time()
    states = 0

    while priority_queue:
        states+=1
        if time.time() - start_time > 30:
            cost, current_state, path, moves = heapq.heappop(priority_queue)
            return None, states, True, moves

        cost, current_state, path, moves = heapq.heappop(priority_queue)
        current_state_tuple = tuple(current_state)
        state_list.append(current_state)

        if current_state_tuple == tuple(goal_state):
            return path + [current_state], states, False, moves

        if current_state_tuple not in visited:
            visited.add(current_state_tuple)
            
            neighbors = get_neighbors(current_state, directions)
            for i, neighbor in enumerate(neighbors):
                heapq.heappush(priority_queue, (cost + costs[i], neighbor, path + [current_state], moves + 1))

    return None, states, False, moves

# This function repeatedly modifies the state until all rows are divisible by 3
def get_division(state, directions):
    global filtered
    while True:
        row1 = state[0]*100 + state[1]*10 + state[2]
        row2 = state[3]*100 + state[4]*10 + state[5]
        row3 = state[6]*100 + state[7]*10 + state[8]
        
        # Check if all rows are divisible by 3 as whole numbers
        if row1%3==0 and row2%3==0 and row3%3==0:
            print_state(state)
            print("Goal state was reached")
            return state
        else:
            filtered+=1
            state = next_state(state, random.randint(-3, 0), directions)
            print_state(state)

# This function gets the inital state from the user
def get_state():
    print("Enter the current state of the puzzle in the form of a 9 digit number(0-8)")
    print("For example, the input 012345678 would result in this state:")
    print_state([0, 1, 2, 3, 4, 5, 6, 7, 8])
    
    # Loop until a valid state is entered
    while True:
        user_input = input()
        # Check if input length is 9 and contains only unique digits
        if len(user_input) == 9 and len(set(user_input)) == 9 and user_input.isdigit():
            initial_state = [int(digit) for digit in user_input]  
            # Print the state    
            print("The state is:")
            print_state(initial_state)
            return initial_state
        else:
            print("Invalid input. Please enter 9 unique digits(0-8)")
        
# Print the given puzzle state
def print_state(state):
    print("---------")
    for i in range(0, 9, 3):
        print(state[i],"|",state[i+1],"|",state[i+2])
    print("---------")

def initialize_logger():
    with open("Log_File.txt", "w") as file:
        file.write(f"{'BFS':<20}{'DFS':<20}{'G1':<20}{'G2':<20}\n")
        file.write(f"{'-'*20}{'-'*20}{'-'*20}{'-'*20}\n")

def logger(bfs_states, dfs_states, g1_states, g2_states):
    # Read the existing content and store the headers
    with open("Log_File.txt", "r") as file:
        headers = [next(file) for _ in range(2)]
    
    # Clear the file and write back the headers
    with open("Log_File.txt", "w") as file:
        file.writelines(headers)
    
    # Now append the new data
    with open("Log_File.txt", "a") as file:
        max_len = max(len(bfs_states), len(dfs_states), len(g1_states), len(g2_states))

        for i in range(max_len):
            bfs_state = ' '.join(map(str, bfs_states[i])) if i < len(bfs_states) else ''
            dfs_state = ' '.join(map(str, dfs_states[i])) if i < len(dfs_states) else ''
            g1_state = ' '.join(map(str, g1_states[i])) if i < len(g1_states) else ''
            g2_state = ' '.join(map(str, g2_states[i])) if i < len(g2_states) else ''

            file.write(f"{bfs_state:<20}{dfs_state:<20}{g1_state:<20}{g2_state:<20}\n")

initialize_logger()
bfs_states = []
dfs_states = []
g1_states = []
g2_states = []

# Define possible directions to move the empty spot
directions = [
    (0, 1),  # Right
    (1, 0),  # Down
    (0, -1), # Left
    (-1, 0)  # Up
]
# Initial state of the puzzle
initial_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# Store all possible states of the puzzle
unique_states = find_all_states(initial_state, 'bfs', directions, False, None, bfs_states)

while True:
    filtered = 0
    logger(bfs_states, dfs_states, g1_states, g2_states)
    print("!!Please refer to Log_File.txt to view all state transitions!!")
    user_input = input("Please enter the letter of the section of the assignment you'd like to check (a-h) ").lower()
    
    # All possible states of the board
    if user_input == 'a':
        ran_states = random.sample(unique_states, 10)
        for state in ran_states:
            print_state(state)
        print(".\n.\n.\n.")
        print("Total number of unique/possible states:", len(unique_states), "\n")

    # Print 10 random states of the board with no adjacent odd nunmbers
    elif user_input == 'b':
        for state in random_states(unique_states, 10):
            print_state(state)
        print("Number of states that were filtered out:",filtered, "\n")
            
    # Get the initial state of the puzzle and take an action
    elif user_input == 'c':
        initial_state = get_state()
        print("Now, please choose what the action will be")
        print("Please consider that the empty space is the space that 'moves'")
        print("Enter the number corresponding to the direction you would like to move")
        action = int(input("right:0, down:1, left:2, or up:3.\n"))
        new_state = next_state(initial_state, action, directions)
        print("The new state is:")
        print_state(new_state)
        print("\n")

    # Take random actions until all rows are divisible by 3
    elif user_input == 'd':
        get_division(get_state(), directions)
        print("Number of state transitions:",filtered, "\n")
    
    # Preform BFS and DFS to get to goal state
    elif user_input in ['e', 'f', 'g']:
        if user_input == 'g':
            goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]
        else:
            goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        initial_state = get_state()
        
        print("The goal state is:")
        print_state(goal_state)

        # Time the execution of the BFS algorithm
        print("\nChecking BFS solution...")
        start_time = time.time()
        path_bfs, moves_bfs, states_bfs, time_limit_reached_bfs = find_all_states(initial_state, 'bfs', directions, True, goal_state, bfs_states)
        bfs_time = time.time() - start_time

        # Time the execution of the DFS algorithm
        print("Checking DFS solution...")
        start_time = time.time()
        path_dfs, moves_dfs, states_dfs, time_limit_reached_dfs = find_all_states(initial_state, 'dfs', directions, True, goal_state, dfs_states)
        dfs_time = time.time() - start_time

        # Print the results for BFS
        print("\nBFS Results:")
        if time_limit_reached_bfs:
            print("The BFS search was terminated because the time limit of 30 seconds was reached")
        elif path_bfs is not None:
            print(f"The goal state was reached in {moves_bfs} moves")
            print(f"Total state transitions: {states_bfs}")
        else:
            print("The goal state could not be reached using BFS")
        print(f"BFS execution time: {bfs_time:.4f} seconds")

        # Print the results for DFS
        print("\nDFS Results:")
        if time_limit_reached_dfs:
            print("The DFS search was terminated because the time limit of 30 seconds was reached")
        elif path_dfs is not None:
            print(f"The goal state was reached in {moves_dfs} moves")
            print(f"Total state transitions: {states_dfs}")
        else:
            print("The goal state could not be reached using DFS")
        print(f"DFS execution time: {dfs_time:.4f} seconds")

        # Decide which algorithm was faster or more successful
        if path_bfs is not None and path_dfs is not None:
            if bfs_time < dfs_time:
                print("\nBFS was faster\n")
            else:
                print("\nDFS was faster\n")
        elif path_bfs is not None:
            print("\nBFS was successful in finding a solution, whereas DFS was not\n")
        elif path_dfs is not None:
            print("\nDFS was successful in finding a solution, whereas BFS was not\n")
        else:
            if time_limit_reached_bfs and time_limit_reached_dfs:
                print("Both algorithms reached the time limit\n")
            else:
                if bfs_time < dfs_time:
                    print("BFS reached a conclusion faster, but neither found a solution\n")
                else:
                    print("DFS reached a conclusion faster, but neither found a solution\n")
    
    # Perform UCS with cost differentials   
    elif user_input == 'h':
        goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        initial_state = get_state()
        
        print("The goal state is:")
        print_state(goal_state)
        
        # G1: All moves have a unit cost
        print("\nPerforming UCS with G1 cost structure...")
        costs = [1, 1, 1, 1]  # Specify the cost structure for G1 here
        start_time = time.time()
        path, g1_state, failure, g1_moves = uniform_cost_search(initial_state, goal_state, directions, costs, g1_states)
        g1_time = time.time() - start_time
        if not failure:
            print(f"The goal state was reached in {g1_moves} moves.")
            print(f"Total state transitions: {g1_state}\n")
        else:
            print("The goal state could not be reached using UCS")
        
        # G2: Different moves have different costs
        print("Performing UCS with G2 cost structure...")
        costs = [2, 0.5, 1, 1.5]  # Specify the cost structure for G2 here
        start_time = time.time()
        path, g2_state, failure, g2_moves = uniform_cost_search(initial_state, goal_state, directions, costs, g2_states)
        g2_time = time.time() - start_time
        
        if not failure:
            print(f"The goal state was reached in {g2_moves} moves.")
            print(f"Total state transitions: {g2_state}\n")
        else:
            print("The goal state could not be reached using UCS")
        print(f"G1 execution time: {g1_time:.4f} seconds")
        print(f"G2 execution time: {g2_time:.4f} seconds")
    else:
        print("Invalid input")