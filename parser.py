from bs4 import BeautifulSoup
from database import Database
from datetime import datetime, timedelta
import requests

class Parser:
    siteUrl = 'https://bloknot-volgograd.ru'
    nextPage = ''

    def doParsing(self):
        database = Database()

        # узнать общее кол-во страниц пагинации
        first = requests.get(self.siteUrl)
        soupFirst = BeautifulSoup(first.text, "html.parser")
        lastPageNumber = int(soupFirst.find('div', class_='navigation-pages').findAll('a')[-1].text) # для for page in range(1):

        for page in range(lastPageNumber):
            print(page + 1)
            # главная или нет
            if self.nextPage == '':
                newsListUrl = self.siteUrl
            else:
                newsListUrl = self.siteUrl + self.nextPage

            newsListUrl = requests.get(newsListUrl)

            # страница
            soupNewsList = BeautifulSoup(newsListUrl.text, "html.parser")

            # получить адрес следующей страницы пагинации
            self.nextPage = soupNewsList.find(id='navigation_1_next_page').get('href')

            # собрать новости на текущей странице
            newsListArr = soupNewsList.find('ul', class_='bigline').findAll('a', class_='sys') # для for i in range

            # обработать данные о каждой новости
            for i in range(len(newsListArr)):
                # ссылка на новость
                currentNewsShortUrl = newsListArr[i].get('href')
                currentNewsFullUrl = self.siteUrl + newsListArr[i].get('href')

                # поля новости
                newsData = requests.get(currentNewsFullUrl)
                soupNews = BeautifulSoup(newsData.text, "html.parser")

                # почистить от js
                for script in soupNews(["script", "style"]):
                    script.decompose()

                # поля новости
                name = soupNews.find('h1').text
                date = soupNewsList.find('a', href=currentNewsShortUrl + '#comments').find_parent('span').next_element.next_element
                # обработаем дату
                date = str(self.converteDate(date))

                href = currentNewsFullUrl
                text = soupNews.find('div', class_='news-text').text
                count_comments = int(soupNewsList.find('a', href=currentNewsShortUrl + '#comments').text)

                # запись в БД
                database.addNews({
                    "name" : name,
                    "date" : date,
                    "href" : href,
                    "text" : text,
                    "count_comments" : count_comments
                })

    def converteDate(self, date):
        if "сегодня" in date:
            newDate = datetime.now().date()
        elif "вчера" in date:
            newDate = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        else:
            date = ''.join(date.split())
            newDate = datetime.strptime(date, '%d.%m.%Y')
            newDate = datetime.strftime(newDate, '%Y-%m-%d')

        return newDate

parser = Parser()
parser.doParsing()