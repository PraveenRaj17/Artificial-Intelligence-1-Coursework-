import numpy as np
import math
from scipy.stats import chi2

class Node_example:
        def __init__(self,example,parent_example,action):
            self.example = example
            self.parent_example = parent_example

# ---------------------------------INFORMATION GAIN CALCULATION --------------------------------------#

# to calculate value of B(q)
def B(q):
    if q==0 or q==1: return 0
    return (q*(math.log2(q)) + (1-q)*math.log2(1-q)) * (-1)
    
# To calculate Remainder    
def Remainder(attribute,examples_matrix,p,n):
    r=0    
    d = np.unique(examples_matrix[:,attribute-1])
    n_rows, n_cols = examples_matrix.shape
    for k in d:
        pk=0
        nk=0
        for i in range(0,n_rows):
            if examples_matrix[i,-1] == 'Yes' and examples_matrix[i,attribute-1] == k:
                pk = pk+1
            elif examples_matrix[i,-1] == 'No' and examples_matrix[i,attribute-1] == k:
                nk = nk+1
        r = r + ((pk+nk)/(p+n))*B(pk/(pk+nk))        
    return r

# To calculate Gain for a particular attribute
def Gain(attribute,examples_matrix):
    g=0
    p=0
    n=0
    n_rows, n_cols = examples_matrix.shape
    for i in range(0,n_rows):
        if examples_matrix[i,-1] == 'Yes':
            p = p+1
        else:
            n = n+1
            
    g = B(p/(p+n)) - Remainder(attribute,examples_matrix,p,n)
    
    return g

# -------------------------------------------------------------------------------------------------------#

# To get the most important attribute i.e. most suitable attribute to perform the split.
def importance(attributes, examples_matrix):
    gains = {}
    for a in attributes:
        gains[a] = Gain(a,examples_matrix)
    
    key_list = list(gains.keys())
    val_list = list(gains.values())
 
    position = val_list.index(max(gains.values()))
    
    return key_list[position]

# ---------------------------------------DECISION TREE IMPLEMENTATION ------------------------------------------------------------------------------------#

# Function to learn the decision tree, given the examples, attributes and outputs for each example.
def learn_dec_tree(examples,list_of_attributes,parent_examples, last_rem_attr,c):
    # If there are no examples left :
    if examples.size == 0: 
        list_of_attributes.append(last_rem_attr)        
        c = int(c + 5)
        print("-"*c,'\033[1m',"Will Wait ? " + str(max(set(list(parent_examples[:,10])), key = (list(parent_examples[:,10]).count))),'\033[0m')
        c = int(c - 5)
        return 0
    
    # If the remaining examples or all positive or all negative :
    elif len(set(list(examples[:,10]))) == 1:
        list_of_attributes.append(last_rem_attr) 
        c = int(c + 5)
        print("-"*c,'\033[1m',"Will Wait ? " + str(examples[0,10]),'\033[0m')
        c = int(c - 5)
        return 0
    
    # If there are no attributes left :
    elif len(list_of_attributes) == 0:
        list_of_attributes.append(last_rem_attr)
        c = int(c + 5)
        print("-"*c,'\033[1m',"Will wait ? " + str(max(set(list(parent_examples[:,10])), key = (list(parent_examples[:,10]).count))),'\033[0m')
        c = int(c - 5)
        return 0
    
    else:
        a = importance(list_of_attributes,examples)
        c = int(c+5)
        print('\033[1m' + "-"*c + " | " + column_attributes[a] + " | " + '\033[0m')

        d = np.unique(matrix[:,a-1])

        n_rows, n_cols = examples.shape

        threshold = 0
        delta = 0
        pk_values = []
        # Iterating through each unique values in an attribute
        for k in d:
            exs = np.empty((1,11), dtype='str')
            exs = np.delete(exs, 0, 0)            
            for i in range(0,n_rows):
                if examples[i,a-1] == k:
                    exs = np.vstack((exs, examples[i,:]))

            # ----------------- Pruning ---------------#
                # ------ Calculating Delta -------#
            p_pru = n_pru = pk_pru = nk_pru = 0
            for x in range(0,n_rows):
                if examples[x,-1] == 'Yes':
                    p_pru = p_pru+1
                else:
                    n_pru = n_pru+1                            
            nr,nc = exs.shape        
            for y in range(0,nr):
                if exs[y,-1] == 'Yes':
                    pk_pru = pk_pru+1
                else:
                    nk_pru = nk_pru+1  

            pke = ((pk_pru+nk_pru)/(p_pru+n_pru))*p_pru
            nke = ((pk_pru+nk_pru)/(p_pru+n_pru))*n_pru
            # pk_values.append(pk_pru)
            if pke != 0 and nke != 0 : delta = delta + (((math.pow((pk_pru - pke),2))/pke) + ((math.pow((nk_pru - nke),2))/nke))

            # -------------------------------------------#

            c = int(c + 5)
            print(("-"*c),column_attributes[a] , ":", k)
            if a in list_of_attributes : list_of_attributes.remove(a)
            learn_dec_tree(exs,list_of_attributes,examples,a,c)
            c = int(c - 5)
        
        dof = len(d) - 1   # Degree of Freedom
        threshold = chi2.ppf(0.95, dof )  #Getting threshold value  [ 1 - 0.05 = 0.95 ]

        threshold_values[column_attributes[a]] = threshold
        delta_values[column_attributes[a]] = delta
        # chiSquare_values[a] = chisquare(pk_values)
        list_of_attributes.append(last_rem_attr)
    c = int(c+5)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------#

def main():

    # ----------------------------Reading data from csv-----------------------#
    file = open("restaurant.csv")
    global matrix
    matrix = np.loadtxt(file,dtype='str',delimiter=",")
    nr, nc = matrix.shape
    for r in range(0,nr):
        for cl in range(0,nc):
            matrix[r,cl] = matrix[r,cl].strip()
    # print(matrix)
    # print("\n")
    #--------------------------------------------------------------------------#

    global column_attributes
    column_attributes = {1:"Alternate",2:"Bar",3:"Fri/Sat",4:"Hungry",5:"Patrons",6:"Price",7:"Raining",8:"Reservation",9:"Type",10:"Wait Estimate"}#,11:"Output"}
    global rows_examples
    rows_examples = [1,2,3,4,5,6,7,8,9,10,11,12]
    n_examples = 12

    global delta_values
    delta_values = {}

    global chiSquare_values
    chiSquare_values = {}

    global threshold_values
    threshold_values = {}

    global c
    c = 1
    learn_dec_tree(matrix,list(column_attributes.keys()),None, None,c)
    print("\n",'\033[1m',"Chi Square values i.e. delta for all the nodes : ",'\033[0m')
    print(delta_values)
    print("\n",'\033[1m',"Threshold for each nodes : ",'\033[0m')
    print(threshold_values)
    # print("Chi Square values for all the attributes : ")
    # print(chiSquare_values)



if __name__ == "__main__":
    main()




