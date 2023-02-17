import constants
import mysql_functions

mysql_functions.mysql_connect()

for sentiment in constants.LEXICAL_RESOURCES_FILES:
	for file_name in constants.LEXICAL_RESOURCES_FILES[sentiment]:
		for source in constants.LEXICAL_RESOURCES_SOURCES:
			if source in file_name:
				query = "INSERT INTO SENTIMENT_R_LEXICAL_RESOURCE (SENTIMENT, LEXICAL_RESOURCE) VALUES ('" + sentiment + "' , '" + source + "');"
				mysql_functions.exec_query(query, True)

mysql_functions.close_connection()
