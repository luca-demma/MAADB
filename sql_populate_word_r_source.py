import mysql_functions
import time


def populate(words):
	records = []

	mysql_functions.mysql_connect()

	time_start = time.time()

	for sentiment in words:
		for word in words[sentiment]:
			for source in words[sentiment][word]:
				source_id_query = "SELECT ID FROM SENTIMENT_R_LEXICAL_RESOURCE WHERE SENTIMENT = '%s' AND LEXICAL_RESOURCE = '%s';"%(sentiment, source)
				source_id = mysql_functions.exec_query(source_id_query, False, True)
				source_id = source_id[0]
				records.append((word, source_id))

	print(records)
	populate_WORD_R_SOURCE_query = "INSERT INTO WORD_R_SOURCE (WORD, SOURCE_ID) VALUES (%s , %s);"
	mysql_functions.insert_many(populate_WORD_R_SOURCE_query, records)

	time_end = time.time()
	time_lapsed = time_end - time_start
	print("TIME SQL POPULATE WORD_SOURCE " + str(time_lapsed))

	mysql_functions.close_connection()
