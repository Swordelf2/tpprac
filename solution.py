from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from nltk.corpus import stopwords

class Solution:
    def __init__(self):
        # Init vectorizer
        self.vectorizer = CountVectorizer()
        stop_words = stopwords.words('russian')
        analyzer = self.vectorizer.build_analyzer()
        for word in stopwords.words('english'):
            stop_words.extend(analyzer(word))
        self.vectorizer.stop_words = stop_words

        # Init labels
        self.labels = {'Вредоносное ПО', 'Инцидент', 'Угроза',
                'Уязвимость', 'Эксплойт'}
        self.label_other = 'Прочее'

        # Init Log Regression classifier for every label
        self.clf = {label: LogisticRegression(
            solver = 'lbfgs', random_state=0,
            max_iter = 4000)
                for label in self.labels}
    
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
        for label in self.labels:
            self.clf[label].fit(X, Y[label])

    # news: List[Tuple[str, str]]
    # Returns List[Set[str]] - list of sets of labels
    def predict(self, news):
        docs = [news_el[1] for news_el in news]
        X = self.vectorizer.transform(docs)

        result_label_sets = [set() for i in range(len(docs))]

        for label in self.labels:
            predictions = self.clf[label].predict(X)
            for label_set, p in zip(result_label_sets, predictions):
                if p == 1:
                    label_set.add(label)

        # Add 'Прочее' to every empty label set
        for label_set in result_label_sets:
            if len(label_set) == 0:
                label_set.add(self.label_other)

        return result_label_sets
