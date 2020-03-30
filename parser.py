from bs4 import BeautifulSoup
from database import Database
import requests

class Parser:
    siteUrl = 'https://bloknot-volgograd.ru'
    nextPage = ''

    def doParsing(self):
        for number in range(2):

            # главная или нет
            if self.nextPage == '':
                newsListUrl = 'https://bloknot-volgograd.ru/'
            else:
                newsListUrl = 'https://bloknot-volgograd.ru' + self.nextPage

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
                currentNewsUrl = self.siteUrl + newsList[i].get('href')

                # поля новости
                newsData = requests.get(currentNewsUrl)
                soupNews = BeautifulSoup(newsData.text, "html.parser")
                name = soupNews.find('h1').text
                print(name)

                # newsObject = News(name)
                # print(newsObject)

parser = Parser()
parser.doParsing()

# database = Database()
# database.addRecord( {"footg" : "bagggr" })