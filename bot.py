# Copyright (c) 2015–2016 Molly White
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, re, tweepy, random
from secrets import *
from time import gmtime, strftime
from wordfilter import wordfilter


# ====== Individual bot configuration ==========================
bot_username = 'oinker_bot'
logfile_name = bot_username + ".log"
# ==============================================================

# Twitter authentication
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)
tweets = tweepy.Cursor(api.user_timeline).items()

wordfilter = Wordfilter()

vowels = "aeiouAEIOU"
constants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
##{"b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z", "y"}
querymatchdata = {'latin': ['pig']}
regex = "!@#$%^&*()_-=+}{][\|:;><,./?~`"


#https://github.com/torypeterschild/dream-bot/blob/master/bot.py
def get_tweet():
    """Get list of tweets matching a certain query"""
    query = random.choice(data['latin'])
    results = api.search(q=query, count = 50)
    return results

def filter_tweets(results_):
    """Filter tweets that are retweets or contains mention/s, etc"""
    while True:
        tweet_ = results_.pop(0);
        text = tweet_.text;

        if not (hasattr(tweet_, "retweeted_stats") or
            toptweet.in_reply_to_status_id or
            toptweet.in_reply_to_screen_name or
            toptweet.truncated or
            "@" in text or
            "RT" in text or
            "#" in text or):
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

        translated_ = " ".join(pig_latin_output)
        if tweet(translated):
            return True

def tweet(text):
    """Send out the text as a tweet."""

    # Send the tweet and log success or failure
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        log(e.message)
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
    create_tweet()
