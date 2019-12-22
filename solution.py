
class Solution:
    def __init__(self):
        self.labels = {'Вредоносное ПО', 'Инцидент', 'Угроза',
                'Уязвимость', 'Прочее', 'Эксплойт'}
    
    # Train corpus: List[Tuple[str, str, Dict[str, Set[str]]]]
    def train(self, train_corpus):
        print('nihuya ne trainim')


    # news: List[Tuple[str, str]]
    # Returns List[Set[str]] - list of sets of labels
    def predict(self, news):
        return [{}]
