import mysql_functions
import constants
import helpers
import time


mysql_functions.mysql_connect()

time_start = time.time()

# Wordcount WORDS
for sentiment in constants.TWITTER_SENTIMENTS:
	print("GENERATING WORDS %s WORDCLOUD" % sentiment)

	words_count_sum_QUERY = '''
		-- get count for every word in tweets by sentiment  (WORDCLOUD)
		SELECT WORD_TWEET.WORD, SUM(WORD_TWEET.WORD_COUNT ) as W_COUNT
		FROM WORD_TWEET
		JOIN TWEET
		ON WORD_TWEET.TWEET_ID = TWEET.ID
		WHERE TWEET.SENTIMENT = '%s'
		GROUP BY WORD_TWEET.WORD
		ORDER BY W_COUNT DESC;
	''' % sentiment

	words_count_sum = mysql_functions.exec_query(words_count_sum_QUERY, False, False, True)

	# converting tuples results to dict
	words_count_sum = dict((x, int(y)) for x, y in words_count_sum)

	helpers.word_cloud(words_count_sum, sentiment + "_words")

# Wordcount EMOJI
for sentiment in constants.TWITTER_SENTIMENTS:
	print("GENERATING EMOJI %s WORDCLOUD" % sentiment)

	emoji_count_QUERY = '''
			SELECT EMOJI.CODE, COUNT(EMOJI.CODE) AS OCCURENCES
			FROM EMOJI
			JOIN TWEET
			ON EMOJI.TWEET_ID  = TWEET.ID
			WHERE TWEET.SENTIMENT = '%s'
			GROUP BY EMOJI.CODE
			ORDER BY OCCURENCES DESC;
		''' % sentiment

	emoji_count = mysql_functions.exec_query(emoji_count_QUERY, False, False, True)

	# converting tuples results to dict
	emoji_count = dict((x, int(y)) for x, y in emoji_count)

	helpers.word_cloud(emoji_count, sentiment + "_emojis", True)

# Wordcount EMOTICONS
for sentiment in constants.TWITTER_SENTIMENTS:
	print("GENERATING EMOTICON %s WORDCLOUD" % sentiment)

	emoticon_count_QUERY = '''
			SELECT EMOTICON.STRING, COUNT(EMOTICON.STRING) AS OCCURENCES
			FROM EMOTICON 
			JOIN TWEET
			ON EMOTICON.TWEET_ID  = TWEET.ID 
			WHERE TWEET.SENTIMENT = '%s'
			GROUP BY EMOTICON.STRING
			ORDER BY OCCURENCES DESC;
		''' % sentiment

	emoticon_count = mysql_functions.exec_query(emoticon_count_QUERY, False, False, True)

	# converting tuples results to dict
	emoticon_count = dict((x, int(y)) for x, y in emoticon_count)

	helpers.word_cloud(emoticon_count, sentiment + "_emoticons")

time_end = time.time()
time_lapsed = time_end - time_start
print("TIME SQL WORDCLOUDS " + str(time_lapsed))

mysql_functions.close_connection()
