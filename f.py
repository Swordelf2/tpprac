from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords

corpus = [
        'This is the first document',
        'This is the second document',
        'This is another one',
        'Yet another one']

# Init TF-IDF vectorizer, vectorize the documents with stopwords
vectorizer = TfidfVectorizer()
stop_words = stopwords.words('russian')
analyzer = vectorizer.build_analyzer()
for word in stopwords.words('english'):
    stop_words.extend(analyzer(word))

vectorizer.stop_words = stop_words

# TODO maybe cut-off here
X = vectorizer.fit_transform(corpus)

print(stop_words)
print(vectorizer.get_feature_names())
print(X.shape)
print(X)
