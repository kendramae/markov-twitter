from random import choice
from sys import argv


class KSimpleMarkovGenerator(object):


    def __init__(self, size_of_ngram, input_path_list):
        self.size_of_ngram = size_of_ngram
        self.input_path_list = input_path_list
        self.chains = {}
        self.text_strings_list = []
        self.make_master_chains_dict()


    def open_and_read_files(self):
        """Opens each file in self.input_path_list and adds a string version of file's text
           to self.input_text_list.
        """

        for input_path in self.input_path_list:
            text_file = open(input_path)
            text_string = text_file.read()
            self.text_strings_list.append(text_string)


    def add_text_to_chains(self,text_string):
        """Takes a text string, adds its ngrams to self.chains; return None

        Takes a text string from self.text_strings_list and adds its markov chains to our self.chains 
        dictionary, with None as the value to the key of the final n words.
        A chain will be a key that consists of a tuple of (word1, word2, ..., wordn)
        and the value would be a list of the word(s) that follow those n words in the input text.

        Called by self.make_master_chains_dict() in __init__ -- does not need to be called directly.
        """
        
        word_list = text_string.split()
        word_list.append(None)

        #initialize first ngram (which will become the tuple/key) with the first n words in the text
        ngram_list = []
        for i in range(self.size_of_ngram):
            ngram_list.append(word_list[i])
        ngram = tuple(ngram_list)
        
        # for each word in our text, add it to the dictionary entry for the ngram preceeding it
        for i in range(self.size_of_ngram, len(word_list)):
            word = word_list[i]
            if ngram in self.chains:
                self.chains[ngram].append(word)
            else:
                self.chains[ngram] = [word]

            ngram = ngram[1:] + (word,)


    def make_master_chains_dict(self):
        
        """ 


        Calls self.open_and_read_files() to open list of files and add string versions to self.text_string_list, 
        then calls self.add_text_to_chains() to create our master dictionary of markov chains, self.chains.
        """

        # Open all files and add a string version of the text of each to self.text_string_list
        self.open_and_read_files()

        # Add chains from each text source to master chains dictionary
        for text_string in self.text_strings_list:
            self.add_text_to_chains(text_string)


    def make_text(self):
        """Looks at self.chains (dictionary of markov chains); returns random text."""

        ngrams = self.chains.keys()  # list of ngrams (which are tuples)
        active_ngram = choice(ngrams)  # pick a random starting n-gram

        # if our current starting n-gram doesn't begin with a capital, choose another until it does
        while not active_ngram[0][0].isupper():
            active_ngram = choice(ngrams)

        #put the initial n-gram into the list of words which will be joined to become new text
        text_list = list(active_ngram)

        # until we reach the end (flagged by a None from choice(possible_next_words)), keep picking 
        # a random word from the active ngram's list of followers
        while True:
            possible_next_words = self.chains[active_ngram]
            new_word = choice(possible_next_words)

            if new_word == None:
                break
            elif len(text_list) >= 500 and new_word.endswith((".", "?", "!")):
                text_list.append(new_word)
                break
            else:
                text_list.append(new_word)

                # set active_ngram to be new final n words
                active_ngram = active_ngram[1:] + (new_word,)

        #convert list into text string and return it
        text = " ".join(text_list)

        return text


if __name__ == '__main__':

    ##FIX ME TO TAKE CLASSES INTO ACCOUNT

    size_of_ngram = int(argv[1])

    #get filepaths from command line
    input_path_list = argv[2:]

    ## instantiate generator here
    generator = KSimpleMarkovGenerator(size_of_ngram, input_path_list)

    # Produce random text
    random_text = generator.make_text()

    print random_text
