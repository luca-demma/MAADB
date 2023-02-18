import constants
import helpers
import re
import emoji
import string
import contractions
import spacy

nlp = spacy.load("en_core_web_sm")

# {
# 	sentiment:
# 		[
# 			{
# 				cleaned_text: "adas",
# 				hashtags: [],
#				emoji: []
# 			}
# 		]
# }
tweets = {}


# extending the slang dictionary
slang_json = helpers.read_slang_json()
for slang in slang_json:
	contractions.add(slang, slang_json[slang])


# per ogni sentiment tweet
for tweet_path in constants.TWITTER_DATASETS_PATHS:
	sentiment = ""
	# prendiamo il sentiment in esame dal nome del file
	for s in constants.TWITTER_SENTIMENTS:
		if s in tweet_path:
			sentiment = s
			break
	# leggiamo il file
	tweets_list = helpers.read_file(tweet_path)
	# per ogni tweet
	for tweet in tweets_list:
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
		stopwords = nlp.Defaults.stop_words
		lst = []
		for token in tweet.split():
			if token.lower() not in stopwords:  	# checking whether the word is not
				lst.append(token)  					# present in the stopword list.
		tweet = ' '.join(lst)
		print(tweet)
