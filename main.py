#!/usr/bin/python3
import json
import pprint as pp

from solution import Solution

from collections import Counter

test_data_proportion = 0.3  

labels = {'Вредоносное ПО', 'Инцидент', 'Угроза', 'Уязвимость', 'Прочее', 'Эксплойт'}

with open("dataset.json", "r") as dataset_json_file:
    json_els = json.loads(dataset_json_file.read())

# Construct corpus =
# Dict{questionId, [Tuple(title, text, dict[user, Set[label]])]}
corpus = {}
for el in json_els:
    questionId = el['questionId']
    try:
        corpus_el = corpus[questionId]
    except KeyError:
        corpus_el = corpus.setdefault(questionId,
                (el['title'], el['text'], {}))

    # Insert current user's labels into the dict of this element
    corpus_el[2][el['userId']] = set(el['labels'])

corpus = list(corpus.values())
# Split into train and test
split_index = int(test_data_proportion * len(corpus))
test_corpus = corpus[: split_index]
train_corpus = corpus[split_index :]

# Init the solution
solution = Solution()

# Train
solution.train(train_corpus)

# Test
tp, tn, fp, fn = 0, 0, 0, 0

for el in train_corpus:
    # Extract the news itself
    news = (el[0], el[1])
    # Calculate the ground truth as the set of labels
    # which were picked by at least 2/3s of all people
    label_pick_list = el[2].values();
    total_picks = len(label_pick_list)
    c = Counter()
    for label_pick in label_pick_list:
        c.update(label_pick)

    gold_labels = {counter_item[0]
            for counter_item in c.items()
            if counter_item[1] > 2/3 * total_picks}
    

    # Predict with the solution
    predicted_labels = solution.predict([news])[0]

    # Compare to the gold labels
    for label in labels:
        pred = label in predicted_labels
        gold = label in gold_labels
        if pred and gold:
            tp += 1
        elif not pred and not gold:
            tn += 1
        elif pred and not gold:
            fp += 1
        elif not pred and gold:
            fn += 1
        #print(predicted_labels, gold_labels)
        #print("tp = {}\ntn={}\nfp={}\nfn={}".format(tp, tn, fp, fn))


precision = tp / (tp + fp)
recall = tp / (tp + fn)
F1 = 2 * precision * recall / (precision + recall)
print("tp={}\ntn={}\nfp={}\nfn={}".format(tp, tn, fp, fn))
print("precision = {}\nrecall={}".format(precision, recall))
print("F1 = {}".format(F1))

