# Tate Larsen
# Intro to AI
# Homework 3
# Hunt the Wumpus 2

# Usage:
#  python larset2-hw3.py <MAP_FILE>

# To have it solve, use the "solve" command
# Tends to fail if there is no clear path to the goal (i.e there is a stench or a breeze in the first spot)
# Couldn't figure out a solution to that before the deadline
# Prints path to the command line

# Tested with Python 2.7.3

import string
import copy
import sys
import operator

# Class to represent the map
class board:
    map = []
    percepts = [] # [Stench, Breeze, Glitter, Scream, Wumpus, Pit]
    x = 0
    y = 0
    wumpus_position = [0,0]
    wumpus_alive = True
    
    def __init__(self, filename):
        # Load the map from the file
        f = open(filename, 'r')
        line = f.readline()
        while(line):
            self.y += 1
            l_tmp = string.split(string.strip(line), ',')
            self.x = len(l_tmp)
            self.map.append(list(l_tmp))
            line = f.readline()
        self.map.reverse() # Flip the map so 0,0 is bottom left
        f.close()
        
        # Generate the percepts as base
        base_p = {'S':False,'B':False,'G':False,'W':False,'P':False}
        row = []
        for i in range(self.x):
            row.append(base_p.copy())
        for i in range(self.y):
            self.percepts.append(copy.deepcopy(row))
        
        # Populate precepts based on the previously loaded data
        for i in range(self.x):
            for j in range(self.y):
                if(self.map[i][j] == 'X'): # Handle empty spaces
                    continue
                if(self.map[i][j] == 'G'): # Handle Gold
                    self.percepts[i][j]['G'] = True
                    continue
                if(self.map[i][j] == 'P'): # Handle Pits
                    self.percepts[i][j]['P'] = True
                    # Populate Breezes
                    self.percepts[i][j]['B'] = True
                    if(i - 1 >= 0):
                        self.percepts[i-1][j]['B'] = True
                    if(j - 1 >= 0):
                        self.percepts[i][j-1]['B'] = True
                    if(i + 1 < self.x):
                        self.percepts[i+1][j]['B'] = True
                    if(j + 1 < self.y):
                        self.percepts[i][j+1]['B'] = True
                    continue
                if(self.map[i][j] == 'W'): # Handle Wumpus
                    self.percepts[i][j]['W'] = True
                    # Populate Stench
                    self.percepts[i][j]['S'] = True
                    self.wumpus_position = [i,j]
                    if(i - 1 >= 0):
                        self.percepts[i-1][j]['S'] = True
                    if(j - 1 >= 0):
                        self.percepts[i][j-1]['S'] = True
                    if(i + 1 < self.x):
                        self.percepts[i+1][j]['S'] = True
                    if(j + 1 < self.y):
                        self.percepts[i][j+1]['S'] = True
                    continue
    
    # Return symbol for specified location (None if off map)
    def get(self, x, y):
        if(x < 0 or x >= self.x):
            return None
        if(y < 0 or y >= self.y):
            return None
        return self.map[x][y]
    
    # return percept for specified location (None if off map
    def get_percept(self, x, y):
        if(x < 0 or x >= self.x):
            return None
        if(y < 0 or y >= self.y):
            return None
        return self.percepts[x][y]

