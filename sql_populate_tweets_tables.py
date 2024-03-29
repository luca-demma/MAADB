import mysql_functions
from tqdm import tqdm
import time


def populate(tweets):

	mysql_functions.mysql_connect()
	tweet_index = 0

	time_start = time.time()

	for sentiment in tqdm(tweets):
		tweets_records = []
		hashtags_records = []
		emojis_records = []
		words_records = []
		emoticons_records = []

		for tweet in tweets[sentiment]:
			tweet_index += 1

			tweets_records.append((tweet_index, tweet['lemmatized_text'], tweet['original_text'], sentiment))

			for hashtag in tweet['hashtags']:
				hashtags_records.append((hashtag, tweet_index))

			for emoji in tweet['emojis']:
				emojis_records.append((emoji, tweet_index))

			for emoticon in tweet['emoticons']:
				emoticons_records.append((emoticon, tweet_index))

			for word in tweet['word_count']:
				word_count = tweet['word_count'][word]
				words_records.append((word, tweet_index, word_count))

		print("SENTIMENT: " + sentiment)
		print("TWEETS RECORDS: " + str(len(tweets_records)))
		print("HASHTAGS RECORDS: " + str(len(hashtags_records)))
		print("EMOJIS RECORDS: " + str(len(emojis_records)))
		print("WORD_TWEET RECORDS: " + str(len(words_records)))

		populate_TWEET_query = "INSERT INTO TWEET (ID, LEMMATIZED_TEXT, ORIGINAL_TEXT, SENTIMENT) VALUES (%s , %s, %s, %s);"
		mysql_functions.insert_many(populate_TWEET_query, tweets_records)

		populate_HASHTAG_query = "INSERT INTO HASHTAG (HASHTAG, TWEET_ID) VALUES (%s , %s);"
		mysql_functions.insert_many(populate_HASHTAG_query, hashtags_records)

		populate_EMOJI_query = "INSERT INTO EMOJI (CODE, TWEET_ID) VALUES (%s , %s);"
		mysql_functions.insert_many(populate_EMOJI_query, emojis_records)

		populate_EMOTICON_query = "INSERT INTO EMOTICON (STRING, TWEET_ID) VALUES (%s , %s);"
		mysql_functions.insert_many(populate_EMOTICON_query, emoticons_records)

		populate_WORD_TWEET_query = "INSERT INTO WORD_TWEET (WORD, TWEET_ID, WORD_COUNT) VALUES (%s , %s, %s);"
		mysql_functions.insert_many(populate_WORD_TWEET_query, words_records)

	time_end = time.time()
	time_lapsed = time_end - time_start
	print("TIME SQL POPULATE TWEET " + str(time_lapsed))

	mysql_functions.close_connection()
