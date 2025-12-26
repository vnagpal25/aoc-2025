# TrieNode defines each node in the Trie
class TrieNode:
    def __init__(self):
        self.children = {} # children as a dictionary, map letters to TrieNodes
        self.is_end_of_word = False # by default it should be false as not every prefix is a word

# Trie implements full prefix Trie
class Trie:
    def __init__(self, word_list=None):
        self.root = TrieNode()
        if word_list:
            for word in word_list:   
              self.insert(word)

    def insert(self, word):
        node = self.root
        for char in word:
            # create a new child if the letter doesn't exist at this level
            if char not in node.children:
                node.children[char] = TrieNode()
            # move to child
            node = node.children[char]
        node.is_end_of_word = True # mark it as the end of a word

    def search_prefix(self, prefix): # returns True if the prefix exists in the Trie
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def search_word(self, word): # returns True if the prefix exists in the Trie
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
