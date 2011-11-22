# Tate Larsen
# Programming in Python
# Homework 3

import random

class TrieNode(object):
    """
        TrieNode object.
        Basically stores a dict of words beginning with this node plus a letter (the key in the dict).
    """
    def __init__(self):
        self.word = None
        self.children = {}
        
    def insert(self, word):
        """
            Add a word to the Trie.
        """
        node = self
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.word = word
        
    def search(self, word):
        """
            Search for a word within the Trie.
            If the word is not found, return None,
            else return the containing TrieNode
        """
        node = self
        for c in word:
            if c not in node.children:
                return None
            else:
                node = node.children[c]
        return node.word
        
    def hasChildren(self, word):
        """
            Search for a node within the Trie and checks if that node has children.
        """
        node = self
        for c in word:
            if c not in node.children:
                return False
            else:
                node = node.children[c]
        if len(node.children) > 0:
            return True
        return False
        
    def getChildren(self, word):
        """
            Search for a node within the Trie and returns its children.
        """
        node = self
        for c in word:
            if c not in node.children:
                return None
            else:
                node = node.children[c]
        if len(node.children) > 0:
            return node.children
        return None
        

class WordGrid(object):
    """
        Simple object storing a 2D grid of letters.
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.words = []
        self.grid = []
        
        # Populate with placeholder chars
        for i in range(rows):
            r = []
            for i in range(cols):
                r.append(".")
            self.grid.append(r)

    def __str__(self):
        """
            Convert to a string
        """
        stringGrid = ""
        for r in self.grid:
            for c in r:
                stringGrid += c
            stringGrid += "\n"
        return stringGrid[:-1]
        
    def __repr__(self):
        return self.__str__()
        
    def fillGrid(self):
        """
            Replace all placeholder '.' with random letters.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == ".":
                    self.grid[r][c] = random.choice(string.ascii_uppercase)
    
    def addWord(self, word, sR, sC, dR, dC):
        """
            Add a word starting from location (sR,sC) and moving in direction specified by dR and dC.
        """
        cR = sR
        cC = sC
        # Check if we're going out of bounds
        if ((cR + (len(word) * dR)) < 0 or
           (cC + (len(word) * dC)) < 0 or
           (cR + (len(word) * dR)) > self.rows or
           (cC + (len(word) * dC)) > self.cols):
            return
        # Fill in the word
        for c in word:
            self.grid[cR][cC] = c
            cR += dR
            cC += dC
            
    def checkWord(self, word, sR, sC, dR, dC):
        """
            Check if a word will fit starting from location (sR,sC) and moving in direction specified by dR and dC.
        """
        cR = sR
        cC = sC
        # Check if we're going out of bounds
        if ((cR + (len(word) * dR)) < 0 or
           (cC + (len(word) * dC)) < 0 or
           (cR + (len(word) * dR)) > self.rows or
           (cC + (len(word) * dC)) > self.cols):
            return
        # Check if we fit
        for c in word:
            # Bad overlap
            if (self.grid[cR][cC] != c and 
                self.grid[cR][cC] != '.'):
                return False
            cR += dR
            cC += dC
        return True
        
        
def generateWordFindPuzzle(words, numwords, rows, cols):
    # Check input
    if rows < 1 or cols < 1:
        print("Invalid grid size.")
        return None, None

    # Trim the list to only words short enough to fit
    wTrimmed = [x for x in words if len(x) <= max(rows,cols)]
    
    # Initialize the grid
    grid = WordGrid(rows,cols)
    addedWords = []
    
    # Start from the top left and see if we can put any words in here, break out of these loops if we reached numwords words added
    for r in range(rows):
        if len(addedWords) >= numwords:
            break
        for c in range(cols):
            if len(addedWords) >= numwords:
                break
            # Randomize the words
            random.shuffle(wTrimmed)
            # See if anything fits
            for w in wTrimmed:
                if len(addedWords) >= numwords:
                    break
                if w in addedWords:
                    continue
                # Check every orientation
                x = -1
                while x < 2:
                    y = -1
                    while y < 2:
                        if x == 0 and y == 0:
                            y += 1
                            continue
                        # If it will fit, add it
                        if grid.checkWord(w, r, c, x, y):
                            grid.addWord(w, r, c, x, y)
                            addedWords.append(w)
                            x = 2
                            y = 2
                        y += 1
                    x += 1
         
    # Couldn't add enough words
    if len(addedWords) < numwords:
        print( "No Possible Word Puzzle Found." )
        return None, None
                   
    # Fill in any empty spots
    grid.fillGrid()
    
    return str(grid), tuple(sorted(addedWords))

    
