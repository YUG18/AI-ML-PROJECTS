import requests
from bs4 import BeautifulSoup
import schedule
import pandas as pd
import datetime
import time

def fetch_news_from_bbc():
    url = "https://www.bbc.com/innovation"
    headers = {'User-Agent':'Mozilla/5.0'}
    response = requests.get(url,headers)
    soup = BeautifulSoup(response.text,'html.parser')
    articles = soup.find_all("div", attrs={'data-testid': 'anchor-inner-wrapper'})
    news = []
    for article in articles:
        link_tag = article.find("a")
        if link_tag:
            title = link_tag.get_text(strip = True)
            link = link_tag['href']
            full_link = "https://www.bbc.com" + link
            print(title,full_link)
            news.append({"title":title,"link":full_link})
    return news

def save_to_csv(news,filename="news.csv"):
    df = pd.DataFrame(news)
    df['date'] = datetime.datetime.now().strftime('%Y:%m:%d')
    df.to_csv(filename,index=False)

def job():
    news = fetch_news_from_bbc()
    save_to_csv(news)

if __name__ == "__main__":
    job()
    print("News Updated")
    schedule.every().day.at('09:00').do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

