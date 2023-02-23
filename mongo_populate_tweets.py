import mongo_functions
from tqdm import tqdm
import time


def populate(tweets):

	mongo_functions.mongo_connect()

	time_start = time.time()

	for sentiment in tqdm(tweets):
		print(sentiment)

		records = []

		for tweet in tweets[sentiment]:
			tweet['sentiment'] = sentiment
			records.append(tweet)

		mongo_functions.insert_many('tweet', records)

	time_end = time.time()
	time_lapsed = time_end - time_start
	print("TIME MONGO POPULATE TWEET " + str(time_lapsed))


	mongo_functions.mongo_disconnect()
