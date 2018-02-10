import pdb; pdb.set_trace()
import os, re, tweepy, random
from secrets import *
from time import gmtime, strftime

# ====== Individual bot configuration ==========================
bot_username = 'oinker_bot'
logfile_name = bot_username + ".log"
# ==============================================================

# Twitter authentication
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)
tweets = tweepy.Cursor(api.user_timeline).items()

vowels = "aeiouAEIOU"
constants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
##{"b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z", "y"}
querymatchdata = {'latin': ['pig']}
regex = "!@#$%^&*()_-=+}{][\|:;><,./?~`"


#https://github.com/torypeterschild/dream-bot/blob/master/bot.py
def get_tweet():
    """Get list of tweets matching a certain query"""
    pdb.set_trace()
    query = random.choice(querymatchdata['latin'])
    results = api.search(q=query, count=50)
    return results

def filter_tweets(_results):
    """Filter tweets that are retweets or contains mention/s, etc"""
    while True:
        _tweet = random.choice(_results)
        text = _tweet.text;

        if not (hasattr(_tweet, "retweeted_status") or
            # pdb.set_trace()
            _tweet.in_reply_to_status_id or
            _tweet.in_reply_to_screen_name or
            _tweet.truncated or
            "@" in text or
            "RT" in text or
            "#" in text):
            if create_tweet(text):
                break
            else:
                continue

##https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
def hasNumbers(_inputstring):
    return any(char.isdigit() for char in _inputstring)

def create_tweet(_text):
    pig_latin_output = []
    if "pig" not in _text:
        return False
    else:
        translate_pig_latin = _text.split()

        for word in translate_pig_latin:
            if len(word) > 1:
                if hasNumbers(word):
                    pig_latin_output.append(word)
                elif word in regex:
                    pig_latin_output.append(word)
                elif word[0] in vowels:
                    word=word+"way"
                    pig_latin_output.append(word)
                elif word[0] in constants:
                    if word[1] in constants:
                        word = word[2:]+word[0]+word[1]+"ay"
                        pig_latin_output.append(word)
                    else:
                        word = word[1:]+word[0]+"ay"
                        pig_latin_output.append(word)
                else:
                    pig_latin_output.append(word)

        _translated = " ".join(pig_latin_output)
        if tweet(_translated):
            return True

def tweet(text):
    """Send out the text as a tweet."""

    # Send the tweet and log success or failure
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        # errorobject = e.pop()
        log(e.response.text)
    else:
        log("Tweeted: " + text)

def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


if __name__ == "__main__":

    results = get_tweet()
    filter_tweets(results)
