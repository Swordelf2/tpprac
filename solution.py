from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords

class Solution:
    def __init__(self):
        # Init vectorizer
        self.vectorizer = TfidfVectorizer()
        stop_words = stopwords.words('russian')
        analyzer = self.vectorizer.build_analyzer()
        for word in stopwords.words('english'):
            stop_words.extend(analyzer(word))
        self.vectorizer.stop_words = stop_words

        # Init labels
        self.labels = {'Вредоносное ПО', 'Инцидент', 'Угроза',
                'Уязвимость', 'Прочее', 'Эксплойт'}

        # Init Log Regression model for every label

    
    # Train corpus: List[Tuple[str, str, Dict[str, Set[str]]]]
    def train(self, train_corpus):
        # Xs
        docs = []
        # Ys for each label
        Y = {label: [] for label in self.labels}

        for corpus_el in train_corpus:
            for label_set in corpus_el[2].values():
                docs.append(corpus_el[1])
                for label in self.labels:
                    if label in label_set:
                        Y[label].append(1)
                    else:
                        Y[label].append(0)

        # Run tokenization and TF-IDF feature extraction
        X = self.vectorizer.fit_transform(docs)

        # Fit into LogisticRegression

    # news: List[Tuple[str, str]]
    # Returns List[Set[str]] - list of sets of labels
    def predict(self, news):
        return [self.labels]
