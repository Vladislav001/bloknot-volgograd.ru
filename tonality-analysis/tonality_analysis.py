import csv
import codecs
import pickle
import nltk
import re
import sys

from nltk import NaiveBayesClassifier, classify
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from operator import itemgetter
from itertools import chain
from random import shuffle

sys.path.append('./')
from database import Database


# Стоп-слова для очистки токенов
STOP_WORDS = stopwords.words('russian')


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

    cleaned_tokens = []
    for word, tag in pos_tag(tokens=tokens, lang='rus'):
        word = re.sub('[^А-Яа-я]', '', word)

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
    f = open('tonality-analysis/my_classifier2.pickle', 'wb')
    pickle.dump(classifier, f, -1)
    f.close()


def load_classifier():
    """
    Загрузка классификатора
    :return:
    """
    f = open('tonality-analysis/my_classifier2.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier


def learn_model():
    """
    Обучение модели для определения тональности предложения
    """
    # Получение твитов из файлов
    positive_tweets, negative_tweets = read_tweets()

    # Возьмём по 100000 твитов из каждого набора
    positive_tweets = positive_tweets[:100000]
    negative_tweets = negative_tweets[:100000]

    # Получение всех токенов в твитах
    positive_tweet_tokens = map(nltk.word_tokenize, positive_tweets)
    negative_tweet_tokens = map(nltk.word_tokenize, negative_tweets)

    # Получение 'чистых' токенов
    clean_positive_tweet_tokens = map(lemmatize_sentence, positive_tweet_tokens)
    clean_negative_tweet_tokens = map(lemmatize_sentence, negative_tweet_tokens)

    # Получение данных
    positive_tokens_for_model = get_tweets_for_model(
        clean_positive_tweet_tokens)
    negative_tokens_for_model = get_tweets_for_model(
        clean_negative_tweet_tokens)

    positive_dataset = ((tweet_dict, 'Positive')
                        for tweet_dict in positive_tokens_for_model)
    negative_dataset = ((tweet_dict, 'Negative')
                        for tweet_dict in negative_tokens_for_model)
    dataset = list(chain(positive_dataset, negative_dataset))
    shuffle(dataset)
    train_data = dataset[:70000]
    test_data = dataset[70000:]

    classifier = NaiveBayesClassifier.train(train_data)

    save_classifier(classifier)
    print('Accuracy is:', classify.accuracy(classifier, test_data))


def get_phrases_tonality():
    """
    Определение тональности предложений
    """
    saved_classifier = load_classifier()

    database = Database()
    phrases = database.getAllPhrases()
    for phrase in phrases:
        tokens = lemmatize_sentence(nltk.word_tokenize(phrase['sentence']))
        phrase['tonality'] = saved_classifier.classify(
            dict([token, True] for token in tokens))
        database.update_phrase(phrase)

    return phrases


def main():
    result = get_phrases_tonality()
    print(result)


if __name__ == '__main__':
    main()
