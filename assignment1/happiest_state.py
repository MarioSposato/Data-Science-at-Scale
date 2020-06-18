import sys
import json
from collections import defaultdict as d_dict


def _tostring(text):
    if isinstance(text, unicode):
        return text.encode('utf-8')
    elif isinstance(text, list):
        return [_tostring(word) for word in text]


def hw(scores, states, states_with_scores, tweet_file):
    for tweet_line in tweet_file:
        out = json.loads(tweet_line)
        tweet_score = 0
        if 'place' in out.keys():
            location = locate_us(states, out)
            if location is not '' and 'text' in out.keys():
                tweet_text = out['text'].split(" ")
                tweet_text = _tostring(tweet_text)
                for word in tweet_text:
                    if word in scores.keys():
                        tweet_score += scores[word]
                states_with_scores[location] += tweet_score
    max_s = states_with_scores.keys()[states_with_scores.values().index(max(states_with_scores.values()))]
    # print max_s, states_with_scores[max_s]
    print max_s

def locate_us(states, out):
    state_code = ''
    if out['place'] is not None and out['place']['country_code'] == 'US':
        state = out['place']['full_name'].split(', ')
        # print state
        if state[1] == 'USA':
            state_code = states.keys()[states.values().index(state[0])]
        elif state[1] in states.keys():
            state_code = state[1]
        else:
            pass
    return state_code


def main():
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    } # State dictonary
    states_with_score = d_dict(float)
    scores = {}  # initialize an empty dictionary
    sent_file = open(sys.argv[1]) #"AFINN-111.txt"
    # sent_file = open("AFINN-111.txt") #
    tweet_file = open(sys.argv[2]) #three_minutes_tweets
    # tweet_file =open("three_minutes_tweets.json")
    for sent_line in sent_file.readlines():
        term, score = sent_line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    hw(scores, states, states_with_score, tweet_file)


if __name__ == '__main__':
    main()
