import pandas as pd
import re
import numpy as np

# Library which parses text and removes html tags
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

train = pd.read_csv("data/labeledTrainData.tsv", header=0, delimiter="\t", quoting=3)

def review_to_words(raw_review):
	review_text = BeautifulSoup(raw_review, "html.parser").get_text()
	letters_only = re.sub("[^a-zA-Z]", " ", review_text)
	words = letters_only.lower().split()
	stops = set(stopwords.words("english"))	
	meaningful_words = [w for w in words if not w in stops]

	return (" ".join(meaningful_words))


num_reviews = train["review"].size
clean_train_reviews = []

print("Cleaning and parsing the training set movie reviews...\n")
for i in range(0, num_reviews):
	if( (i+1)%1000 == 0 ):
		print("Review %d of %d\n" % ( i+1, num_reviews ))
	clean_train_reviews.append(review_to_words(train["review"][i]))


vectorizer = CountVectorizer(analyzer="word", tokenizer=None, preprocessor=None, stop_words=None, max_features=5000)
train_data_features = vectorizer.fit_transform(clean_train_reviews)
train_data_features = train_data_features.toarray()

print("Training random forest ...")
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit(train_data_features, train["sentiment"])

print("Testing ...")
test = pd.read_csv("data/testData.tsv", header=0, delimiter="\t", quoting=3)
num_reviews = len(test["review"])
clean_test_reviews = []

for i in range(0,num_reviews):
    if( (i+1) % 1000 == 0 ):
    	print("Review %d of %d\n" % (i+1, num_reviews))
    clean_review = review_to_words(test["review"][i])
    clean_test_reviews.append( clean_review )

test_data_features = vectorizer.transform(clean_test_reviews)
test_data_features = test_data_features.toarray()

result = forest.predict(test_data_features)

output = pd.DataFrame(data={"id": test["id"], "sentiment": result})
output.to_csv("Bag_of_words_model.csv", index=False, quoting=3)




















