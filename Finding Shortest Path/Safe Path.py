from queue import PriorityQueue
from collections import deque

def  DataGathering(line):
    BinaryLine = ''
    Index = 0
    while Index < len(line):
        if line[Index] == '-':
            if Index + 2 < len(line) and line[Index + 1] == '-' and line[Index + 2] == '-':
                BinaryLine += '1'
                Index += 3 
            else:
                BinaryLine += '0' 
                Index += 1
        elif line[Index] == ' ':
            if Index % 2 != 0 and Index + 2 < len(line) and line[Index + 1] == ' ' and line[Index + 2] == ' ' :
                BinaryLine += '0'
                Index += 3 
            elif (Index % 2 != 0 and Index + 2 < len(line) and (line[Index + 1].lower() == 'a' or line[Index + 1].lower() == 's' or line[Index + 1].lower() == 'z' or line[Index + 1].lower() == 'w')  and line[Index + 2] == ' ') :
                BinaryLine += line[Index + 1]
                Index += 3
            else:
                BinaryLine += '0'
                Index += 1
        elif line[Index].lower() == 'a' or line[Index].lower() == 's' or line[Index].lower() == 'z' or line[Index].lower() == 'w' :
                BinaryLine += line[Index]
                Index += 1
        else:
            BinaryLine += '1'
            Index += 1
    return BinaryLine

def Conversion(filename):
    BinaryData = []
    row = 0
    column = 0
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():  
                BinaryData.append(DataGathering(line.strip()))
                row += 1
                column = max(column, len(line.strip()))
    return BinaryData, row, column

def Location(grid, symbol):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == symbol:
                return (i, j)
    return None

moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]



def CheckValidity(x, y, row, col, grid):
    return 0 <= x < row and 0 <= y < col and grid[x][y] != 1


def get_adjacent_cells(x, y):
    return [(x+dx, y+dy) for dx, dy in moves]

def heuristic_manhattan(curr, goal):
    return abs(curr[0] - goal[0]) + abs(curr[1] - goal[1])

def dfs(grid, start, goal):
    visited = set()
    stack = [(start, [])]

    while stack:
        current, path = stack.pop()
        if current == goal:
            return path + [current]
        if current in visited:
            continue
        visited.add(current)
        for move in moves:
            next_cell = (current[0] + move[0], current[1] + move[1])
            if CheckValidity(next_cell[0], next_cell[1], len(grid), len(grid[0]), grid):
                stack.append((next_cell, path + [current]))
    print("Oh, no. Anato is doomed and going to die in suspense without watching the Final episode.")
    return -1

def bfs(grid, start, goal):
    visited = set()
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path + [current]
        if current in visited:
            continue
        visited.add(current)
        for move in moves:
            next_cell = (current[0] + move[0], current[1] + move[1])
            if CheckValidity(next_cell[0], next_cell[1], len(grid), len(grid[0]), grid):
                queue.append((next_cell, path + [current]))
    print("Oh, no. Anato is doomed and going to die in suspense without watching the Final episode.")
    return -1

def ucs(grid, start, goal):
    visited = set()
    pq = PriorityQueue()
    pq.put((0, start, []))

    while not pq.empty():
        cost, current, path = pq.get()
        if current == goal:
            return path + [current]
        if current in visited:
            continue
        visited.add(current)
        for move in moves:
            next_cell = (current[0] + move[0], current[1] + move[1])
            if CheckValidity(next_cell[0], next_cell[1], len(grid), len(grid[0]), grid):
                new_cost = cost + 1  # Uniform cost
                pq.put((new_cost, next_cell, path + [current]))
    print("Oh, no. Anato is doomed and going to die in suspense without watching the Final episode.")
    return -1

def astar(grid, start, goal):
    visited = set()
    pq = PriorityQueue()
    pq.put((0, start, []))

    while not pq.empty():
        _, current, path = pq.get()
        if current == goal:
            return path + [current]
        if current in visited:
            continue
        visited.add(current)
        for move in moves:
            next_cell = (current[0] + move[0], current[1] + move[1])
            if CheckValidity(next_cell[0], next_cell[1], len(grid), len(grid[0]), grid):
                new_cost = len(path) + heuristic_manhattan(next_cell, goal)
                pq.put((new_cost, next_cell, path + [current]))
    print("Oh, no. Anato is doomed and going to die in suspense without watching the Final episode.")
    return -1


filename = 'sample.txt' 
BinaryDataFormatted, row, column = Conversion(filename)
start = Location(BinaryDataFormatted, 'A')  
goal = Location(BinaryDataFormatted, 'S')   

dfs_path = dfs(BinaryDataFormatted, start, goal)
print("DFS Path:", dfs_path)

bfs_path = bfs(BinaryDataFormatted, start, goal)
print("BFS Path:", bfs_path)

ucs_path = ucs(BinaryDataFormatted, start, goal)
print("UCS Path:", ucs_path)

astar_path = astar(BinaryDataFormatted, start, goal)
print("A* Path:", astar_path)