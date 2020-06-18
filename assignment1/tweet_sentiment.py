import sys
import json

def _tostring(text):
    if isinstance(text, unicode):
        return text.encode('utf-8')
    elif isinstance(text, list):
        return [_tostring(word) for word in text]

def hw(scores, tweet_line):

    out = json.loads(tweet_line)
    tweet_score = 0
    if 'text' in out.keys():
        tweet_text = out['text'].split(" ")
        tweet_text = _tostring(tweet_text)
        for word in tweet_text:
            if word in scores.keys():
                tweet_score += scores[word]
    return tweet_score



def main():

    scores = {}  # initialize an empty dictionary
    sent_file = open(sys.argv[1]) #"AFINN-111.txt"
    # sent_file = open("AFINN-111.txt") #
    tweet_file = open(sys.argv[2]) #three_minutes_tweets
    # tweet_file =open("problem_1_submission.txt")
    for sent_line in sent_file.readlines():
        term, score = sent_line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    for line in tweet_file:
        print(hw(scores, line))

if __name__ == '__main__':
    main()
