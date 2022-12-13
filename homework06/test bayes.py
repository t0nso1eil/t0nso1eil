from string import punctuation
from sklearn.metrics import accuracy_score
from bayes import NaiveBayesClassifier

def read_sms():
    with open("data/SMSSpamCollection", "r", encoding="utf-8") as f:
        text = f.readlines()
    types = []
    texts = []
    for i in range(0, len(text)):
        types.append(text[i].split("\t")[0])
        texts.append(text[i].split("\t")[1])
    return texts, types


def template_texts(texts, types):
    temp = []
    for text in texts:
        temp.append(text.lower())
    texts = temp
    temp = []
    for text in texts:
        temp.append(text.replace("\n", " ").replace("\r", " "))
    texts = temp
    temp = []
    for text in texts:
        temp.append(text.split())
    texts = temp
    temp = []
    for text in texts:
        words = []
        for word in text:
            if word not in punctuation:
                words.append(word)
        temp.append(words)
    texts = temp
    temp = []
    for text in texts:
        temp.append(" ".join(text))
    texts = temp
    temp = []
    for type in types:
        if type == "ham":
            temp.append(0)
        else:
            temp.append(1)
    return texts, types


def split_data(texts, types):
    ind = int(len(texts) * 0.7)
    known_texts = texts[:ind]
    known_types = types[:ind]
    guess_texts = texts[ind:]
    expect_types = types[ind:]
    return known_texts, known_types, guess_texts, expect_types


if __name__ == "__main__":
    types, texts = read_sms()
    types, texts = template_texts(types, texts)
    known_texts, known_types, guess_text, expect_types = split_data(types, texts)
    class_bot = NaiveBayesClassifier()
    class_bot.fit(known_texts, known_types)
    guess_types = class_bot.predict(guess_text)
    print("Accuracy: ", accuracy_score(expect_types, guess_types))
