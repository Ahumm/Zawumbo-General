##################################################################
##                                                              ##
## Tate Larsen                                                  ##
## 11/28/2012                                                   ##
##                                                              ##
## ------------------------------------------------------------ ##
##                                                              ##
## Intro to AI - Homework 4                                     ##
##   Word Probability                                           ##
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
##   Read words from file :  python larset2-hw4.py <filename>   ##
##                                                              ##
##################################################################

import sys, operator, random

class probability_list:
    word_count = 0
    word_dict = {}
    
    def __init__(self):
        return
        
    def load_file(self, filename):
        f_input = []
        try:
            f = open(filename, "r")
            s = f.read()
            f.close()
            f_input = s.split()
        except IOError as e:
            # Problem opening or reading the file
            print "Error opening or reading file: ", e
            return
        except Exception as e:
            # Handle undexpected errors
            print "Unexpected error: ", e
            return
        
        # Now populate the dictionary
        self.populate(f_input)
        
    def populate(self, word_list):
        # Reset values
        self.word_count = 0
        self.word_dict = {}
        
        # Get total word count
        self.word_count = len(word_list)
        
        # Reverse the list for faster poping
        word_list.reverse()
        if word_list:
            w1 = word_list.pop().lower() # Pop the first word
            self.word_dict[w1] = [1,{}] # Add it to the dict
            
        while word_list:
            w2 = word_list.pop().lower() # Grab the next word
            if w1 in self.word_dict:
                self.word_dict[w1][0] += 1 # If w1 already in word_dict, increment the count
            else:
                self.word_dict[w1] = [1,{}] # Else add it as a new entry
            if(w2 in self.word_dict[w1][1]):
                self.word_dict[w1][1][w2] += 1 # If w2 in w1's following dict, increment the count
            else:
                self.word_dict[w1][1][w2] = 1 # Else add it as a new entry to the following dict
            w1 = w2 # Move forward
        # Handle the last word in the list
        if w1:
            if w1 in self.word_dict:
                self.word_dict[w1][0] += 1
            else:
                self.word_dict[w1] = [1,{}]
        return
        
    def query(self, q_word):
        q_word = q_word.lower() # Convert word to lowercase for ease of use
        
        # Handle the case where the word was not in the text
        if not q_word in self.word_dict:
            print "Failed to find \"%s\" in the text\t (probability=%.4f)\n" % (q_word, 0.0)
            return
        
        # Sort the words by they number of occurances
        sorted_word_freq = sorted(self.word_dict[q_word][1].iteritems(), key=operator.itemgetter(1))
        # Keep track of total occurances
        occurances = self.word_dict[q_word][0]
        # Flip to most frequent -> least frequest order
        sorted_word_freq.reverse()
        
        # handle where the word only occured at the end of the file
        if len(sorted_word_freq) == 0:
            print "No words found following \"%s\" (Word only occured at the end of the file)\n" % (q_word)
            return
        
        # Find the longest following word (for output formatting)
        longest = 0
        for w in sorted_word_freq:
            if len(w[0]) > longest: longest = len(w[0])
        
        # Pick a word at random from the following words
        rnd = random.randint(0,occurances-1) # Generate an int from 0 to the number of occurances
        for w in sorted_word_freq:
            rnd -= w[1] # Subtract the occurances of the current following word
            if rnd < 0: # If rnd falls below zero, print the current word as the choosen one
                print "Possible word pair:"
                print "\t%s %s (probability=%.4f)" % (q_word, w[0].ljust(longest + 2), float(w[1])/occurances)
                print ""
                break
        
        # Print the rest of the words
        print "All word paits with probability > 0:"
        for w in sorted_word_freq:
            print "\t%s %s (probability=%.4f)" % (q_word, w[0].ljust(longest + 2), float(w[1])/occurances)
            
        print ""
            
def main(argv):
    # Check command arguments
    if not len(argv) > 0:
        print "Usage: larset2-hw4.py <filename>"
        return
    
    # Creat and populate a new probability list
    p_l = probability_list()
    p_l.load_file(argv[0])
    
    while True:
        # Get user input
        in_word = raw_input("Please Input a word (exit() to exit): ")
        print ""
        
        # Check user input
        while len(in_word.split()) > 1:
            print "Invalid input!"
            in_word = raw_input("Please Input a single keyword (exit() to exit): ")
            print ""
        
        # Exit clause
        if(in_word == "exit()"): break
        
        # Query the probability list
        p_l.query(in_word)
        
if __name__ == "__main__":
    main(sys.argv[1:])