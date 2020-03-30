from bs4 import BeautifulSoup
from database import Database
import requests

class Parser:
    siteUrl = 'https://bloknot-volgograd.ru'
    nextPage = ''

    def doParsing(self):
        database = Database()

        for number in range(1):

            # главная или нет
            if self.nextPage == '':
                newsListUrl = self.siteUrl
            else:
                newsListUrl = self.siteUrl + self.nextPage

            newsListUrl = requests.get(newsListUrl)

            # страница
            soupNewsList = BeautifulSoup(newsListUrl.text, "html.parser")

            # получить адрес следующей страницы пагинации
            nextPage = soupNewsList.find(id='navigation_1_next_page').get('href')

            # собрать новости на текущей странице
            newsListArr = soupNewsList.find('ul', class_='bigline').findAll('a', class_='sys')

            # обработать данные о каждой новости
            for i in range(len(newsListArr)):
                # ссылка на новость
                currentNewsShortUrl = newsListArr[i].get('href')
                currentNewsFullUrl = self.siteUrl + newsListArr[i].get('href')
                #currentNewsFullUrl = 'https://bloknot-volgograd.ru/news/nazvana-srednyaya-zarabotnaya-plata-v-malykh-i-sre-1206800'

                # поля новости
                newsData = requests.get(currentNewsFullUrl)
                soupNews = BeautifulSoup(newsData.text, "html.parser")

                # поля новости
                name = soupNews.find('h1').text
                data = ''
                href = currentNewsFullUrl

                textArr = soupNews.find('div', class_='news-text').findAll('p')
                text = ''
                for pTag in range(len(textArr)):
                    text += textArr[pTag].text

                count_comments = int(soupNewsList.find('a', href=currentNewsShortUrl + '#comments').text)

                # запись в БД
                database.addRecord( {
                    "name" : name,
                    "data" : data,
                    "href" : href,
                    "text" : text,
                    "count_comments" : count_comments
                })


parser = Parser()
parser.doParsing()