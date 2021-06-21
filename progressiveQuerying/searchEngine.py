import requests
import json


def search(q):
    q = q.strip('\n').strip(' ').split(' ')
    query = ""
    for w in q:
        query = query+w+"%20"
    query = query[:-3]

    URL = "http://api.wolframalpha.com/v2/query?appid=RX4H49-LR986EXTXL&input=" + \
        query+"&includepodid=Result&format=plaintext&output=json"
    r = requests.get(url=URL)
    data = r.json()

    data = data['queryresult']
    try:
        if data['success']:
            try:
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
            except:
                return "Not Found"
        else:
            return "Not Found"

        data = data.split('(')[0].strip(' ')
        data = data.split('|')[0].strip(' ')
        return data
    except:
        return "Not Found"


if __name__ == "__main__":
    query = input()
    result = search(query)
    print(result)
