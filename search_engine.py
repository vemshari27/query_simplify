
# # def search(query):
# #     if 'who' == query[:3]:
# #         return 'Hillary'
# #     elif 'the' == query[:3]:
# #         return 'Trump'
# #     elif 'when' == query[:4]:
# #         return '1999'


# # importing the requests library 
# import requests 
  
# # api-endpoint 
# URL = "http://api.wolframalpha.com/v2/query?appid=RX4H49-LR986EXTXL&input=when%20was%20of%20Mahatma%20gandhi%20born&includepodid=Result&format=plaintext&output=json"
  
# # location given here 
# # location = "delhi technological university"
  
# # defining a params dict for the parameters to be sent to the API 
# # PARAMS = {'address':location} 
  
# # sending get request and saving the response as response object 
# r = requests.get(url = URL) 
  
# # extracting data in json format 
# data = r.json() 

  
# # extracting latitude, longitude and formatted address  
# # of the first matching location 
# # latitude = data['results'][0]['geometry']['location']['lat'] 
# # longitude = data['results'][0]['geometry']['location']['lng'] 
# # formatted_address = data['results'][0]['formatted_address'] 
  
# # # printing the output 
# # print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
# #       %(latitude, longitude,formatted_address)) 
# print(data)

import requests
import json

def search(q):
    q = q.strip('\n').strip(' ').split(' ')
    query = ""
    for w in q:
        query = query+w+"%20"
    query = query[:-3]

    URL = "http://api.wolframalpha.com/v2/query?appid=RX4H49-LR986EXTXL&input="+query+"&includepodid=Result&format=plaintext&output=json"
    r = requests.get(url = URL)
    data = r.json()
    
    data = data['queryresult']
    if data['success']:
        if data['numpods'] == 1:
            data = data['pods'][0]
        else:
            for i in data['pods']:
                if 'primary' in i.keys():
                    if i['primary']:
                        data = i

    if data['numsubpods'] == 1:
            data = data['subpods'][0]['plaintext']
    else:
        for i in data['subpods']:
            if 'primary' in i.keys():
                if i['primary']:
                    data = i['plaintext']

    data = data.split('(')[0].strip(' ')
    data = data.split('|')[0].strip(' ')
    return data

if __name__ == "__main__":
    query = input()
    result = search(query)
    print(result)
