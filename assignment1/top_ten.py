import sys
import json
from collections import defaultdict as d_dict
from collections import OrderedDict as o_dict

import re

def _tostring(text):
    if isinstance(text, unicode):
        text = text.encode('utf-8')
        text = re.sub('\W+', '', text)
        return text
    elif isinstance(text, list):
        return [_tostring(word) for word in text]

def top_ten(tweet_file):

    top_dict = d_dict(float)
    for tweet_line in tweet_file:
        out = json.loads(tweet_line)
        if 'entities' in out.keys():
            hashtag = out['entities']['hashtags']
            if len(hashtag) != 0:
                for h in hashtag:
                    hashtag_text = h['text']
                    hashtag_text = _tostring(hashtag_text)
                    top_dict[hashtag_text] += 1.0


    return top_dict


def main():

    tweet_file = open(sys.argv[1]) #three_minutes_tweets
    # tweet_file = open('problem_1_submission.txt')
    # tweet_file = open('three_minutes_tweets.json')

    top_dict = top_ten(tweet_file)
    o_dict(sorted(top_dict.items(), key=lambda t: t[0]))
    for k, v in top_dict.items()[:10]:
        print "%s %.2f" % (k, v)



if __name__ == '__main__':
    main()
