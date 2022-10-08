import numpy as np
import copy
import time
import sys

initial_state_matrix = [] # Initial state

for i in sys.argv[1:17]:
    initial_state_matrix.append(int(i))

initial_state_matrix = np.array(initial_state_matrix)
initial_state_matrix = np.reshape(initial_state_matrix, (4,4))   #The initial state is reshaped into a matrix to better represent the puzzle
initial_state_matrix = initial_state_matrix.tolist()

class Node:
    
    # state_matrix -> This is the matrix representing the positions of all the elements in the puzzle
    # parentNode -> The parent node of a node
    # parentAction -> The action which resulted in the current node being expanded from its parent node.
    # children_nodes -> contains the children nodes
    # visited_nodes -> To keep track of all the visited nodes

    state_matrix = []

    def __init__(self, state, pAction, parent):
        self.state_matrix = state
        self.parentNode = parent
        self.parentAction = pAction

    def getChildNodes(self, visited_nodes, pn):
        
        children = {}  #A dictionary of children - Key:parentAction ; Value:state
        children_nodes = []    #Set of children nodes of a node    
        proceed = True
        frontier = [] #Frontier of the expansion
        
        for i in range(len(self.state_matrix)):
            for j in range(len(self.state_matrix[0])):
                
                if self.state_matrix[i][j] == 0:
                    
                    if ((i + 1) < len(self.state_matrix)):                #swapping the element with the element down
                        proceed = True
                        temp_state = copy.deepcopy(self.state_matrix)
                        temp = temp_state[i][j]
                        temp_state[i][j] = temp_state[i + 1] [j]
                        temp_state[i + 1][j] = temp
                        
                        ### Checking for repeated states ###
                        for v in visited_nodes:
                            
                            if(temp_state == v.state_matrix):    #We do not expand further if the node was already visited
                                proceed = False
                                
                        if proceed == True:       
                            children["D"] = temp_state
                            children_nodes.append(Node(temp_state, "D", pn))

                            for c in children_nodes:
                                visited_nodes.append(c)
                                frontier.append(c)
                        
                    if ((i - 1) >= 0):                #swapping the element with the element up
                        proceed = True
                        temp_state = copy.deepcopy(self.state_matrix)
                        temp = temp_state[i][j]
                        temp_state[i][j] = temp_state[i - 1] [j]
                        temp_state[i - 1][j] = temp
                        
                        ### Checking for repeated states ###
                        for v in visited_nodes:
                            
                            if(temp_state == v.state_matrix):
                                proceed = False
                                
                        if proceed == True:
                            children["U"] = temp_state
                            children_nodes.append(Node(temp_state, "U", pn))

                            for c in children_nodes:
                                visited_nodes.append(c)
                                frontier.append(c)
                            
                        
                    if ((j + 1) < len(self.state_matrix)):                #swapping the element with the element to the right
                        proceed = True
                        temp_state = copy.deepcopy(self.state_matrix)
                        temp = temp_state[i][j]
                        temp_state[i][j] = temp_state[i] [j+1]
                        temp_state[i][j+1] = temp

                        ### Checking for repeated states ###
                        for v in visited_nodes:
                            
                            if(temp_state == v.state_matrix):
                                proceed = False
                                
                        if proceed == True:
                            children["R"] = temp_state
                            children_nodes.append(Node(temp_state, "R", pn))

                            for c in children_nodes:
                                visited_nodes.append(c)
                                frontier.append(c)
                        
                    if ((j - 1) >= 0):                #swapping the element with the element to the right
                        proceed = True
                        temp_state = copy.deepcopy(self.state_matrix)
                        temp = temp_state[i][j]
                        temp_state[i][j] = temp_state[i] [j - 1]
                        temp_state[i][j - 1] = temp
                        
                        ### Checking for repeated states ###
                        for v in visited_nodes:
                            
                            if(temp_state == v.state_matrix):
                                proceed = False
                                
                        if proceed == True:        
                            children["L"] = temp_state
                            children_nodes.append(Node(temp_state, "L", pn))

                            for c in children_nodes:
                                visited_nodes.append(c)
                                frontier.append(c)
                      
        return [children_nodes, visited_nodes, frontier]            


goal_state_matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]  # Goal state is represented as a matrix

visited_nodes = []
queue = []


def bfs(visited, initial_state):
    initial_node = Node(initial_state, [],[])
    visited.append(initial_node)
    queue.append(initial_node)
    frontier = []
    frontier.append(initial_node)

    for nd in frontier:
        if nd.state_matrix == goal_state_matrix :
            return
        else:
            frontier = []
    
    while len(queue)!=0:

        s = queue.pop(0)
        parent_node = s
        nod = s.getChildNodes(visited,parent_node)
        frontier = nod[2]
        visited = nod[1]

        for n in nod[0]:
            queue.append(n)
        moves = ""
        for f in frontier:
            if f.state_matrix == goal_state_matrix:  
                reached_goal_node = f
                current_node = reached_goal_node
                while current_node != initial_node :
                    moves = moves + current_node.parentAction
                    current_node = current_node.parentNode
                return moves,visited,frontier
    


start = time.time()
moves,visited,frontier = bfs([], initial_state_matrix)
end = time.time()

print("Moves : ",moves[::-1])
print("Number of nodes expanded : ", len(set(visited)))
print("Time taken : ", (end-start))
print("Memory used : ", sys.getsizeof(visited) + sys.getsizeof(frontier) )

