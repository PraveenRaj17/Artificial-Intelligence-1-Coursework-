import numpy as np

class MDP:

    def __init__(self, size, WALLS, TERMINAL_STATES, reward, transition_probs, discount_rate, epsilon):
        self.states = []  # record position and action taken at the position
        self.intended_actions = ["east","west","north","south"]
        self.possible_actions = {"straight":transition_probs[0], "left":transition_probs[1], "right":transition_probs[2], "reverse":transition_probs[3]}
        self.r = reward
        self.eps = epsilon
        self.TERMINAL_STATES = TERMINAL_STATES
        self.WALLS = WALLS
        self.gamma = discount_rate
        self.BOARD_ROWS = size[0]
        self.BOARD_COLUMNS = size[1]
        self.TERMINAL_STATES = TERMINAL_STATES
        # initial Q values
        self.Q_valuess = {}
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLUMNS):
                self.Q_valuess[(i,j)] = 0
    
    def nxtPosition(self, cur_position, action, int_action):
        nxtState = (0,0)
        if(int_action == "north"):
            if action == "straight":
                nxtState = (cur_position[0], cur_position[1]+1)
            elif action == "reverse":
                nxtState = (cur_position[0], cur_position[1]-1)
            elif action == "left":
                nxtState = (cur_position[0]-1, cur_position[1])
            else:
                nxtState = (cur_position[0]+1, cur_position[1])

        if(int_action == "east"):
            if action == "straight":
                nxtState = (cur_position[0]+1, cur_position[1])
            elif action == "reverse":
                nxtState = (cur_position[0]-1, cur_position[1])
            elif action == "left":
                nxtState = (cur_position[0], cur_position[1]+1)
            else:
                nxtState = (cur_position[0], cur_position[1]-1)

        if(int_action == "south"):
            if action == "straight":
                nxtState = (cur_position[0], cur_position[1]-1)
            elif action == "reverse":
                nxtState = (cur_position[0], cur_position[1]+1)
            elif action == "left":
                nxtState = (cur_position[0]+1, cur_position[1])
            else:
                nxtState = (cur_position[0]-1, cur_position[1])
                
        if(int_action == "west"):
            if action == "straight":
                nxtState = (cur_position[0]-1, cur_position[1])
            elif action == "reverse":
                nxtState = (cur_position[0]+1, cur_position[1])
            elif action == "left":
                nxtState = (cur_position[0], cur_position[1]-1)
            else:
                nxtState = (cur_position[0], cur_position[1]+1)
        
#        print(nxtState)
        if(nxtState[0]<0 or nxtState[0]>self.BOARD_ROWS-1 or nxtState[1]<0 or nxtState[1]>self.BOARD_COLUMNS-1 or nxtState in self.WALLS):
            nxtState = cur_position

        return nxtState
    
    def showBoard(self):
        for i in range(0, self.BOARD_ROWS):
            print('-----------------')
            out = '| '
            for j in range(0, self.BOARD_COLUMNS):             
                if (i,j) in self.TERMINAL_STATES.keys():
                    token = str(self.TERMINAL_STATES[(i,j)])
                elif (i,j) in self.WALLS:
                    token = '    *    '
                else:
                    token = str(format(self.Q_valuess[(i,j)], '.6f'))
                out += token + ' | '
            print(out)
        print('-----------------')
    
        
    def play(self):
#         print(self.BOARD_ROWS,self.BOARD_COLUMNS)
        print(self.TERMINAL_STATES.keys())
        R = {}
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLUMNS):
                if (i,j) in self.TERMINAL_STATES.keys():
                    R[(i,j)] = self.TERMINAL_STATES[(i,j)]
                elif (i,j) in self.WALLS:
                    R[(i,j)] = 0
                else:
                    R[(i,j)] = -0.04
                    
        rnd = 0

        U1 = []
        U2 = []
        
        it = 0
        proceed = True
        while proceed == True:
            
            U1 = list(self.Q_valuess.values())                    
            for i in range(self.BOARD_ROWS):
                for j in range(self.BOARD_COLUMNS):
                    if (i,j) not in self.TERMINAL_STATES.keys() and (i,j) not in self.WALLS:
                        q = [] # List containing q values for each intended actions
                        for intended_action in self.intended_actions:
                            Qpa = 0
                            for key in self.possible_actions.keys():
                                Qkey = self.possible_actions[key] * (R[self.nxtPosition((i,j),key,intended_action)] - (self.gamma * self.Q_valuess[self.nxtPosition((i,j),key,intended_action)]))
                                Qpa = Qpa + Qkey
                            q.append(Qpa)
                        self.Q_valuess[(i,j)] = max(q)
            U2 = list(self.Q_valuess.values())

            prc = False
            for m in range(self.BOARD_ROWS * self.BOARD_COLUMNS):
                if (abs(U2[m]-U1[m]) <= (self.eps * (1 - self.gamma))/(self.gamma)):
                    prc = prc + False
                else:
                    prc = prc + True
            if prc == False : proceed = False
            it = it + 1
            print("Iteration : ", str(it))
            self.showBoard()
            rnd = rnd + 1
