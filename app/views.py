from django.shortcuts import render
from django.http import HttpResponse
import os, subprocess

def home(request):
    output = script(request)
    ml = train(request)
    return render(request, 'app/home.html')

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
