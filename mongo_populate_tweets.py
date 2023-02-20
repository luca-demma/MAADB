import mongo_functions
from tqdm import tqdm


def populate(tweets):
	mongo_functions.mongo_connect()

	for sentiment in tqdm(tweets):
		print(sentiment)

		records = []

		for tweet in tweets[sentiment]:
			tweet['sentiment'] = sentiment
			records.append(tweet)

		mongo_functions.insert_many('tweet', records)


	mongo_functions.mongo_disconnect()
