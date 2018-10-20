import feedparser as fp
import json
import newspaper
from newspaper import Article
from time import mktime
from datetime import datetime
import os.path

# http://www.sahalnews.com/wp-content/uploads/2014/12/news-update-.jpg

# Set the limit for number of articles to download
LIMIT = 4

data = {}
data['articles'] = []

# Loads the JSON files with news sites
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
print(PROJECT_ROOT)
with open(PROJECT_ROOT +'/NewsPapers.json', 'r') as data_file:
    companies = json.load(data_file)

# companies = {
#     	"dna": {
#     		"link": "https://www.dnaindia.com/mumbai"
#     	},
#     	"thehindu": {
#     		"link": "https://www.thehindu.com/news/cities/mumbai/"
#     	},
#         "ndtv": {
#         "link": "https://www.ndtv.com/mumbai-news"
#     	},
#         "hindustantimes": {
#     	"link": "https://www.hindustantimes.com/mumbai-news/"
#     	}
# }
count = 1

# Iterate through each news company
for company, value in companies.items():
    # If a RSS link is provided in the JSON file, this will be the first choice.
    # Reason for this is that, RSS feeds often give more consistent and correct data.
    # If you do not want to scrape from the RSS-feed, just leave the RSS attr empty in the JSON file.
    if 'rss' in value:
        d = fp.parse(value['rss'])
        print("Downloading articles from ", company)
        newsPaper = {
            "rss": value['rss'],
            "link": value['link'],
            "articles": []
        }
        for entry in d.entries:
            # Check if publish date is provided, if no the article is skipped.
            # This is done to keep consistency in the data and to keep the script from crashing.
            if hasattr(entry, 'published'):
                if count > LIMIT:
                    break
                article = {}
                article['link'] = entry.link
                date = entry.published_parsed
                article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                try:
                    content = Article(entry.link)
                    content.download()
                    content.parse()
                except Exception as e:
                    # If the download for some reason fails (ex. 404) the script will continue downloading
                    # the next article.
                    print(e)
                    print("continuing...")
                    continue
                article['title'] = content.title
                article['text'] = content.text
                newsPaper['articles'].append(article)
                print(count, "articles downloaded from", company, ", url: ", entry.link)
                count = count + 1
    else:
        # This is the fallback method if a RSS-feed link is not provided.
        # It uses the python newspaper library to extract articles
        print("Building site for ", company)
        paper = newspaper.build(value['link'], memoize_articles=False)
        # newsPaper = {
        #     # "link": value['link'],
        #     "articles": []
        # }
        noneTypeCount = 0
        for content in paper.articles:
            if count > LIMIT:
                break
            try:
                content.download()
                content.parse()
                content.nlp()
            except Exception as e:
                print(e)
                print("continuing...")
                continue
            # Again, for consistency, if there is no found publish date the article will be skipped.
            # After 10 downloaded articles from the same newspaper without publish date, the company will be skipped.
            # if content.publish_date is None:
            #     print(count, " Article has date of type None...")
            #     noneTypeCount = noneTypeCount + 1
            #     if noneTypeCount > 10:
            #         print("Too many noneType dates, aborting...")
            #         noneTypeCount = 0
            #         break
            #     count = count + 1
            #     continue
            article = {}
            article['title'] = content.title
            article['text'] = content.text
            article['link'] = content.url
            article['image'] = content.top_image
            article['summary'] = content.summary
            # article['published'] = content.publish_date.isoformat()

            print(count, "articles downloaded from", company, " using newspaper, url: ", content.url)
            count = count + 1
            noneTypeCount = 0
            # print(article)
    data['articles'].append(article)
    if count == 1:
        del data['articles'][0]
    count = 1

# Finally it saves the articles as a JSON-file.
try:
    with open(PROJECT_ROOT+'/data/scraped_articles.json', 'w') as outfile:
        json.dump(data, outfile, indent = 4, sort_keys = True)
except Exception as e: print(e)
