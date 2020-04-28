import csv
import codecs
import pickle
import nltk
import re

from nltk import NaiveBayesClassifier, classify
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from operator import itemgetter
from pymystem3 import Mystem
from itertools import chain
from random import shuffle

# Стоп-слова для очистки токенов
STOP_WORDS = stopwords.words("russian")


def read_tweets():
    """
    Чтение позитивных и негативных твитов
    :return: список твитов
    """
    with codecs.open(
            'tonality-analysis/tweets/positive.csv', 'r', 'utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        pos_tweets = tuple(map(itemgetter(3), reader))

    with codecs.open(
            'tonality-analysis/tweets/negative.csv', 'r', 'utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        neg_tweets = tuple(map(itemgetter(3), reader))

    return pos_tweets, neg_tweets


def lemmatize_sentence(tokens):
    """
    Получение 'чистых' токенов твита
    :param tokens: токены одного твита
    :return: список 'чистых' токенов
    """
    # mystem = Mystem()
    # lemmatized_sentence = []
    cleaned_tokens = []
    for word, tag in pos_tag(tokens=tokens, lang='rus'):
        word = re.sub('[^А-Яа-я]', '', word)
        # fixme нужна нормализация? Все слова получают тэг = 'S'
        # lemmatized_sentence.append(mystem.lemmatize(word))
        # word, _ = mystem.lemmatize(word)
        if word and word.lower() not in STOP_WORDS:
            cleaned_tokens.append(word.lower())

    return cleaned_tokens


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


def save_classifier(classifier):
    """
    Сохранение полученного классификатора для дальнейшего использования
    :param classifier:
    :return:
    """
    f = open('tonality-analysis/my_classifier.pickle', 'wb')
    pickle.dump(classifier, f, -1)
    f.close()


def load_classifier():
    """
    Загрузка классификатора
    :return:
    """
    f = open('tonality-analysis/my_classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier


# Получение твитов из файлов
positive_tweets, negative_tweets = read_tweets()

# Возьмём по 10000 твитов из каждого набора
positive_tweets = positive_tweets[:10000]
negative_tweets = negative_tweets[:10000]

# Получение всех токенов в твитах
positive_tweet_tokens = map(nltk.word_tokenize, positive_tweets)
negative_tweet_tokens = map(nltk.word_tokenize, negative_tweets)

# Получение 'чистых' токенов
clean_positive_tweet_tokens = map(lemmatize_sentence, positive_tweet_tokens)
clean_negative_tweet_tokens = map(lemmatize_sentence, negative_tweet_tokens)

# Получение данных
positive_tokens_for_model = get_tweets_for_model(clean_positive_tweet_tokens)
negative_tokens_for_model = get_tweets_for_model(clean_negative_tweet_tokens)

positive_dataset = ((tweet_dict, 'Positive')
                    for tweet_dict in positive_tokens_for_model)
negative_dataset = ((tweet_dict, 'Negative')
                    for tweet_dict in negative_tokens_for_model)
dataset = list(chain(positive_dataset, negative_dataset))
shuffle(dataset)
train_data = dataset[:7000]
test_data = dataset[7000:]

classifier = NaiveBayesClassifier.train(train_data)

save_classifier(classifier)

saved_classifer = load_classifier()
print('Accuracy is:', classify.accuracy(saved_classifer, test_data))

custom_tweet = 'Ненавижу людей'
custom_tokens = lemmatize_sentence(nltk.word_tokenize(custom_tweet))
print(custom_tweet,
      saved_classifer.classify(dict([token, True] for token in custom_tokens)))
