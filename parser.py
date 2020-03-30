from bs4 import BeautifulSoup
from database import Database
import requests

class Parser:
    siteUrl = 'https://bloknot-volgograd.ru'
    nextPage = ''

    def doParsing(self):
        database = Database()

        # узнать общее кол-во страниц пагинации
        first = requests.get(self.siteUrl)
        soupFirst = BeautifulSoup(first.text, "html.parser")
        lastPageNumber = int(soupFirst.find('div', class_='navigation-pages').findAll('a')[-1].text)

        for page in range(1):
            #print(page + 1)
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
            newsListArr = soupNewsList.find('ul', class_='bigline').findAll('a', class_='sys')

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
                date = self.converteDate(date)

                href = currentNewsFullUrl
                text = soupNews.find('div', class_='news-text').text
                count_comments = int(soupNewsList.find('a', href=currentNewsShortUrl + '#comments').text)
                print(name)
                # запись в БД
                database.addRecord({
                    "name" : name,
                    #"date" : date,
                    "href" : href,
                    "text" : text,
                    "count_comments" : count_comments
                })

    def converteDate(self, date):
        newDate = date
        #TODO чекать: менять сегодня, вчера
        return newDate

parser = Parser()
parser.doParsing()