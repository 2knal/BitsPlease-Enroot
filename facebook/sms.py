# -*- coding: UTF-8 -*-

from fbchat import log, Client
import json
from fbchat import Client
from fbchat.models import *

# Subclass fbchat.Client and override required methods
class EchoBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
        with open('scraped_articles.json',"r") as file:
              data = json.load(file)

        tomato1=Message(text='!news')
        tomato2=Message(text='!help')
        tomato3=Message(text='Send !news for the latest news!')
        tomato4=Message(text='Send !help for more info')
        if author_id != self.uid:
            if message_object.text==tomato2.text:
                    
                self.send(tomato3, thread_id=thread_id, thread_type=thread_type)
            
            elif message_object.text==tomato1.text:
                for i in data['articles']:
                    tomato=Message(text=i['title']) 
                    self.send(tomato, thread_id=thread_id, thread_type=thread_type)
                    self.sendRemoteFiles(i['image'], message=None, thread_id=thread_id, thread_type=thread_type)

            elif message_object.text==Message(text = '1').text:
                self.send(Message(text = data['articles'][0]['summary']), thread_id=thread_id, thread_type=thread_type)
                self.send(Message(text = data['articles'][0]['link']), thread_id=thread_id, thread_type=thread_type) 

            elif message_object.text==Message(text = '2').text:
                self.send(Message(text = data['articles'][1]['summary']), thread_id=thread_id, thread_type=thread_type)
                self.send(Message(text =data['articles'][1]['link']), thread_id=thread_id, thread_type=thread_type) 
               
            elif message_object.text==Message(text = '3').text:
                self.send(Message(text = data['articles'][2]['summary']), thread_id=thread_id, thread_type=thread_type)
                self.send(Message(text =data['articles'][2]['link']), thread_id=thread_id, thread_type=thread_type) 
               
            elif message_object.text==Message(text = '4').text:
                self.send(Message(text = data['articles'][3]['summary']), thread_id=thread_id, thread_type=thread_type)
                self.send(Message(text =data['articles'][3]['link']), thread_id=thread_id, thread_type=thread_type) 
            
            else:
                self.send(tomato4, thread_id=thread_id, thread_type=thread_type)
            while(True):
                self.send(Message(text='Want to learn more?'), thread_id=thread_id, thread_type=thread_type)
                self.send(Message(text ='Type 1,2,3 or 4 to know more about respective topics'), thread_id=thread_id, thread_type=thread_type)
                break
            
                
               
               
t=True                
client = EchoBot("anay.kulkarni@somaiya.edu", "redbull")
client.listen()
