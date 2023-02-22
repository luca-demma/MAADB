import mysql_functions
import constants
import wordcloud

mysql_functions.mysql_connect()

for sentiment in constants.TWITTER_SENTIMENTS:

	words_count_sum_QUERY = '''
		-- get count for every word in tweets by sentiment  (WORDCLOUD)
		SELECT WORD_TWEET.WORD, SUM(WORD_TWEET.WORD_COUNT ) as W_COUNT
		FROM WORD_TWEET 
		JOIN TWEET
		ON WORD_TWEET.TWEET_ID = TWEET.ID 
		WHERE TWEET.SENTIMENT = '%s'
		GROUP BY WORD_TWEET.WORD
		ORDER BY W_COUNT DESC;
	'''%(sentiment)

	words_count_sum = mysql_functions.exec_query(words_count_sum_QUERY, False, False, True)
	print(words_count_sum)

mysql_functions.close_connection()
