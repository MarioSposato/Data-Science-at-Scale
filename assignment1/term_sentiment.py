import sys
import json
""" In this script I first read the entire tweet file, for each tweet I save the sentiment score in a dict indexed by the
    tweet id, and a missing_words dictionary, indexed by the word, where I save the tweets ids in which that word appears.
    Then I check every entry in this dictionary, and I associate to them a sentiment value, as the sum of sentiments
    of the tweets containing that word, divided by the number of those tweets.
    
"""

def _tostring(text):
    if isinstance(text, unicode):
        return text.encode('utf-8')
    elif isinstance(text, list):
        return [_tostring(word) for word in text]


def hw(scores, tweet_file):
    tweet_score_dict = {}
    missing_words = {}
    for tweet_line in tweet_file:
        out = json.loads(tweet_line)
        tweet_score = 0
        if 'text' in out.keys():
            tweet_text = out['text'].split(" ")
            tweet_text = _tostring(tweet_text)
            for word in tweet_text:
                if word in scores.keys():
                    tweet_score += scores[word]
                else:

                    if word in missing_words.keys():
                        ids = missing_words[word]
                        ids.append(out['id'])
                    else:
                        ids = [out['id']]

                    missing_words[word] = ids
            tweet_score_dict[out['id']] = tweet_score

    mis_words_score = {}
    for word in missing_words.keys():
        value = 0
        for idx in missing_words[word]:
            value += tweet_score_dict[idx]
        mis_words_score[word] = float(value/len(missing_words[word]))
    return mis_words_score


def main():
    scores = {}  # initialize an empty dictionary
    sent_file = open(sys.argv[1]) #"AFINN-111.txt"
    tweet_file = open(sys.argv[2]) #three_minutes_tweets
    for sent_line in sent_file.readlines():
        term, score = sent_line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    mis_words_score = hw(scores, tweet_file)
    for k, v in mis_words_score.items():
        print k+" "+str(v)


if __name__ == '__main__':
    main()
