from django.shortcuts import render
from django.http import HttpResponse
import os, subprocess, json

articles = []
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
with open(PROJECT_ROOT + '/scraping/data/scraped_articles.json') as fp:
    data = json.load(fp)
    articles = data['articles']

inp_value = ''
def home(request):
    output = script(request)
    ml = train(request)
    try:
        inp_value = request.GET['news']
        if inp_value != '':
            with open('url.txt', 'w') as file:
                file.write(str(inp_value))
    except:
        print('something')
    userthingy = test(request)
    blaze = dict()
    with open(PROJECT_ROOT + '/scraping/data/return.json') as f:
        blaze = json.load(f)
        print(blaze)
    context = {
        'articles': articles,
        'url': blaze
    }
    print('Enter the url, mannn')
    print(context)
    # print(type(request.GET['news']))
    # print(inp_value)
    # print(something)



    return render(request, 'app/home.html', context)

def script(request):
    if request.method == 'GET':
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        print(PROJECT_ROOT)
        return subprocess.run(['python', PROJECT_ROOT+'/scraping/NewsScraper.py'])
def train(request):
    if request.method == 'GET':
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        print('00'+PROJECT_ROOT)
        PROJECT_ROOT = PROJECT_ROOT[0: -4]
        print('01'+PROJECT_ROOT)
        return subprocess.run(['python', PROJECT_ROOT+'/Fake_News_Detection/prediction.py'])
def test(request):
    if request.method == 'GET':
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        return subprocess.run(['python', PROJECT_ROOT+'/user_url.py'])
