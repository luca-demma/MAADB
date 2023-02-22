import constants
import mysql_functions
import helpers

mysql_functions.mysql_connect()

for sentiment in constants.LEXICAL_RESOURCES_FILES:
	for file_name in constants.LEXICAL_RESOURCES_FILES[sentiment]:
		for source in constants.LEXICAL_RESOURCES_SOURCES:
			if source in file_name:
				words_count = helpers.count_file_lines(constants.LEXICAL_RESOURCES_PATH + sentiment + "/" + file_name)
				query = "INSERT INTO SENTIMENT_R_LEXICAL_RESOURCE (SENTIMENT, LEXICAL_RESOURCE, WORDS_COUNT) VALUES ('%s', '%s', %s);"%(sentiment.lower(), source, words_count)
				mysql_functions.exec_query(query, True)

mysql_functions.close_connection()
