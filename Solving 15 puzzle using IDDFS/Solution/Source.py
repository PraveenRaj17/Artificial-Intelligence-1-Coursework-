

import math
import time
import os
import sys
from queue import LifoQueue
#import numpy as np

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


# Function to get the children of a given node
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


def dfs(root_node, goal_state, limit):
    
    cur_depth = 0
    frontier = []
    frontier.append(root_node)
    visited = []
    
    backTrack = False  # To define whether the algorithm should proceed further down the branch or backtrack.
    
    while (len(frontier)!=0):
        backTrack = False
        
        # -------Backtracking : when depth limit has been reached--------- #
        if (cur_depth == limit):
            if (cur_depth == 1 and len(frontier) == 0 ):
                return None, None, False, None
            else:
                backTrack = True
        # -------------------------------------------------------------------
        
        current_node = frontier.pop()
        visited.append(current_node)
        
        # Check if the current node is the goal node
        if(goal_state == current_node.state.tiles):
            path = find_path(current_node)
            return path,len(visited), True, max(0, sys.getsizeof(frontier)+sys.getsizeof(visited))
        
        children_nodes = get_children(current_node)  # Expanding a node
        
        
        # -----------------------------Backtracking ---------------------------- #

        # If the node has no children, the parent node is added to the frontier i.e. the stack
        if (len(children_nodes) == 0):
            backTrack = True
        else:
            # If the node has no unvisited children, the parent node is added to the frontier i.e. the stack
            unvisited_children = []
            for child in children_nodes:
                if child not in visited:
                    unvisited_children.append(child)  # An arbitary array containing children of the node which were already visited
            if (len(unvisited_children) == 0):
                # If the algorithm is backtracking at the root node and there are no available unvisited children, 
                # the algorithm stops further expansion and backtracking
                if (current_node == root_node):
                    return None, None, False, None
                backTrack = True
         
        if backTrack == True:
            frontier.append(current_node.parent)
            cur_depth = cur_depth - 1  # Decreasing depth by 1, since backtracking...
            
        # ------------------------If conditions for Backtracking fail------------------------- #
        
        else:
            # -------Adding unvisited child nodes into frontier i.e. stack---------
            for child in children_nodes:
                if child not in visited:
                    frontier.append(child)
            cur_depth = cur_depth + 1
        # ------------------------------------------------------------------------------------- #
                
    return None,None, False, None  # Executed when the goal state couldn't be found
                    

def iterative_deepening_dfs(root, goal):
    limit = 1
    goal_reached = False
    while (goal_reached == False):
        path,exp_nodes,goal_reached, memory = dfs(root, goal, limit)
        limit = limit + 1
        
    return path, exp_nodes, memory

def main():

    initial = []
    for i in range(1,17):
        initial.append(sys.argv[i])

    #initial = str(input("initial configuration: "))
    initial_list = initial
    root = Node(Puzzle(initial_list),None,None)

    goal_state = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']

    start_time = time.time()
    path, expanded_nodes, memory_used = iterative_deepening_dfs(root, goal_state)
    end_time = time.time()

    print("Moves: " , path)
    print("Number of expanded Nodes: "+ str(expanded_nodes))
    print("Time Taken: " + str(end_time - start_time))
    print("Max Memory (Bytes): " +  str(memory_used))
    
if __name__ == "__main__":
    main()



