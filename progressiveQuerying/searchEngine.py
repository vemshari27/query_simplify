    # Copyright © 2021 Eric John, Srihari Vemuru. All rights reserved
    
    # This file is part of PTGQ.

    # PTGQ is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # PTGQ is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with PTGQ.  If not, see <https://www.gnu.org/licenses/>.

import requests
import json


def search(q):
    appId = ""
    q = q.strip('\n').strip(' ').split(' ')
    query = ""
    for w in q:
        query = query+w+"%20"
    query = query[:-3]

    URL = "http://api.wolframalpha.com/v2/query?appid=" + appId + "&input=" + \
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
