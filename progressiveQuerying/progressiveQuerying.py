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
