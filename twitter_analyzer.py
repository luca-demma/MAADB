import constants
import helpers
import re
import emoji
import string
import contractions
import spacy
import json
from pqdm.processes import pqdm
import sql_populate_tweets_tables
import pickle
import os.path
from os import path

nlp = spacy.load("en_core_web_sm")
stopwords = nlp.Defaults.stop_words

# extending the slang dictionary
slang_json = helpers.read_slang_json()
for slang in slang_json:
	contractions.add(slang, slang_json[slang])


# per ogni sentiment tweet
def analyze_sentiment(tweet_path):
	tweets = {}
	sentiment = ""
	# prendiamo il sentiment in esame dal nome del file
	for s in constants.TWITTER_SENTIMENTS:
		if s in tweet_path:
			sentiment = s
			break
	# init the tweets object for the sentiment we're using
	tweets[sentiment] = []
	# leggiamo il file
	tweets_list = helpers.read_file(tweet_path)
	# per ogni tweet
	for tweet in tweets_list:
		tweet_original = tweet
		t_tmp = {}
		# eliminiamo i \n
		tweet = tweet.replace('\n', '')
		# eliminiamo URL e USERNAME
		tweet = tweet.replace('USERNAME', '')
		tweet = tweet.replace('URL', '')
		# hashtags list
		t_tmp['hashtags'] = re.findall(r"#(\w+)", tweet)
		# removing hashtags already processed
		for hashtag in t_tmp['hashtags']:
			tweet = tweet.replace('#' + hashtag, '')
		# extract emoji list
		t_tmp['emojis'] = emoji.distinct_emoji_list(tweet)
		# removing emojis already processed
		for e in t_tmp['emojis']:
			tweet = tweet.replace(e, '')
		# to_lower_case
		tweet = tweet.lower()
		# expanding contractions
		tweet = contractions.fix(tweet)
		# remove punctuation
		tweet = tweet.translate(str.maketrans('', '', string.punctuation))
		# lemmatization
		doc = nlp(tweet)
		empty_list = []
		for token in doc:
			empty_list.append(token.lemma_)

		tweet = ' '.join(map(str, empty_list))
		# remove stop words
		lst = []
		for token in tweet.split():
			if token.lower() not in stopwords:  # checking whether the word is not
				lst.append(token)  # present in the stopword list.
		tweet = ' '.join(lst)
		# count word occurrences
		t_tmp['word_count'] = helpers.word_count(tweet)
		t_tmp['lemmatized_text'] = tweet
		t_tmp['original_text'] = tweet_original
		tweets[sentiment].append(t_tmp)
		# print(json.dumps(t_tmp, indent=2))
	return tweets

tweets_result = {}

if not (path.exists('./data/tweets_analyzed.pickle')):
	tweets_list = pqdm(constants.TWITTER_DATASETS_PATHS, analyze_sentiment, n_jobs=constants.CPU_COUNT)

	for t in tweets_list:
		sentiment = list(t.keys())[0]
		tweets_result[sentiment] = t[sentiment]

	print("WRITING_TO_FILE")
	with open('./data/tweets_analyzed.txt', 'w') as f:
		f.write(json.dumps(tweets_result, indent=4))
	file = open('./data/tweets_analyzed.pickle', 'wb')
	pickle.dump(tweets_result, file)
else:
	print("READING_FROM_FILE")
	file = open('./data/tweets_analyzed.pickle', 'rb')
	tweets_result = pickle.load(file)

print("EXECUTING QUERIES")
sql_populate_tweets_tables.populate(tweets_result)

