import time
import heapq

goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)  
movements = ((-1, 0), (1, 0), (0, -1), (0, 1))   

def get_neighbors(state):

    zero_index = state.index(0)
    zero_row, zero_col = zero_index // 3, zero_index % 3
    neighbors=[]
    for dr, dc in movements:
        new_row, new_col = zero_row + dr, zero_col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            neighbor = list(state)
            neighbor[zero_index], neighbor[new_index] = neighbor[new_index], neighbor[zero_index]
            neighbors.append(tuple(neighbor))

    return neighbors

def check_goal(state):
    return state == goal_state

##---------------------------------------BFS-----------------------------------------

def bfs(start):
    
    visited = set()
    queue = [(start, [])]
    nodes_visited = 0  
    start_time = time.time()  
    while queue:
        current_state, path = queue.pop(0)
        nodes_visited += 1
        if(check_goal(current_state)):
            end_time = time.time()  
            time_taken = end_time - start_time 
            return path, nodes_visited, time_taken  
        visited.add(current_state)
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return None


##---------------------------------------DFS-----------------------------------------

def dfs(start):
    visited = set()
    nodes_visited = 0  
    start_time = time.time()
    stack = [(start, [])]
    while stack:
        current_state, path = stack.pop()
        nodes_visited += 1
        if(check_goal(current_state)):
            end_time = time.time()  
            time_taken = end_time - start_time 
            return path, nodes_visited, time_taken
        visited.add(current_state)
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    return None 


##---------------------------------------IDFS-----------------------------------------
def dfs_algo(start,max_depth,visited,path):
    
    nodes_visited = 0  
    start_time = time.time()
    stack = [(start, [])]
    while stack:
        current_state,path = stack.pop()
        nodes_visited += 1
        if(check_goal(current_state)):
            end_time = time.time()  
            time_taken = end_time - start_time 
            return path, nodes_visited, time_taken
        if(max_depth<=0 and not stack):
            return None
        visited.add(current_state)
        if(max_depth>0):
            for neighbor in get_neighbors(current_state):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
            max_depth-=1    
    return None 




def idfs(start,max_depth):
    
    for i in range(max_depth):
        visited=set()
        path=[]
        result=dfs_algo(start,i,visited,path)
        if result is not None:
            return result
            
    return None
   



##---------------------------------------UCS-----------------------------------------


def ucs(start):
    visited = set()
    priority_queue = [(0, start, [])]  
    nodes_visited = 0
    start_time = time.time()
    while priority_queue:
        current_cost, current_state, path = heapq.heappop(priority_queue)
        nodes_visited += 1
        if check_goal(current_state):
            end_time = time.time()
            time_taken = end_time - start_time
            return path, nodes_visited, time_taken
        visited.add(current_state)
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                new_cost = current_cost + 1  # Uniform cost for all transitions
                heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))
    return None


def validate_input(user_input):
    
    numbers = user_input.split(',')
    seen = set()
    for num in numbers:
        try:
            num_int = int(num)
            if len(numbers) != 9:
                return False
            if num_int < 0 or num_int > 8:
                return False
            if num_int in seen:
                return False
            seen.add(num_int)
        except ValueError:
            return False
    return True


def bfs_menu():
    user_input = input("Enter numbers separated by commas (between 0 and 9): ")
    while not validate_input(user_input):
        print("Invalid input. Please enter numbers between 0 and 9 separated by commas.")
        user_input = input("Enter numbers separated by commas (between 0 and 9): ")

    initial_state = tuple(map(int, user_input.split(',')))
    print("Input tuple:", initial_state)
    result = bfs(initial_state)
    if result is not None:
        solution, nodes_visited, time_taken = result
        print("Solution Found:")
        for i, state in enumerate(solution):
            print(f"Step {i + 1}:")
            for j in range(0, 9, 3):
                print(state[j:j+3])
            print()
        print("Path Cost:", len(solution))
        print("Nodes visited:", nodes_visited)
        print("Time taken:", time_taken, "seconds")
    else:
        print("No solution found.")

def dfs_menu():
    user_input = input("Enter numbers separated by commas (between 0 and 9): ")
    while not validate_input(user_input):
        print("Invalid input. Please enter numbers between 0 and 9 separated by commas.")
        user_input = input("Enter numbers separated by commas (between 0 and 9): ")

    initial_state = tuple(map(int, user_input.split(',')))
    print("Input tuple:", initial_state)
    result = dfs(initial_state)
    if result is not None:
        solution, nodes_visited, time_taken = result
        print("Solution Found:")
        for i, state in enumerate(solution):
            print(f"Step {i + 1}:")
            for j in range(0, 9, 3):
                print(state[j:j+3])
            print()
        print("Path Cost:", len(solution))
        print("Nodes visited:", nodes_visited)
        print("Time taken:", time_taken, "seconds")
    else:
        print("No solution found.")

def idfs_menu():
    user_input = input("Enter numbers separated by commas (between 0 and 9): ")
    while not validate_input(user_input):
        print("Invalid input. Please enter numbers between 0 and 9 separated by commas.")
        user_input = input("Enter numbers separated by commas (between 0 and 9): ")

    initial_state = tuple(map(int, user_input.split(',')))
    print("Input tuple:", initial_state)
    result = idfs(initial_state, 1000)
    if result is not None:
        solution, nodes_visited, time_taken = result
        print("Solution Found:")
        for i, state in enumerate(solution):
            print(f"Step {i + 1}:")
            for j in range(0, 9, 3):
                print(state[j:j+3])
            print()
        print("Path Cost:", len(solution))
        print("Nodes visited:", nodes_visited)
        print("Time taken:", time_taken, "seconds")
    else:
        print("No solution found within the specified depth.")

def ucs_menu():
    user_input = input("Enter numbers separated by commas (between 0 and 9): ")
    while not validate_input(user_input):
        print("Invalid input. Please enter numbers between 0 and 9 separated by commas.")
        user_input = input("Enter numbers separated by commas (between 0 and 9): ")

    initial_state = tuple(map(int, user_input.split(',')))
    print("Input tuple:", initial_state)
    result = ucs(initial_state)
    if result is not None:
        solution, nodes_visited, time_taken = result
        print("Solution Found:")
        for i, state in enumerate(solution):
            print(f"Step {i + 1}:")
            for j in range(0, 9, 3):
                print(state[j:j+3])
            print()
        print("Path Cost:", len(solution))
        print("Nodes visited:", nodes_visited)
        print("Time taken:", time_taken, "seconds")
    else:
        print("No solution found.")


while True:
    print("\nMenu:")
    print("1. Breadth-First Search (BFS)")
    print("2. Depth-First Search (DFS)")
    print("3. Iterative Deepening Depth-First Search (IDFS)")
    print("4. Uniform Cost Search (UCS)")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        bfs_menu()
    elif choice == "2":
        dfs_menu()
    elif choice == "3":
        idfs_menu()
    elif choice == "4":
        ucs_menu()
    elif choice == "5":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")

