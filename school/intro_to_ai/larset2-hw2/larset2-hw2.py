# Tate Larsen
# Intro to AI
# Homework 2
# Hunt the Wumpus

# Usage:
#  python larset2-hw2.py <MAP_FILE>

# Tested with Python 2.7.3

import string
import copy
import sys

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
    def update(self):
        self.percept_map[self.position[0]][self.position[1]] = self.percept.copy() # Copy in the current location's percept
        self.percept_map[self.position[0]][self.position[1]]['V'] = True           # Set current location as visited
        
    def move(self, cmd, b):
        # Handle 'Quit' 'Q' and 'Exit'
        if(cmd.lower() == 'q' or cmd.lower() == 'quit' or cmd.lower() == 'exit'):
            self.quit = True
            return
        # Handle 'More'
        if(cmd.lower() == 'more'):
            print "Additional Commands:\n\tQUIT/Q/EXIT\n\tPRINTKB/KB"
            return
        # Handle 'kb' and 'printkb'
        if(cmd.lower() == 'kb' or cmd.lower() == 'printkb'):
            tmp = copy.deepcopy(self.percept_map)
            tmp.reverse() # Flip it
            for l in tmp:
                print l # Print it
            return
        # Handle 'printmap' and map
        if(cmd.lower() == 'map' or cmd.lower() == 'printmap'):
            tmp = copy.deepcopy(b.map)
            tmp.reverse() # Flip it
            for l in tmp:
                print l # Print it
        # Handle undefined input
        if(cmd.lower() != 'f' and cmd.lower() != 's' and cmd.lower() != 'l' and cmd.lower() != 'r'):
            print "Command Not Recognized: Please try again."
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
                    
def main():
    # Check usage
    if not (len(sys.argv) == 2):
        print "Usage: python larset2-hw2.py <MAP_FILE>"
        return
    # Generate the board and player
    b = board(sys.argv[1])
    p = player(b)
    p.update() # Initial update to insert starting position into Knowledge Base
    
    while(not p.dead and not p.win and not p.quit):
        # Print what we see
        p.print_status(b)
        # Get input
        inp = raw_input("What would you like to do? Please enter command [R,L,F,S, more]:\n> ")
        # Process input
        p.move(inp, b)
        #Update KB based on current position
        p.update()
    # Handle win/lose/quit conditions
    if(p.dead):
        print "You have lost.\nScore: %d" % (p.score)
    if(p.win):
        print "You have won!\nScore: %d" % (p.score)
    if(p.quit):
        print "You quit.\nScore: %d" % (p.score)
    
        
          
if __name__ == '__main__':
    main()