from bs4 import BeautifulSoup
from database import Database
import requests

# class News(object):
#     def __init__(self, name):
#         self.name = name

siteUrl = 'https://bloknot-volgograd.ru'
nextPage = ''

for number in range(1):

    # главная или нет
    if nextPage == '':
        newsListUrl = 'https://bloknot-volgograd.ru/'
    else:
        newsListUrl = 'https://bloknot-volgograd.ru' + nextPage

    newsListUrl = requests.get(newsListUrl)

    # страница
    soup = BeautifulSoup(newsListUrl.text, "html.parser")

    # получить адрес следующей страницы пагинации
    nextPage = soup.find(id='navigation_1_next_page').get('href')

    # собрать новости на текущей странице
    newsList = soup.find('ul', class_='bigline').findAll('a', class_='sys')

    # обработать данные о каждой новости
    for i in range(len(newsList)):
        # ссылка на новость
        currentNewsUrl = siteUrl + newsList[i].get('href')

        # поля новости
        newsData = requests.get(currentNewsUrl)
        soupNews = BeautifulSoup(newsData.text, "html.parser")
        name = soupNews.find('h1').text
        print(name)

        # newsObject = News(name)
        # print(newsObject)

database = Database()
database.addRecord( {"footg" : "bagggr" })