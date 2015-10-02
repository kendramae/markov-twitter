from sys import argv
from kmarkov import KSimpleMarkovGenerator

class KMarkovTwitterBot(KSimpleMarkovGenerator):

    MAX_LENGTH = 140

    def create_tweet(self):
        """returns a string of less than MAX_LENGTH from markov chains
        """
        long_text = self.make_text()

        if len(long_text) > 140:
            tweet_rough_draft = long_text[:self.MAX_LENGTH + 1]

            # If rough draft of tweet contains end-type (., ?, !) punctuation, cut off the tweet at
            # last instance of same.
            if any(punc in tweet_rough_draft for punc in [".", "?", "!"]):
                while True:
                    if tweet_rough_draft.endswith((".","?","!", ".\"", ".'", "?\"", "!\"", "!'", "?'")):
                        break
                    else:
                        tweet_rough_draft = tweet_rough_draft[:len(tweet_rough_draft) - 1]

            tweet = tweet_rough_draft

        else:
            tweet = long_text

        return tweet


if __name__ == '__main__':

    size_of_ngram = int(argv[1])

    #get filepaths from command line
    input_path_list = argv[2:]

    ## instantiate generator here
    twitter_bot = KMarkovTwitterBot(size_of_ngram, input_path_list)

    # Produce random text
    for i in range(5):
        tweet = twitter_bot.create_tweet()
        print tweet + "\n"
