import mysql_functions
import constants
import helpers

mysql_functions.mysql_connect()

perc = {}

for sentiment in constants.LEXICAL_RESOURCES_FILES:
	# calc perc solo per i sentiment di twitter dataset
	if sentiment.lower() in constants.TWITTER_SENTIMENTS:
		for file_name in constants.LEXICAL_RESOURCES_FILES[sentiment]:
			for source in constants.LEXICAL_RESOURCES_SOURCES:
				if source in file_name:
					sentiment = sentiment.lower()

					n_shared_words_QUERY = '''
						-- lista di parole presenti sia in lex_resource che in tweet per il sentiment in esame
						SELECT COUNT(T.WORD)
						FROM ( 
								SELECT DISTINCT WORD_TWEET.WORD
								FROM WORD_TWEET
								JOIN TWEET
								ON WORD_TWEET.TWEET_ID = TWEET.ID 
								WHERE TWEET.SENTIMENT = '%s'	
							 )  AS T
						JOIN ( 
								SELECT WORD_R_SOURCE.WORD
								FROM WORD_R_SOURCE
								JOIN SENTIMENT_R_LEXICAL_RESOURCE
								ON WORD_R_SOURCE.SOURCE_ID = SENTIMENT_R_LEXICAL_RESOURCE.ID 
								WHERE SENTIMENT_R_LEXICAL_RESOURCE.SENTIMENT = '%s' AND LEXICAL_RESOURCE = '%s'
							 ) AS S
						
						ON T.WORD=S.WORD
					'''%(sentiment, sentiment, source)

					n_lex_words_QUERY = '''
						-- count parole lex_resource per sentiment e per source in esame
						SELECT COUNT(WORD_R_SOURCE.WORD)
						FROM WORD_R_SOURCE
						JOIN SENTIMENT_R_LEXICAL_RESOURCE
						ON WORD_R_SOURCE.SOURCE_ID = SENTIMENT_R_LEXICAL_RESOURCE.ID 
						WHERE SENTIMENT_R_LEXICAL_RESOURCE.SENTIMENT = '%s' AND LEXICAL_RESOURCE = '%s'
					'''%(sentiment, source)

					n_twitter_words_QUERY = '''
						-- count parole tweet per sentiment 
						SELECT COUNT(DISTINCT WORD_TWEET.WORD)
						FROM WORD_TWEET
						JOIN TWEET
						ON WORD_TWEET.TWEET_ID = TWEET.ID 
						WHERE TWEET.SENTIMENT = '%s'
					'''%(sentiment)

					n_shared_words = mysql_functions.exec_query(n_shared_words_QUERY, False, True)[0]
					n_lex_words = mysql_functions.exec_query(n_lex_words_QUERY, False, True)[0]
					n_twitter_words = mysql_functions.exec_query(n_twitter_words_QUERY, False, True)[0]

					print("SENTIMENT: %s	SOURCE: %s\n" % (sentiment, source))
					print("n_shared_words: %s" % (str(n_shared_words)))
					print("n_lex_words: %s" % (str(n_lex_words)))
					print("n_twitter_words: %s\n" % (str(n_twitter_words)))

					perc_presence_lex_res = n_shared_words / n_lex_words
					perc_presence_twitter = n_shared_words / n_twitter_words


					print("perc_presence_lex_res: %s"%(str(perc_presence_lex_res)))
					print("perc_presence_twitter: %s"%(str(perc_presence_twitter)))
					print("-----------------------")

					perc[sentiment + "_" + source] = int(perc_presence_lex_res * 100)


mysql_functions.close_connection()

helpers.make_histogram(perc)
