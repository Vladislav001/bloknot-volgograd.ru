import csv
import codecs
import nltk
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from operator import itemgetter
from pymystem3 import Mystem

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
    # число всех позитивных твиттов
    # count_pos_tweets = len(positive_tweets)

    # находим 80% от всех позитивных твиттов для обучения
    # count_pos_training_tweets = count_pos_tweets * 0.8
    with codecs.open(
            'tonality-analysis/tweets/negative.csv', 'r', 'utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        neg_tweets = tuple(map(itemgetter(3), reader))

    # count_neg_training_tweets = (len(tweets) - count_pos_tweets) * 0.8

    return pos_tweets, neg_tweets


def lemmatize_sentence(tokens):
    """
    Получение 'чистых' токенов твита
    :param tokens: токены одного твита
    :return: список 'чистых' токенов
    """
    mystem = Mystem()
    lemmatized_sentence = []
    cleaned_tokens = []
    for word, tag in pos_tag(tokens, lang='rus'):
        lemmatized_sentence.append(mystem.lemmatize(word))
        if word.lower() not in STOP_WORDS:
            cleaned_tokens.append(word.lower())

    return cleaned_tokens


# Получение твитов из файлов
positive_tweets, negative_tweets = read_tweets()
tweets = []
tweets.extend(positive_tweets)
tweets.extend(negative_tweets)
# fixme пока для быстроты выполнения
tweets = tweets[:5]
positive_tweets = positive_tweets[:5]
negative_tweets = negative_tweets[:5]

# Получение всех токенов в твитах
tweet_tokens = tuple(map(nltk.word_tokenize, tweets))
positive_tweet_tokens = tuple(map(nltk.word_tokenize, positive_tweets))
negative_tweet_tokens = tuple(map(nltk.word_tokenize, negative_tweets))

# Получение 'чистых' токенов
clean_tweet_tokens = tuple(map(lemmatize_sentence, tweet_tokens))
clean_positive_tweet_tokens = tuple(
    map(lemmatize_sentence, positive_tweet_tokens))
clean_negative_tweet_tokens = tuple(
    map(lemmatize_sentence, negative_tweet_tokens))
