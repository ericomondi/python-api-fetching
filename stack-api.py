import requests
import json

response = requests.get(
    "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow"
)

for quiz in response.json()['items']:
    if quiz['answer_count']==0:
        print(quiz['title'])
        print(quiz['link'])
        print()
    else:
        print(quiz['title'])
        print('Answered..........')     
        print()
    
    

