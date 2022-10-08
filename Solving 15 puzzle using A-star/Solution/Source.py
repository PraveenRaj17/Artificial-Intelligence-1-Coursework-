import math
import time
import os
import sys
from queue import LifoQueue
import numpy as np

class Puzzle:
    def __init__(self,tiles):
        self.size = int(math.sqrt(len(tiles))) # defining length/width of the Puzzle
        self.tiles = tiles

    # Function to get list of possible scenarios of the puzzle for each possible action
    def get_result_of_action(self,action):
        result_tiles = self.tiles[:]
        empty_index = result_tiles.index('0')
        if action=='L':
            if empty_index%self.size>0:
                result_tiles[empty_index-1],result_tiles[empty_index] = result_tiles[empty_index],result_tiles[empty_index-1]
        if action=='R':
            if empty_index%self.size<(self.size-1): 	
                result_tiles[empty_index+1],result_tiles[empty_index] = result_tiles[empty_index],result_tiles[empty_index+1]
        if action=='U':
            if empty_index-self.size>=0:
                result_tiles[empty_index-self.size],result_tiles[empty_index] = result_tiles[empty_index],result_tiles[empty_index-self.size]
        if action=='D':
            if empty_index+self.size < self.size*self.size:
                result_tiles[empty_index+self.size],result_tiles[empty_index] = result_tiles[empty_index],result_tiles[empty_index+self.size]
        return Puzzle(result_tiles)


class Node:
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action

    # __repr__ helps represent objects as a string
    def __repr__(self):
        return str(self.state.tiles)

    # Defining the rules to compare two nodes of class type "Node"
    def __eq__(self,other):
        return self.state.tiles == other.state.tiles

# Priority queue to represent the frontier. The class also has a method 'pop' to get the element with the highest priority - lowest value of evaluation funcyion in this case
class PriorityQueue(object):
    
    def __init__(self):
        self.queue = []
        
    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0
    
    # for inserting an element in the queue
    def append(self, element):
        self.queue.append(element)
  
    # for popping an element based on Priority i.e. low value of evaluation function in this case
    def pop(self, h, goal_state):
            min = 0
            for i in range(len(self.queue)):
                if eval_function(self.queue[i], h, goal_state) < eval_function(self.queue[min], h, goal_state):
                    min = i
            p = self.queue[min]
            del self.queue[min]
            return p

def get_children(parent_node):
    children = []
    actions = ['L','R','U','D']
    for action in actions:
        child_state = parent_node.state.get_result_of_action(action)
        child_node = Node(child_state,parent_node,action)
        children.append(child_node)
    return children

def find_path(node):
    path = []
    while(node.parent is not None):
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path

# Calculates manhattan distance for a given node/state from the goal state
def manhattan_distance(node, goal_state):
    s = node.state.size
    G = np.array(goal_state)
    G = np.reshape(G, (s,s))
    T = np.array(node.state.tiles)
    T = np.reshape(T, (s,s))
    md = 0
    for j in node.state.tiles:
        x_val,y_val = np.where(T == j)
        x_goal,y_goal = np.where(G == j)
        md = abs(x_val - x_goal) + abs(y_val - y_goal) + md
    return md
        

# Function to return number of misplaced tiles in the given node/state
def num_of_misplaced_tiles(node, goal_state):
    n = node.state.tiles
    g = goal_state
    nmt = 0                     # number of misplaced tiles
    for i in range(len(g)):
        if not n[i] == g[i]:
            nmt = nmt + 1
    return nmt
        

# calculates the value of evaluation function f(n) where f(n) = g(n) {or} f(n) = h(n).
# g(n) : number of misplaced tiles
# h(n) : manhattan distance
def eval_function(node, heuristic, goal):
    if(heuristic == "Manhattan distance"):
        f = manhattan_distance(node, goal)
    elif (heuristic == "Number of misplaced tiles"):
        f = num_of_misplaced_tiles(node, goal)
    return f

def a_star(root_node, goal_state, heuristic_type):

    frontier = PriorityQueue()
    frontier.append(root_node)
    visited = []
    
    while not frontier.isEmpty():

        current_node = frontier.pop(heuristic_type, goal_state)
        visited.append(current_node)
        
        # Check if the current node is the goal node
        if(goal_state == current_node.state.tiles):
            path = find_path(current_node)
            return path,len(visited), True, max(0, sys.getsizeof(frontier)+sys.getsizeof(visited))
        
        children_nodes = get_children(current_node)  # Expanding a node
        for child in children_nodes:
            if child not in visited:
                frontier.append(child)
                
    return None,None, False, None  # Executed when the goal state couldn't be found

def main():

    initial = []
    for i in range(1,17):
        initial.append(sys.argv[i])

    heuristic = ""
            
    initial_list = initial
    root = Node(Puzzle(initial_list),None,None)
    heuristics = ["Number of misplaced tiles","Manhattan distance"]
    goal_state = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']

    for i in heuristics:
        heuristic = i
        print("\n")
        print("--------------Heuristic : "+ heuristic +" -------------------")
        start_time = time.time()
        path, expanded_nodes,goal_reached, memory_used = a_star(root, goal_state, heuristic)
        end_time = time.time()
        print("\n")
        print("Moves: " , path)
        print("Number of expanded Nodes: "+ str(expanded_nodes))
        print("Time Taken: " + str(end_time - start_time))
        print("Memory used: " +  str(memory_used))

if __name__ == "__main__":
    main()