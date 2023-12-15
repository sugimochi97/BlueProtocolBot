from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import datetime

def get_news_texts(news_texts = [], title_texts = [], urls = [], page=1):
    """ブルプロの当日更新ニュースを通知します。
    引数:
        - news_texts = []
        - title_texts = []
        - urls = []
    戻り値: 
        - news_text  (list[str]) : 取得HTMLのテキスト部分抽出データ 
        - title_text (list[str]) : ニュースのタイトルテキスト
        - urls       (list[str]) : ニュースのURLです
    """

    # webdriver起動
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # ニュースのトップページを取得し、日付データを取得
    driver.get(f"https://blue-protocol.com/news/?category=all&page={page}")
    time.sleep(1.5)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    news_list_soup = soup.find("div", attrs={"class": "news-list"})

    date_soups = news_list_soup.find_all("p", attrs={"class":"news-list__date"})
    dates = ["-".join(i.text.split(".")) for i in date_soups]

    # 今日の日付
    now = datetime.datetime.now().date()
    
    # ニュースの要素を取得
    items = news_list_soup.find_all("li", attrs={"class":"news-list__item"})
    now = "2023-12-13"
    tbody_indexes = []
    for i, date in enumerate(dates):

        # ニュース日付と今日の日付が一致するものを処理
        if now == date:
            # URLの作成
            link = items[i].a.get("href")
            url = "https://blue-protocol.com"+link

            # アクセスしてソースを取得
            driver.get(url)
            time.sleep(1.5)
            news_page = driver.page_source
            tbody_indexes.append(i)

            # 抽出処理
            soup = BeautifulSoup(news_page, 'html.parser')
            news_texts.append(soup.find("section", attrs={"class":"details"}).text)

            title_texts.append(soup.find("h3", attrs={"class":"details__head__headline"}).text)
            urls.append(url)

    driver.quit()

    # 処理回数が最大の場合、次のページも探索する（再起処理）
    if len(tbody_indexes) == 10:
        news_texts, title_texts, urls = get_news_texts(news_texts, title_texts, urls, page+1)

    return news_texts, title_texts, urls