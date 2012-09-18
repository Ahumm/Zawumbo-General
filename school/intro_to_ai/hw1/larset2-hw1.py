##################################################################
##                                                              ##
## Tate Larsen                                                  ##
## 9/23/2012                                                    ##
##                                                              ##
## ------------------------------------------------------------ ##
##                                                              ##
## Intro to AI - Homework 1                                     ##
##   8 Tile Puzzle Solver                                       ##
##                                                              ##
## ------------------------------------------------------------ ##
##                                                              ##
## Tested with Python 2.7.3                                     ##
##   Previous versions ought to work                            ##
##   Will not work with Python 3.X+                             ##
##                                                              ##
## ------------------------------------------------------------ ##
##                                                              ##
## Usage:                                                       ##
##   Manual puzzle entry   :  python larset2-hw1.py             ##
##   Read puzzle from file :  python larset2-hw1.py <filename>  ##
##                                                              ##
## ------------------------------------------------------------ ##
##                                                              ##
## Included Test Files:                                         ##
##   initstate1 - Invalid Input                                 ##
##   initstate2 - Valid Input, Solvable                         ##
##   initstate3 - Valid Input, Unsolvable                       ##
##                                                              ##
## ------------------------------------------------------------ ##
##                                                              ##
## Note:                                                        ##
##   Stops after checking MAX_RUN reachable permutations        ##
##     Can appear to hang if MAX_RUN is too large but           ##
##       it is still running                                    ##
##                                                              ##
##################################################################

import sys

# Specify maximum number of permutations to check
MAX_RUN = 4000

class board:
    state = [0,1,2,3,4,5,6,7,8]
    move_count = 0
    f_score = 0
    last_board = None
    
    def __init__(self):
        return
    
    # Redefine == to only compare the state list
    def __eq__(self, other):
        return self.state == other.state
    
    # set fields of a board with one call
    def set_board(self, new_state, new_move_count, new_last_board):
        self.state = new_state
        self.move_count = new_move_count
        self.last_board = new_last_board
    
    # Find the 2-4 moves possible with the current board configuration
    def get_possible_moves(self):
        possible_states = []
        # Find the empty tile
        e_i = self.state.index(0)
        e_i_x = e_i % 3
        e_i_y = e_i / 3
        # Generate possible states
        if(e_i_x > 0):
            pos = board()
            n_s = list(self.state)
            # Swap tiles
            a, b = e_i, (e_i - 1)
            n_s[a], n_s[b] = n_s[b], n_s[a]
            pos.set_board(n_s, self.move_count + 1, self)
            possible_states.append(pos)
        if(e_i_x < 2):
            pos = board()
            n_s = list(self.state)
            # Swap tiles
            a, b = e_i, (e_i + 1)
            n_s[a], n_s[b] = n_s[b], n_s[a]
            pos.set_board(n_s, self.move_count + 1, self)
            possible_states.append(pos)
        if(e_i_y > 0):
            pos = board()
            n_s = list(self.state)
            # Swap tiles
            a, b = e_i, (e_i - 3)
            n_s[a], n_s[b] = n_s[b], n_s[a]
            pos.set_board(n_s, self.move_count + 1, self)
            possible_states.append(pos)
        if(e_i_y < 2):
            pos = board()
            n_s = list(self.state)
            # Swap tiles
            a, b = e_i, (e_i + 3)
            n_s[a], n_s[b] = n_s[b], n_s[a]
            pos.set_board(n_s, self.move_count + 1, self)
            possible_states.append(pos)
        return possible_states
    
    # Calculate the Manhattan Distance between two board states
    def manhattan_distance(self, other):
        total_dist = 0
        for n in range(9):
            i_c = self.state.index(n)
            i_x_c = i_c % 3
            i_y_c = i_c / 3
            i_g = other.state.index(n)
            i_x_g = i_g % 3
            i_y_g = i_g / 3
            tile_dist = abs(i_x_c - i_x_g) + abs(i_y_c - i_y_g)
            total_dist += tile_dist
        return total_dist

    # Rebuild the Path taken to the solution by following the chain of last_boards up to the starting board and print it
    def print_path(self):
        if self.last_board:
            self.last_board.print_path()
        print "Move number: %d \n%d %d %d \n%d %d %d \n%d %d %d \n" % tuple([self.move_count] + self.state)
        
