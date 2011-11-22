# Tate Larsen
# Programming in Python
# Homework 3

class TrieNode:
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
            If the word is not found, return None, else return the containing TrieNode
        """
        node = self
        for c in word:
            if c not in node.children:
                return None
            else:
                node = node.children[c]
        return node



def generateWordFindPuzzle(words, numwords, rows, cols):
    wordTrie = TrieNode()
    for word in words:
        wordTrie.insert(word)
        
    hiddenwords = []
    puzzle = ""
    
def findWords(words, puzzle):
    wordTrie = TrieNode()
    for word in words:
        wordTrie.insert(word)
        
    wordsFound = []

    pass
    
def generateDoubleWordSquare(words, size):
    wordTrie = TrieNode()
    for word in words:
        wordTrie.insert(word)
        
    pass
    
def main():
    wordList = open("ospd.txt", "r").read().upper().split()
    print(wordList[: 10])
    
if __name__ == "__main__":
    main()
    
    
