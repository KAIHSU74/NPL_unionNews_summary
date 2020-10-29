from numpy.lib.shape_base import tile
import requests
from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent
import time
from random import randint
import AutoSummary as ausu
import get_newUrl

# 摘要處理
def summary(text_news):
    sentences, indexs = ausu.split_sentence(text_news)          # 按標點分割句子
    tfidf = ausu.get_tfidf_matrix(sentences, stops)             # 移除停用詞並轉換為矩陣
    word_weight = ausu.get_sentence_with_words_weight(tfidf)    # 計算句子關鍵詞權重
    posi_weight = ausu.get_sentence_with_position_weight(sentences)     # 計算位置權重
    scores = ausu.get_similarity_weight(tfidf)                  # 計算相似度權重
    sort_weight = ausu.ranking_base_on_weigth(word_weight, posi_weight, scores, feature_weight=[1,1,1])
    summar = ausu.get_summarization(indexs ,sort_weight, topK_ratio=0.5) # 取得摘要比例
    print(summar)

# 偽裝瀏覽器
ua = UserAgent()
headers = {'User-Agent': ua.random}
# 停用詞
stops = []
with open('stopWord_summar.txt', 'r', encoding='utf-8-sig') as f:
    for line in f.readlines():
        stops.append(line.strip())

urls = []

# 1頁 20則新聞
for p in range(1,2):
    # 取得聯合報即時新聞每筆連結
    url = 'https://udn.com/api/more?page='+str(p)+'&id=&channelId=1&cate_id=0&type=breaknews&totalRecNo=10351'
    html = requests.get(url, headers=headers).json()
    for i in range(len(html['lists'])):
        url = html['lists'][i]['titleLink']
        urls.append("https://udn.com"+url)
        title = html['lists'][i]['title']

# 取得新聞內容
errUrl = []
i = 1
j = 0
for url in urls:
    html = requests.get(url, headers=headers)
    objsoup = soup(html.text, 'lxml')
    try:
        findp = objsoup.find("article",class_="article") or \
                objsoup.find("article",class_="article-content") or \
                objsoup.find("div", id="container") or \
                objsoup.find("div",class_="container") or \
                objsoup.find("div",class_="articleMain")
        text_news = ''
        if findp: 
            allptag = findp.find_all("p")
            print('處理 {0} 新聞內容'.format(url))
            for p in allptag:
                t = p.text.rstrip()
                t = t.replace('\n\r','').replace('\n','').replace('\r','')
                if t != '':
                    text_news += t
        print('第 %d 則新聞' % i)
        # 新聞摘要        
        summary(text_news)
        print('='*120)
        i += 1
        time.sleep(randint(0,2))
    except Exception as e:
        text_news = ''
        errUrl.append(url)
        text_news += get_newUrl.re_url(url)
        if text_news == '會員專屬':
            print(text_news)
            i += 1
            print('='*120)
            next
        else:
            # 新聞摘要
            summary(text_news)
            print("="*120)
            i += 1
            next
for eu in errUrl:
    print(eu)
      