def a_star(start_board, goal_board):
    # Setup
    closed_set = []
    open_set = [start_board]
    start_board.f_score = start_board.move_count + start_board.manhattan_distance(goal_board)
    
    while open_set:
        cur_board = open_set.pop(0) # pop the first board
        # End after a reasonable number of board permutations are explored
        if len(closed_set) > MAX_RUN:
            return -1
        # Return if we have found a solution
        if cur_board == goal_board:
            print "\nSolution found in %d moves\n" % (cur_board.move_count)
            return cur_board
            
        # Add the current board to the closed_set
        closed_set.append(cur_board)
        
        # Get all unvisited neighbor nodes
        #  Ignore duplicates and boards in the closed_set
        neighbors = cur_board.get_possible_moves()
        neighbors_remove = []
        for n in neighbors:
            for c in closed_set:
                if n == c:
                    neighbors_remove.append(n)
        for n_r in neighbors_remove:
            if n_r in neighbors:
                neighbors.remove(n_r)
        
        for n in neighbors:
            # Check if the current board is in the open_set already
            i = -1
            for o_b in open_set:
                if o_b == n:
                    i = open_set.index(o_b)
            if i > -1:
                # check if we have found a shorter path to the board if found in the open_set
                if n.move_count < open_set[i].move_count:
                    continue
                else:
                    n.f_score = n.move_count + n.manhattan_distance(goal_board)
                    open_set[i] = n
                    continue
            # Board not found in the open_set, add it
            n.f_score = n.move_count + n.manhattan_distance(goal_board)
            open_set.append(n)
        # Sort the open_set by predicted score
        open_set = sorted(open_set, key=lambda x: x.f_score)
    # No solution found for the starting board
    return None

#Attempt to solve a puzzle with the given starting state
def solve(input_list):
    # Generate the goal board
    goal_state = board()
    # Generate the starting board
    start_state = board()
    start_state.state = input_list
    # Attempt to solve
    solution = a_star(start_state, goal_state)
    # Handle various solution states
    if solution != -1:
        if solution:
            solution.print_path()
        else:
            print "No solution found."
    else:
        # Couldn't find a solution in few enough tries
        print "No solution found in %d reachable board permutations." % (MAX_RUN)

# Read starting state from a file
def file_input(filename):
    f_input = []
    try:
        f = open(filename, "r")
        s = f.read()
        f.close()
        s_0 = s.split()
        f_input = [int(float(i)) if '.' in i else int(i) for i in s_0]
    except ValueError as e:
        # User entered invalid character (i.e. not an int or float)
        print "File contents invalid, must contain all numbers 0-8 and only numbers 0-8"
        return
    except IOError as e:
        # Problem Opening the file
        print "Error opening the file: ", e
        return
    except Exception as e:
        # Handle unexpected errors
        print "Unexpected error: ", e
        print "Please try again"
        return
    # Check if file input was valid
    if sorted(f_input) != [0,1,2,3,4,5,6,7,8]:
        print "File contents invalid, must contain all numbers 0-8 and only numbers 0-8"
        return
    print "Input is valid"
    solve(f_input)

# Request user input of starting state
def loop_input():
    while True:
        # Get and parse user input, handling exceptions
        u_input = []
        try:
            s = raw_input("line 1: ")
            s_0 = s.split()
            s = raw_input("line 2: ")
            s_0 += s.split()
            s = raw_input("line 3: ")
            s_0 += s.split()
            u_input = [int(float(i)) if '.' in i else int(i) for i in s_0]
        except ValueError as e:
            # User entered invalid character (i.e. not an int or float)
            print "Invalid input, please enter all numbers 0-8 and only numbers 0-8a"
            continue
        except Exception as e:
            # Handle unexpected errors
            print "Unexpected error: ", e
            print "Please try again"
            continue
        
        # Check if input was valid
        if sorted(u_input) != [0,1,2,3,4,5,6,7,8]:
            print "Invalid input, please enter all numbers 0-8 and only numbers 0-8"
            continue
        print "Input is valid"
        solve(u_input)
        return
        
    
def main(argv):
    if len(argv) > 0:
        file_input(argv[0])
    else:
        loop_input()
        
if __name__ == "__main__":
    main(sys.argv[1:])