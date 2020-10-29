import requests, bs4
import re
from fake_useragent import UserAgent

def re_url(url):
    ua = UserAgent()
    headers = {'User-Agent' : ua.random}
    r = requests.get(url)
    objsoup = bs4.BeautifulSoup(r.text, 'lxml')
    # 取得新網址
    real_url = re.search('window.location.href="(.*)"', objsoup.text).group().split('"',2)[1]
    new_r = requests.get(real_url, headers=headers)
    new_Soup = bs4.BeautifulSoup(new_r.text, 'lxml')
    p_texts = ''
    try:
        member = new_Soup.find('div' ,id="member_only") or \
            new_Soup.find('div', class_="paywall-content__member")
        if member:
            return "會員專屬"
        else:
            findp = new_Soup.find_all('p')
            for p in findp:
                p_texts += p.text
            return p_texts
    except Exception as e:
        return e