# Class for the player
class player:
    position = [0,0]
    heading = 0 # 0:East, 1:South, 2:West, 3: North
    arrows = 1
    score = 0
    # Keep track of what we've seen
    percept = {}
    percept_map = []
    # Some end conditions
    dead = False
    win = False
    quit = False
    
    def __init__(self, b):
        self.position = [0,0]
        self.heading = 0;
        self.score = 0
        self.percept = b.get_percept(self.position[0], self.position[1])
        
        # Generate the percept_map for use as Knowledge Base (Initially all cells are None)
        row = []
        for i in range(b.x):
            row.append(None)
        for i in range(b.y):
            self.percept_map.append(copy.deepcopy(row))
    
    # Print the current status text
    def print_status(self, b):
        # Location Info
        dir = ["EAST","SOUTH","WEST","NORTH"]
        print "\nYou are in room [%d,%d] of the cave. Facing %s." % (self.position[0]+1, self.position[1]+1, dir[self.heading])
        # Percepts
        if(self.percept['S']):
            print "There is a STENCH in here!"
        if(self.percept['B']):
            print "There is a BREEZE in here!"
        if(self.percept['G'] and not b.wumpus_alive):
            print "There is a dead Wumpus in here!"
        
    # Update the KB
    def update(self, b):
        self.percept_map[self.position[0]][self.position[1]] = self.percept.copy() # Copy in the current location's percept
        self.percept_map[self.position[0]][self.position[1]]['V'] = True           # Set current location as visited
        
        # Clear the old map knowledge
        for i in range(b.x):
            for j in range(b.y):
                if(self.percept_map[i][j] and not self.percept_map[i][j]['V']):
                    self.percept_map[i][j] = None
                    
        # Now populate with new knowledge
        for i in range(b.x):
            for j in range(b.y):
                if not self.percept_map[i][j]:
                    base_p = {'S':False,'B':False,'G':False,'W':False,'P':False, 'V':False} # Starting percept
                    
                    # Grab neighboring cells
                    adjacent_cells = []
                    if(i - 1 >= 0):
                        adjacent_cells.append(self.percept_map[i-1][j])
                    if(j - 1 >= 0):
                        adjacent_cells.append(self.percept_map[i][j-1])
                    if(i + 1 < b.x):
                        adjacent_cells.append(self.percept_map[i+1][j])
                    if(j + 1 < b.y):
                        adjacent_cells.append(self.percept_map[i][j+1])
                        
                    # Only look at visited cells adjacent_cells
                    adjacent_cells = [a for a in adjacent_cells if a and a['V']]
                    # We know some facts based on where we've been
                    for a in adjacent_cells:
                        if a['W']: base_p['S'] = True
                        if a['P']: base_p['B'] = True
                        
                    # Separate stench and non-stench cells, if both exist it is safe, if s_cells exist and s_not_cells do not, we can assume there is a wumpus there    
                    s_cells = [a for a in adjacent_cells if a['S']]
                    s_not_cells = [a for a in adjacent_cells if not a['S']]
                    if s_cells and not s_not_cells: base_p['W'] = True
                    
                    # Separate breeze and non-breeze cells, if both exist it is safe, if b_cells exist and b_not_cells do not, we can assume there is a pit there    
                    b_cells = [a for a in adjacent_cells if a['B']]
                    b_not_cells = [a for a in adjacent_cells if not a['B']]
                    if b_cells and not b_not_cells: base_p['P'] = True
 
                    # Add that to the map if we changed it
                    if adjacent_cells:
                        self.percept_map[i][j] = copy.deepcopy(base_p)
    
    # Compare the important fields of spot and percept
    def cmp_percept(self, spot, percept):
        tmp_p = self.percept_map[spot[0]][spot[1]]
        if not tmp_p: return False
        return (percept['W'] == tmp_p['W'] and percept['P'] == tmp_p['P'] and percept['V'] == tmp_p['V'])
        
    # Distance to closest of goal percept
    def manhattan_distance(self, b, start_spot, goal_percept):
        least_d = sys.maxint
        least_p = [0,0]
        for i in range(b.x):
            for j in range(b.y):
                if self.cmp_percept([i,j], goal_percept):
                    d = abs(i - start_spot[0]) + abs(j - start_spot[1])
                    if d < least_d:
                        least_d = d
                        least_p = [i, j]
                else:
                    d = abs(i - start_spot[0]) + abs(j - start_spot[1]) + 5
                    if d < least_d:
                        least_d = d
                        least_p = [i, j]
        return least_d
    
    # Get distance to adjacent node, weight away from pits/wumpus
    def dist_between(self, start_spot, end_spot):
        tmp_p = self.percept_map[end_spot[0]][end_spot[1]]
        if not tmp_p: return sys.maxint
        if tmp_p['W']: return 10
        if tmp_p['P']: return 5
        return abs(end_spot[0] - start_spot[0]) + abs(end_spot[1] - start_spot[1])
    
    # Start spot is a list [x,y]
    def a_star(self, b, start_spot, goal_percept):
        # Setup
        closed_set = {}
        open_set = {tuple(start_spot):0}
        came_from = {}
        
        g_score = {}
        g_score[tuple(start_spot)] = 0
        f_score = {}
        f_score[tuple(start_spot)] = g_score[tuple(start_spot)] + self.manhattan_distance(b, start_spot, goal_percept)
        
        while open_set:
            if (3,0) in g_score: print g_score[(2,0)]
            cur = sorted(open_set.iteritems(), key=operator.itemgetter(1))[0][0]

            #if True: return
            open_set.pop(cur)
            if self.cmp_percept(cur, goal_percept):
                return self.rebuild(came_from, tuple(cur))
            
            closed_set[tuple(cur)] = 1
            
            adjacent_cells = []
            if(cur[0] - 1 >= 0):
                adjacent_cells.append([cur[0]-1,cur[1]])
            if(cur[1] - 1 >= 0):
                adjacent_cells.append([cur[0],cur[1]-1])
            if(cur[0] + 1 < b.x):
                adjacent_cells.append([cur[0]+1,cur[1]])
            if(cur[1] + 1 < b.y):
                adjacent_cells.append([cur[0],cur[1]+1])
            adjacent_cells = [a for a in adjacent_cells if self.percept_map[a[0]][a[1]]]
            
            for a in adjacent_cells:
                if tuple(a) in closed_set:
                    continue
                tentative_g_score = g_score[tuple(cur)] + self.dist_between(cur, a)
                if tuple(a) not in open_set or tentative_g_score <= g_score[tuple(a)]:
                    came_from[tuple(a)] = tuple(cur)
                    g_score[tuple(a)] = tentative_g_score
                    f_score[tuple(a)] = g_score[tuple(a)] + self.manhattan_distance(b, a, goal_percept)
                    if tuple(a) not in open_set:
                        open_set[tuple(a)] = g_score[tuple(a)]
        return None
    
    def rebuild(self, came_from, cur):
        #print "cur: " + str(cur) + "  :::  " + str(came_from)
        if came_from[cur] in came_from:
            #print came_from[cur]
            p = self.rebuild(came_from, came_from[cur]) + [list(cur)]
            #print "p: " + str(p)
            return p
        return [list(cur)]
    
    def solve(self, b):
        base_p = {'S':False,'B':False,'G':False,'W':False,'P':False, 'V':False} # Starting percept clear
        risk_p = {'S':False,'B':False,'G':False,'W':False,'P':True, 'V':False} # Starting percept pit
        bad_p = {'S':False,'B':False,'G':False,'W':True,'P':False, 'V':False} # Starting percept wumpus
        hist = ""
        pos_path = str(self.position) + " --> "
        while True:
            if self.win or self.dead: break
            # Try riskier paths until we find one
            path = self.a_star(b, self.position, base_p)
            if not path: path = self.a_star(b, self.position, risk_p)
            if not path: path = self.a_star(b, self.position, bad_p)
            #print "path: " + str(path)
            for c in path:
                if self.win or self.dead: break
                # Perform the move
                if c[0] > self.position[0]: hist += self.move_to(b, "n")
                if c[0] < self.position[0]: hist += self.move_to(b, "s")
                if c[1] > self.position[1]: hist += self.move_to(b, "e")
                if c[1] < self.position[1]: hist += self.move_to(b, "w")
                #print "pos:  " + pos_path#str(self.position)
                pos_path += str(self.position) + " --> "
                #Update
                self.update(b)
                #print "hist: " + hist
        #Print the final path and commands
        print "Path Taken: " + hist  
        print "Pos Order: " + pos_path[:-5]
        return
    
    # Turn to a direction then move forward
    def move_to(self, b, goal):
        d = {'e':0,'s':1,'w':2,'n':3}
        r = ""
        while self.heading != d[goal]:
            self.quiet_move("r", b)
            r += "r"
        self.quiet_move("f", b)
        r += "f"
        return r
    
    def quiet_move(self, cmd, b):
        # Handle 'R'
        if(cmd.lower() == 'r'):
            # Change Heading
            self.heading += 1
            if(self.heading == 4):
                self.heading = 0
            self.percept = b.get_percept(self.position[0], self.position[1]) # Update Percept
        # Handle 'L'
        elif(cmd.lower() == 'l'):
            self.heading -= 1
            if(self.heading == -1):
                self.heading = 3
            self.percept = b.get_percept(self.position[0], self.position[1]) # Update Percept
        # Handle 'F'
        elif(cmd.lower() == 'f'):
            self.score -= 1 # Update Score
            if(self.heading == 0): # Move EAST
                # Check if we hit a wall
                new_percept = b.get_percept(self.position[0], self.position[1]+1)
                if(new_percept):
                    self.position[1] += 1
                    self.percept = new_percept # Update Percept
            elif(self.heading == 1): # Move SOUTH
                # Check if we hit a wall
                new_percept = b.get_percept(self.position[0]-1, self.position[1])
                if(new_percept):
                    self.position[0] -= 1
                    self.percept = new_percept # Update Percept
            elif(self.heading == 2): # Move WEST
                # Check if we hit a wall
                new_percept = b.get_percept(self.position[0], self.position[1]-1)
                if(new_percept):
                    self.position[1] -= 1
                    self.percept = new_percept # Update Percept
            elif(self.heading == 3): # Move NORTH
                # Check if we hit a wall
                new_percept = b.get_percept(self.position[0]+1, self.position[1])
                if(new_percept):
                    self.position[0] += 1
                    self.percept = new_percept # Update Percept
        # Check if player is in a pit
        if(self.percept['P']):
            print "You fall in a pit and die!"
            self.dead = True # OOPS
        # Check if player has found the gold
        if(self.percept['G']):
            print "You have found the GOLD!ff"
            self.score += 1000 # Update Score
            self.win = True # YAY
        # Check if player has found the Wumpus
        if(self.percept['W']):
            # Check if the wumpus is alive
            if(b.wumpus_alive):
                print "You run in to a Wumpus and die!"
                self.score -= 1000 # Update Score
                self.dead = True # OOPS
    
    def move(self, cmd, b):
        # Handle 'Quit' 'Q' and 'Exit'
        if(cmd.lower() == 'q' or cmd.lower() == 'quit' or cmd.lower() == 'exit'):
            self.quit = True
            return
        # Handle 'More'
        elif(cmd.lower() == 'more'):
            print "Additional Commands:\n\tQUIT/Q/EXIT\n\tPRINTKB/KB"
            return
        # Handle 'kb' and 'printkb'
        elif(cmd.lower() == 'kb' or cmd.lower() == 'printkb'):
            tmp = copy.deepcopy(self.percept_map)
            tmp.reverse() # Flip it
            for l in tmp:
                print l # Print it
            return
        # Handle 'rkb'
        elif(cmd.lower() == 'rkb'):
            self.readable_map(b)
            return
        # Handle 'printmap' and map
        elif(cmd.lower() == 'map' or cmd.lower() == 'printmap'):
            tmp = copy.deepcopy(b.map)
            tmp.reverse() # Flip it
            for l in tmp:
                print l # Print it
        # Handle 'solve'
        elif(cmd.lower() == 'solve'):
            self.solve(b)
            return
        # Handle 'R'
        elif(cmd.lower() == 'r'):
            # Change Heading
            self.heading += 1
            if(self.heading == 4):
                self.heading = 0
            self.percept = b.get_percept(self.position[0], self.position[1]) # Update Percept
        # Handle 'L'
        elif(cmd.lower() == 'l'):
            self.heading -= 1
            if(self.heading == -1):
                self.heading = 3
            self.percept = b.get_percept(self.position[0], self.position[1]) # Update Percept
        # Handle 'F'
        elif(cmd.lower() == 'f'):
            self.score -= 1 # Update Score
            if(self.heading == 0): # Move EAST
                # Check if we hit a wall
                new_percept = b.get_percept(self.position[0], self.position[1]+1)
                if(new_percept):
                    self.position[1] += 1
                    self.percept = new_percept # Update Percept
                else:
                    print "BUMP!!! You hit a wall!"
                    self.percept = b.get_percept(self.position[0],self.position[1]) # Update Percept
            elif(self.heading == 1): # Move SOUTH
                # Check if we hit a wall
                new_percept = b.get_percept(self.position[0]-1, self.position[1])
                if(new_percept):
                    self.position[0] -= 1
                    self.percept = new_percept # Update Percept
                else:
                    print "BUMP!!! You hit a wall!"
                    self.percept = b.get_percept(self.position[0],self.position[1]) # Update Percept
            elif(self.heading == 2): # Move WEST
                # Check if we hit a wall
                new_percept = b.get_percept(self.position[0], self.position[1]-1)
                if(new_percept):
                    self.position[1] -= 1
                    self.percept = new_percept # Update Percept
                else:
                    print "BUMP!!! You hit a wall!"
                    self.percept = b.get_percept(self.position[0],self.position[1]) # Update Percept
            elif(self.heading == 3): # Move NORTH
                # Check if we hit a wall
                new_percept = b.get_percept(self.position[0]+1, self.position[1])
                if(new_percept):
                    self.position[0] += 1
                    self.percept = new_percept # Update Percept
                else:
                    print "BUMP!!! You hit a wall!"
                    self.percept = b.get_percept(self.position[0],self.position[1]) # Update Percept
        # Handle 'S'
        elif(cmd.lower() == 's'):
            # Check if we even have arrows
            if(self.arrows == 0):
                print "You have no arrow left to shoot."
                self.percept = b.get_percept(self.position[0],self.position[1]) # Update Percept
                return
            # Update Score
            self.arrows -= 1
            self.score -= 10
            
            if(self.heading == 0): # Shoot East
                # Check if wupus is ahead of us
                if(b.wumpus_position[0] == self.position[0] and b.wumpus_position[1] > self.position[1]):
                    self.score += 500 # Update Score
                    b.wumpus_alive = False # Kill Wumpus
                    print "You hear a SCREAM as the Wumpus dies"
                    self.percept = b.get_percept(self.position[0],self.position[1]) # Update Percept
                    return
            elif(self.heading == 1): # Shoot SOUTH
                # Check if wupus is ahead of us
                if(b.wumpus_position[1] == self.position[1] and b.wumpus_position[0] < self.position[0]):
                    self.score += 500 # Update Score
                    b.wumpus_alive = False # Kill Wumpus
                    print "You hear a SCREAM as the Wumpus dies"
                    self.percept = b.get_percept(self.position[0],self.position[1]) # Update Percept
                    return
            elif(self.heading == 2): # Shoot WEST
                # Check if wupus is ahead of us
                if(b.wumpus_position[0] == self.position[0] and b.wumpus_position[1] < self.position[1]):
                    self.score += 500 # Update Score
                    b.wumpus_alive = False # Kill Wumpus
                    print "You hear a SCREAM as the Wumpus dies"
                    self.percept = b.get_percept(self.position[0],self.position[1]) # Update Percept
                    return
            elif(self.heading == 3): # Shoot NORTH
                # Check if wupus is ahead of us
                if(b.wumpus_position[1] == self.position[1] and b.wumpus_position[0] > self.position[0]):
                    self.score += 500 # Update Score
                    b.wumpus_alive = False # Kill Wumpus
                    print "You hear a SCREAM as the Wumpus dies"
                    self.percept = b.get_percept(self.position[0],self.position[1]) # Update Percept
                    return
            # We missed
            print "Your arrow flies off and doesn't hit anything"
            self.percept = b.get_percept(self.position[0],self.position[1]) # Update Percept   
        # Handle undefined input
        else:
            print "Command Not Recognized: Please try again."
            return
        
        # Check if player is in a pit
        if(self.percept['P']):
            print "You fall in a pit and die!"
            self.dead = True # OOPS
        # Check if player has found the gold
        if(self.percept['G']):
            print "You have found the GOLD!"
            self.score += 1000 # Update Score
            self.win = True # YAY
        # Check if player has found the Wumpus
        if(self.percept['W']):
            # Check if the wumpus is alive
            if(b.wumpus_alive):
                print "You run in to a Wumpus and die!"
                self.score -= 1000 # Update Score
                self.dead = True # OOPS
            else:
                print "You have found a dead Wumpus!"
    
    def readable_map(self, b):
        p = []
        for i in range(b.x):
            s = ""
            for j in range(b.y):
                t = ""
                if not self.percept_map[i][j]:
                    s += "   X,"
                    continue
                if self.position == [i,j]: t+= "."
                if self.percept_map[i][j]['S']: t += "S"
                if self.percept_map[i][j]['B']: t += "B"
                if self.percept_map[i][j]['W']: t += "W"
                if self.percept_map[i][j]['P']: t += "P"
                if not t: t = "X"
                s += str.rjust(t,4) + ","
            p.append(s)
        p.reverse()
        print "\n".join(p)
        
def main():
    # Check usage
    if not (len(sys.argv) == 2):
        print "Usage: python larset2-hw2.py <MAP_FILE>"
        return
    # Generate the board and player
    b = board(sys.argv[1])
    p = player(b)
    p.update(b) # Initial update to insert starting position into Knowledge Base
    
    while(not p.dead and not p.win and not p.quit):
        # Print what we see
        p.print_status(b)
        # Get input
        inp = raw_input("What would you like to do? Please enter command [R,L,F,S, more]:\n> ")
        # Process input
        p.move(inp, b)
        #Update KB based on current position
        p.update(b)
    # Handle win/lose/quit conditions
    if(p.dead):
        print "You have lost.\nScore: %d" % (p.score)
    if(p.win):
        print "You have won!\nScore: %d" % (p.score)
    if(p.quit):
        print "You quit.\nScore: %d" % (p.score)
    
        
          
if __name__ == '__main__':
    main()