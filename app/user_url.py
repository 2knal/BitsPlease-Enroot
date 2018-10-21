import json
import newspaper
from newspaper import Article
import os.path
from Fake_News_Detection import prediction
import views

# url = 'https://www.ndtv.com/business/petrol-price-on-october-20-petrol-diesel-prices-cut-for-third-straight-day-check-fuel-rates-here-1934766?News_Trending'
with open('url.txt', 'r') as fp:
    url = fp.read()
# url = views.inp_value
print(url)
news = Article(url)
try:
    news.download()
    news.parse()
    news.nlp()
except Exception as e:
    news.download()
    print(e)
    print("continuing...")

data = dict()
data['title'] = news.title
data['text'] = news.text
data['link'] = news.url
data['image'] = news.top_image
data['summary'] = news.summary

verdict, prob = prediction.detecting_fake_news(news.text)
if verdict == True:
    verdict = 'True'
else:
    verdict = 'False'
data['verdict'] = verdict
data['probability'] = prob

print(data)
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
with open(PROJECT_ROOT+'/scraping/data/return.json', 'w') as fp:
    json.dump(data, fp, indent = 4, sort_keys = True)
