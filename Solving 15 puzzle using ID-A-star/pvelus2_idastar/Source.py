import math
import time
import os
import sys
from queue import LifoQueue
import numpy as np

class Puzzle: # A class to represent the properties of the puzzle
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

class Node: # A class to represent a node in the graph
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
    def pop(self, heuristic_type, goal):
            min = 0
            for i in range(len(self.queue)):
                if eval_function(self.queue[i], heuristic_type, goal) < eval_function(self.queue[min], heuristic_type, goal):
                    min = i
            p = self.queue[min]
            del self.queue[min]
            return p

def get_children(parent_node): # Expands the given node to get its children nodes
    children = []
    actions = ['L','R','U','D']
    for action in actions:
        child_state = parent_node.state.get_result_of_action(action)
        child_node = Node(child_state,parent_node,action)
        children.append(child_node)
    return children

def find_path(node): # Function to calculate the path traveled (or) the order of actions performed from initial state to reach the given state
    path = []
    while(node.parent is not None):
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path

def depth_of_node(node): # Calculates the depth of a given node. This can be used as the cost [g(n)] of the node when calculating the node's evaluation function [f(n)]
    depth = 0
    while(node.parent is not None):
        depth = depth + 1
        node = node.parent
    return depth

# Calculates manhattan distance for a given node/state from the goal state. 'g' represents goal state
def manhattan_distance(node, g):
    s = node.state.size
    G = np.array(g)
    G = np.reshape(G, (s,s))
    T = np.array(node.state.tiles)
    T = np.reshape(T, (s,s))
    md = 0
    for j in node.state.tiles:
        x_val,y_val = np.where(T == j)
        x_goal,y_goal = np.where(G == j)
        md = abs(x_val - x_goal) + abs(y_val - y_goal) + md
    return md

# Function to return number of misplaced tiles in the given node/state. 'g' represents goal state
def num_of_misplaced_tiles(node, g):
    n = node.state.tiles
    nmt = 0                     # number of misplaced tiles
    for i in range(len(g)):
        if not n[i] == g[i]:
            nmt = nmt + 1
    return nmt

# Calculates the value of evaluation function f(n) where f(n) = g(n) {or} f(n) = h(n).
# g(n) : depth or cost of the node
# h(n) : manhattan distance or number of misplaced tiles
def eval_function(node, heuristic, goal):
    if(heuristic == "Manhattan distance"):
        f = depth_of_node(node) + manhattan_distance(node, goal)
    elif (heuristic == "Number of misplaced tiles"):
        f = depth_of_node(node) + num_of_misplaced_tiles(node, goal)
    return f

# ------------------------- ITERATIVE DEEPENING A-STAR Search -------------------------------- #
def IDA_star(root, goal, h_type):
    limit = eval_function(root, h_type, goal)
    goal_reached = False
    nIterations = 0
    while (goal_reached == False):
        ExpandedNodes = []
        path, nExpandedNodes, goal_reached, mem, f = a_star(root, goal, limit, h_type, ExpandedNodes)
        limit = f
        nIterations = nIterations + 1
    return path, nExpandedNodes, mem, nIterations
# ---------------------------------------------------------------------------------------------

def a_star(node, goal_state, limit, heuristic_type, NodesExpanded):
    
    if(goal_state == node.state.tiles):
            p = find_path(node)
            return p,len(NodesExpanded), True, max(0, sys.getsizeof(NodesExpanded)), None
    
    f = eval_function(node, heuristic_type, goal_state)
    
    if (f > limit):
        return None,None, False, None, f
    
    children_nodes = get_children(node)
    NodesExpanded.append(node)
    
    min = float("inf")
    
    # Sorting children nodes in ascending order of their evaluation function
    for i in range(0,len(children_nodes)):
        for j in range(i+1,len(children_nodes)):
            if eval_function(children_nodes[i],heuristic_type, goal_state) > eval_function(children_nodes[j], heuristic_type, goal_state):
                temp = children_nodes[i]
                children_nodes[i] = children_nodes[j]
                children_nodes[j] = temp
        
    for child in children_nodes :
        if (child not in NodesExpanded):
            p, nNodesExpanded, goal_reached, mem, evalFunc = a_star(child, goal_state, limit, heuristic_type, NodesExpanded)
            if ( evalFunc == None ):
                return p, nNodesExpanded, goal_reached, mem, evalFunc
            elif (evalFunc < min):
                min = evalFunc
    
    return None, len(NodesExpanded), False, None, min

def main():

    initial = []
    for i in range(1,17):
        initial.append(sys.argv[i])

    initial_list = initial
    root = Node(Puzzle(initial_list),None,None)
    heuristics = []
    #heuristics = ["Number of misplaced tiles","Manhattan distance"]
    #heuristics = ["Manhattan distance"]
    goal_state = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']

    print("\n\n\t a. Number of misplaced tiles")
    print("\t b. Manhattan distance")
    print("\t c. Both a & b")

    h_chosen = input("\t\t\t Choose the type of heuristic : ")
    if h_chosen == "a": heuristics = ["Number of misplaced tiles"]
    elif h_chosen == "b": heuristics = ["Manhattan distance"]
    elif h_chosen == "c": heuristics = ["Number of misplaced tiles","Manhattan distance"]
    else: print("Enter a valid option")

    for heuristic in heuristics:
        #heuristic = i
        print("\n--------------Heuristic : "+ heuristic +" -------------------")
        start_time = time.time()
        path, expanded_nodes, memory_used, iterations = IDA_star(root, goal_state, heuristic)
        end_time = time.time()
        print("Moves: " , path)
        print("Number of expanded Nodes: "+ str(expanded_nodes))
        print("Time Taken: " + str(end_time - start_time))
        print("Max Memory (Bytes): " +  str(memory_used))
        #print("Num of iterations: " +  str(iterations))
        print("\n")

if __name__ == "__main__":
    main()


