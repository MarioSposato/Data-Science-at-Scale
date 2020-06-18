import sys
import json
from collections import defaultdict as d_dict
import re

def _tostring(text):
    if isinstance(text, unicode):
        text.encode('utf-8')
        text = re.sub('\W+', '', text)
        return text

    elif isinstance(text, list):
        return [_tostring(word) for word in text]

def frequency(tweet_file):

    freq_dict = d_dict(float)
    for tweet_line in tweet_file:
        out = json.loads(tweet_line)
        if 'text' in out.keys():
            # if out['lang'] == 'en':
            tweet_text = out['text'].split(" ")
            tweet_text = _tostring(tweet_text)
            for word in tweet_text:
                freq_dict[word] += 1.0

    tot = 0
    for val in freq_dict.values():
        tot += val
    for k in freq_dict.keys():
        freq_dict[k] /= tot

    return freq_dict


def main():

    tweet_file = open(sys.argv[1]) #three_minutes_tweets
    # tweet_file = open('problem_1_submission.txt')
    # tweet_file = open('three_minutes_tweets.json')

    freq_dict = frequency(tweet_file)
    for k, v in freq_dict.items():
        print "%s %.4f" % (k, v)


if __name__ == '__main__':
    main()
