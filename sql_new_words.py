import mysql_functions
import constants
import time

mysql_functions.mysql_connect()

time_start = time.time()

for sentiment in constants.TWITTER_SENTIMENTS:
	print("FINDING NEW WORDS: " + sentiment)
	new_words_query = '''
	INSERT INTO NEW_WORDS (WORD, W_COUNT)
	SELECT T.WORD, T.W_COUNT
	FROM (
		SELECT WORD_TWEET.WORD, SUM(WORD_TWEET.WORD_COUNT ) as W_COUNT
		FROM WORD_TWEET 
		JOIN TWEET
		ON WORD_TWEET.TWEET_ID = TWEET.ID 
		WHERE TWEET.SENTIMENT = '%s'
		GROUP BY WORD_TWEET.WORD
	) AS T
	LEFT JOIN (
		SELECT DISTINCT WORD_R_SOURCE.WORD 
		FROM WORD_R_SOURCE
		JOIN SENTIMENT_R_LEXICAL_RESOURCE
		ON WORD_R_SOURCE.SOURCE_ID = SENTIMENT_R_LEXICAL_RESOURCE.ID 
		WHERE SENTIMENT_R_LEXICAL_RESOURCE.SENTIMENT = '%s'
	) AS S
	ON T.WORD=S.WORD
	ORDER BY W_COUNT DESC
	'''%(sentiment, sentiment)

	mysql_functions.exec_query(new_words_query, True)


time_end = time.time()
time_lapsed = time_end - time_start
print("TIME SQL NEW WORDS " + str(time_lapsed))

mysql_functions.close_connection()