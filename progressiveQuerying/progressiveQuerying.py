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

import os
from queryTreeConstruction.queryTree import QueryNode, QueryTree
from .searchEngine import search


def progressive_searcher(querytree, result_dic):
    if querytree is None:
        return ""

    wh_words = {'what': '', 'where': 'in',
                'when': 'in', 'who': 'of', 'whom': ''}

    # prepositions = [i.strip('\n').strip(' ') for i in open('prepositions.txt').readlines()]

    final_result = ""
    left_ans, right_ans = "", ""
    left_ans = progressive_searcher(querytree.left_child, result_dic)
    right_ans = progressive_searcher(querytree.right_child, result_dic)

    querynode = querytree.node

    search_query = querynode.get_left_text() + " " + left_ans + " " + \
        querynode.get_middle_text() + " " + right_ans + " " + querynode.get_right_text()

    search_query = " ".join(search_query.split())

    # print(search_query)
    result = search(search_query)
    # result = "Not Found"
    # If answer wasn't found give the query back
    if(result == "Not Found"):
        return search_query

    # print(search_query)
    print(result)

    result = result.rstrip('\n')
    final_result = result

    # Adding prefix to result
    prefix = ''
    if querynode.get_first_word() in wh_words.keys():
        prefix = wh_words[querynode.get_first_word()]

    final_result = prefix + " " + result

    result_dic[search_query] = result
    return final_result


if __name__ == "__main__":
    # query = input("Enter query: ")
    query_tree = ['who is', 'the wife of',
                  'the president of usa', 'when gandhi was born']
    result = progressive_searcher(query_tree)
    print(result)
