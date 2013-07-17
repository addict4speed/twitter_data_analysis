#Q: what is the sys library
#This module provides access to some variables used or maintained by the interpreter and to functions 
#that interact strongly with the interpreter. It is always available
import sys
import json
import string
import codecs

#import the sentiment score file
def initSentiment(sentiment_filename):
    #encoding is necessary because there are characters that do not conform to ASCII chart
    sentiment_words = codecs.open(sentiment_filename, "r", encoding = "utf-8")
    scores = {}
    for line in sentiment_words:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.
    sentiment_words.close()
    return scores

def initTweet(tweet_filename):
    tweets = []
    tweet_file = open(tweet_filename, "r")
     
    for line in tweet_file:
        #Q: What's the difference between json.loads() and json.load()
        #A: The functions with an s take string parameters. The others take file streams        
        tweets.append(json.loads(line))
    tweet_file.close()
    return tweets

def filterPunctuation(content):
    words = ""
    for i in range(len(content)):
            if content[i] not in string.punctuation:
                    words += content[i]
    return words

def calculate_tweet_sentiment(words, scores):
    total = 0
    for word in words:
        for sentiment in scores:
            if word == sentiment:
                total += scores[sentiment]
                break
    return total
    
def main():    
    sentiment_filename = "AFINN-111.txt"
    tweet_filename = "output.txt"
    
    scores = initSentiment(sentiment_filename)
    tweets = initTweet(tweet_filename)
    sentiment = codecs.open("sentiment_score.txt", "w", encoding = "utf-8")
    for tweet in tweets:
        if  "text" in tweet and tweet["lang"] == "en":
            print tweet["text"]
            content = tweet["text"]
            words = filterPunctuation(content)
            words = words.lower().split()
            sentiment_score = calculate_tweet_sentiment(words, scores)
            print sentiment_score
            sentiment.write(content + "\n")
            sentiment.write(str(sentiment_score) + "\n\n")

    sentiment.close()
    
if __name__ == '__main__':
    main()


    