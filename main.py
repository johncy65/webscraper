import requests
from bs4 import BeautifulSoup
import datetime

def datetime_converter(string_datetime):
    string_datetime = string_datetime.split(",")
    if len(string_datetime) <= 1:
        return datetime.date.today()
    return datetime.datetime.strptime("".join(string_datetime[0:2]),'%b %d %Y').date()

def get_article_heading(article_head):
    article_heading = article_head.contents[-1]
    span_heading = article_head.select('span.langspan')
    if len(span_heading) > 0:
        return span_heading[0].get_text()
    return article_heading.strip()

page_size = 100
page = 1
#get current week's starting date
week_start_date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
while_condition = True

file = open("articles.txt","a")
file.write("date,heading,excerpt,image\n")

while while_condition:
    params = {'page':str(page),'pagesize':str(page_size)}
    response = requests.get('https://www.prnewswire.com/news-releases/news-releases-list/',params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.select('.row .arabiclistingcards')
    print("page",page,"articles",len(articles))
    for article in articles:
        article_head = article.select('h3')[0]
        article_published_datetime = datetime_converter(article_head.select('small')[0].get_text())
        article_heading = get_article_heading(article_head)
        article_image = article.select('img')[0].get("src") if len(article.select('img')) > 0 else None;
        article_excerpt = article.select('p.remove-outline')[0].get_text()

        if article_published_datetime < week_start_date:
            while_condition = False
            break

        file.write(",".join([str(article_published_datetime),article_heading,article_excerpt,str(article_image)]) + "\n")
        file.flush()
    page+=1 

file.close()