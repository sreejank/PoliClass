import re
import os
import html
from twython import Twython
from twython.exceptions import TwythonAuthError
from twython.exceptions import TwythonError

screen_name = 'SenSanders'
filename = 'texts/tweets/' + screen_name + '_d.txt'
include_retweets = False

all_tweets = []

CONSUMER_KEY = 'IHjarUj5gUmXIEDt8krIrljIs'
CONSUMER_SECRET =  'MrGops24RCQCgi0VgYbUsd2RGZh3oFBkRiMkoVAY26cOgQqrqG'



try:
	twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET)
	tweets = twitter.get_user_timeline(screen_name=screen_name, count=200, include_rts=include_retweets)
	oldest_id = tweets[-1]['id'] - 1
	new_tweets = [re.sub(r'[^\x00-\x7f]',r'', tweet['text'].replace("\n", " ")) for tweet in tweets]
	all_tweets.extend(new_tweets)

	
	rounds = 1

	while len(new_tweets) > 0 and rounds < 16:
		tweets = twitter.get_user_timeline(screen_name=screen_name, count=200, max_id=oldest_id, include_rts=include_retweets)
		oldest_id = tweets[-1]['id'] - 1
		new_tweets = [re.sub(r'[^\x00-\x7f]',r'', tweet['text'].replace("\n", " ")) for tweet in tweets]
		all_tweets.extend(new_tweets)

		
		rounds +=1


except TwythonError:
	print("Twython  error")
except TwythonAuthError:
	print("Twython auth error")
except Exception, e:
    print("Error getting twitter :" + str(e))

output = open(filename, 'w')

for t in all_tweets:
	output.write(t)
	output.write('\n')
	print("** " + t)

print('Got ' + str(len(all_tweets)) + ' tweets')