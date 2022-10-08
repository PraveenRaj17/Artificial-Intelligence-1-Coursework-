"A-Star search" to find a solution for the 15-puzzle using two types of heuristics
	1. Number of misplaced tiles
	2. Manhattan distance

Language used : Python
Interpreter : Python 3.8.8

The file ‘Source.py’ contains the source code for the program which gives the solution for a 15-puzzle whose initial/starting state has been provided.

The program accepts input as a command line argument.
The input i.e. initial state needs to be entered as a sequence of numbers with a space in between.

Example:
$ python Source.py 1 2 3 4 5 6 7 . . .


The program gives the following information in the output for both heuristics in the below format:

--------------Heuristic : Number of misplaced tiles -------------------

1. Moves 
2. Number of Nodes expanded 
3. Time Taken 
4. Memory Used 

--------------Heuristic : Manhattan distance -------------------

1. Moves 
2. Number of Nodes expanded 
3. Time Taken 
4. Memory Used 