#            rnd = rnd + 1

        optimal_action = np.empty([self.BOARD_ROWS,self.BOARD_COLUMNS], dtype=object)
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLUMNS):
                if (i,j) not in self.TERMINAL_STATES and (i,j) not in self.WALLS:
                    choice = {}           
                    q = []

                    north_cell = (i-1,j)
                    if(north_cell[0]<0 or north_cell[0]>self.BOARD_ROWS-1 or north_cell[1]<0 or north_cell[1]>self.BOARD_COLUMNS-1 or north_cell in self.WALLS) == False:
                        choice[self.Q_valuess[north_cell]] = "up"
                    #    if i==1 and j==0: print(self.Q_valuess[north_cell])
                    #print(i,j)
                    south_cell = (i+1,j)
                    if(south_cell[0]<0 or south_cell[0]>self.BOARD_ROWS-1 or south_cell[1]<0 or south_cell[1]>self.BOARD_COLUMNS-1 or south_cell in self.WALLS) == False:
                        choice[self.Q_valuess[south_cell]] = "down"
                    #    if i==1 and j==0: print(self.Q_valuess[south_cell])                    
                    west_cell = (i,j-1)
                    if(west_cell[0]<0 or west_cell[0]>self.BOARD_ROWS-1 or west_cell[1]<0 or west_cell[1]>self.BOARD_COLUMNS-1 or west_cell in self.WALLS) == False:
                        choice[self.Q_valuess[west_cell]] = "left"
                    #    if i==1 and j==0: print(self.Q_valuess[west_cell])                    
                    east_cell = (i,j+1)
                    if(east_cell[0]<0 or east_cell[0]>self.BOARD_ROWS-1 or east_cell[1]<0 or east_cell[1]>self.BOARD_COLUMNS-1 or east_cell in self.WALLS) == False:
                        choice[self.Q_valuess[east_cell]] = "right"
                    #    if i==1 and j==0: print(self.Q_valuess[east_cell])                

                    z = list(choice.keys())
                    optimal_action[i,j] = str(choice[max(z)])
                    # if(i==1 and j==0): 
                    #     print(choice)
                    #     print(max(z), str(choice[max(z)]))
                
        print(optimal_action)


def main():

    wall_locs = []
    TERMINAL_STATES = {}
    size = []
    reward = 0
    transition_probs = []
    eps = 0
    disc_rate = 0

    lines = []
    with open('mdp_input.txt') as f:
        lines = f.readlines()


    # print(lines[10])
    leng = len(lines)
    for i in range(leng):
        if ':' in lines[i]:
            if (lines[i].split(':')[0].strip() == 'size'):
                size = (int((lines[i].split(':')[1].strip()).split(' ')[0]),int((lines[i].split(':')[1].strip()).split(' ')[1]))

            if (lines[i].split(':')[0].strip() == 'walls'):
                length = len((lines[i].split(':')[1].strip()).split(','))
                for l in range(length):
                    wall_locs.append((int(((((lines[i].split(':')[1].strip()).split(',')[l]).strip()).split(' ')[0]).strip())-1,int(((((lines[i].split(':')[1].strip()).split(',')[l]).strip()).split(' ')[1]).strip())-1))

            if (lines[i].split(':')[0].strip() == 'terminal_states'):
                length = len((lines[i].split(':')[1].strip()).split(','))
                for l in range(length):
                    TERMINAL_STATES[(int(((((lines[i].split(':')[1].strip()).split(',')[l]).strip()).split(' ')[0]).strip())-1,int(((((lines[i].split(':')[1].strip()).split(',')[l]).strip()).split(' ')[1]).strip())-1)] = int(((((lines[i].split(':')[1].strip()).split(',')[l]).strip()).split(' ')[2]).strip())
            
            if (lines[i].split(':')[0].strip() == 'reward'):
                reward = float(lines[i].split(':')[1].strip())
            

            if (lines[i].split(':')[0].strip() == 'discount_rate'):
                disc_rate = float(lines[i].split(':')[1].strip())
            
            if (lines[i].split(':')[0].strip() == 'epsilon'):
                eps = float(lines[i].split(':')[1].strip())

            if (lines[i].split(':')[0].strip() == 'transition_probabilities'):
                transition_probs = ((lines[i].split(':')[1].strip()).split(' '))
                transition_probs = [float(i) for i in transition_probs]

    md = MDP(size,wall_locs,TERMINAL_STATES,reward,transition_probs,disc_rate,eps)
    md.play()

if __name__ == "__main__":
    main()

