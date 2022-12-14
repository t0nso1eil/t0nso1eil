import collections
import math


class NaiveBayesClassifier:
    def __init__(self, alpha=1):
        """Initialize classifier with smoothing parameter alpha."""
        self.alpha = alpha
        self.types = set()
        self.words = set()
        self.word_dict = dict()
        self.type_dict = dict()

    def fit(self, texts, types):
        """Fit Naive Bayes classifier according to X, y."""
        self.types = set(types)
        self.words = set()
        self.word_dict = dict()
        self.type_dict = dict()
        for type in self.types:
            self.word_dict[type] = collections.Counter()
            self.type_dict[type] = 0
        for i in range(0, len(texts)):
            self.type_dict[types[i]] += 1
            for word in texts[i].split():
                self.words.add(word)
                self.word_dict[types[i]][word] += 1

    def predict(self, texts):
        """Perform classification on an array of test vectors X."""
        guess_types = []
        for i in range(0, len(texts)):
            max_type = None
            max_prob = -math.inf
            for type in self.types:
                prob = math.log(self.type_dict[type] / sum(self.type_dict.values()))
                for word in texts[i].split():
                    prob += math.log(
                        (self.word_dict[type][word] + self.alpha)
                        / (sum(self.word_dict[type].values()) + self.alpha * len(self.words))
                    )
                print(prob)
                if prob > max_prob:
                    max_prob = prob
                    max_type = type
            guess_types.append(max_type)
        return guess_types

    def score(self, texts_test, types_test):
        """Returns the mean accuracy on the given test data and labels."""
        guess_types = self.predict(texts_test)
        sum = 0
        for i in range(0, len(guess_types)):
            if guess_types[i] == types_test[i]:
                sum += 1
        return sum / len(guess_types)
