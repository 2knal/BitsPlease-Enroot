# -*- coding: utf-8 -*-
import pickle, os, json
import pyphi
#function to run for prediction
def detecting_fake_news(var):
#retrieving the best model for prediction
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    load_model = pickle.load(open(PROJECT_ROOT+'/final_model.sav', 'rb'))
    prediction = load_model.predict([var])
    prob = load_model.predict_proba([var])

    print("The given statement is ",prediction[0])
    print("The truth probability score is ",prob[0][1])
    return prediction[0], prob[0][1]
# var = input("Please enter the news text you want to verify: ")
# print("You entered: " + str(var))

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = PROJECT_ROOT[0: -19]
something = dict()
with open(PROJECT_ROOT + 'scraping/data/scraped_articles.json', 'r') as file:
    data = json.load(file)
    print(data)
    for article in data['articles']:
        verdict, prob = detecting_fake_news(article['text'])
        if verdict == True:
            verdict = 'True'
        else:
            verdict = 'False'
        article['verdict'] = verdict
        article['probability'] = prob
        print(verdict, str(prob))
    print(data)
    something = data
    print(type(something))
    print(something)
# with open(PROJECT_ROOT + 'app/scraping/data/scraped_articles.json', 'w') as file:
#     json.dump(data, file, indent = 4, sort_keys = True)
with open(PROJECT_ROOT+'scraping/data/scraped_articles.json', 'w') as fp:
    json.dump(something, fp, indent = 4, sort_keys = True)
    print('Fuck Yeah!')