def findWords(words, puzzle):
    # Initialize the Trie with word list
    wordTrie = TrieNode()
    for word in words:
        wordTrie.insert(word)
    
    # Here to keep track of words as we find them
    wordsFound = set()
    
    # Break up the string
    grid = [list(x) for x in puzzle.split()]
    
    # Go through and check every substring in every orientation within the grid
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            x = -1
            while x < 2:
                y = -1
                while y < 2:
                    if y == 0 and x == 0:
                        y += 1
                        continue
                    cstr = ""
                    cr = r
                    cc = c
                    while 1:
                        # Out of bounds
                        if (cr < 0 or
                           cc < 0 or
                           cr >= len(grid) or
                           cc >= len(grid[0])):
                            break
                        else:
                            cstr += grid[cr][cc]
                            # Check forwards
                            if wordTrie.search(cstr):
                                wordsFound.add(cstr)
                            # Check backwards
                            if wordTrie.search(cstr[::-1]):
                                wordsFound.add(cstr[::-1])
                            cr += x
                            cc += y
                    y += 1
                x += 1
            
    
    return tuple(sorted(wordsFound))

class DoubleSquare(object):
    """
        Special grid to generate double word squares
    """
    def __init__(self, size, words):
        self.size = size
        self.grid = []
        
        for i in range(size):
            self.grid.append(['.'] * size)
            
        self.words = [x for x in words if len(x) == size]
        
        self.wordTrie = TrieNode()
        for word in self.words:
            self.wordTrie.insert(word)
            
        self.firstSol = None
            
    def row(self, i):
        """
            Grab a row
        """
        return self.grid[i]

    def col(self, i):
        """
            Grab a column
        """
        return [row[i] for row in self.grid]
    
    def __str__(self):
        """
            Convert to string form.
        """
        stringGrid = ""
        for r in self.grid:
            for c in r:
                stringGrid += c
            stringGrid += "\n"
        return stringGrid[:-1]
        
    def __repr__(self):
        return self.__str__()
        
    def fillSquare(self):
        # Try to fill the square
        self.fillSquare1(0)
        # Found a solution
        if self.firstSol:
            self.grid = self.firstSol
            return True
        # Did not find a solution
        return False
        
    def fillSquare1(self, depth):
        # Solution has been found, terminate
        if self.firstSol:
            return
            
        # Reached the bottom right corner of the grid, woo
        if depth > 2 * (self.size - 1):
            self.firstSol = self.grid
            return
        
        # Figure out what stage we're on and which way we're facing
        i = (depth + 1) // 2
        j = depth // 2
        d = depth % 2
        
        # Horizontal
        if d == 0:
            # Trim word list to just words that would fit in this row and shuffle it
            pre = "".join(self.row(i)[0:j])
            rem = [x for x in self.words if x.startswith(pre)]
            random.shuffle(rem)
            for w in rem:
                good = True
                # Put a word in here and check if it breaks things
                for x in range(j, self.size):
                    self.grid[i][x] = w[x]
                    c = self.col(x)[0:i+1]
                    if (len(c) != self.size and not self.wordTrie.hasChildren(c)) or (len(c) == self.size and not self.wordTrie.search(c)):
                        good = False
                        break
                # Didn't break, recurse
                if good:
                    self.fillSquare1(depth + 1)
                # Solution found, terminate
                if self.firstSol:
                    return
        # Vertical
        else:
            # Trim word list to just words that fould fin in this column and shuffle it
            pre = "".join(self.col(j)[0:i])
            rem = [x for x in self.words if x.startswith(pre)]
            random.shuffle(rem)
            for w in rem:
                good = True
                # Put a word in and see if it breaks things
                for y in range(i, self.size):
                    self.grid[y][j] = w[y]
                    c = self.row(y)[0:j+1]
                    if (len(c) != self.size and not self.wordTrie.hasChildren(c)) or (len(c) == self.size and not self.wordTrie.search(c)):
                        good = False
                        break
                # Didn't break, recurse
                if good:
                    self.fillSquare1(depth + 1)
                # Solution found, terminate
                if self.firstSol:
                    return
        
    
def generateDoubleWordSquare(words, size):
    # Check size of square (should really check 7 or 8 but meh)
    if size < 1 or size > 9:
        print("Invalid grid size.")
        return None
        
    # Make a square and try to fill it
    square = DoubleSquare(size, words)
    if square.fillSquare():
        # Succeeded
        return str(square)
    else:
        # Failed
        print("No Double Word Square Found.")
        return None
    
def main():
    # Load a dictionary
    wordList = open("ospd.txt", "r").read().upper().split()
    
    # Test generateWordFindPuzzle
    #g, w = generateWordFindPuzzle(wordList,10,20,20)
    #if g:
    #    print(g)
    #    print(w)
        # Test findWords
    #    fw = findWords(wordList, g)
    #    print(fw)
    #    print(len(fw))
        
    # Test generateDoubleWordSquare
    s = generateDoubleWordSquare(wordList, 5)
    print(s)
    
if __name__ == "__main__":
    main()
    
    
