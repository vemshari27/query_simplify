import os
import search_engine
from query_tree import Query, QueryTree, print_qt

def progressive_searcher(qt):
    if qt is None:
        return ""
    wh_words = {'what':'', 'where':'in', 'when':'in', 'who':'of', 'whom':''}
    # prepositions = [i.strip('\n').strip(' ') for i in open('prepositions.txt').readlines()]

    # prev_res = ""
    final_result = ""
    left_ans, right_ans = "", ""
    left_ans = progressive_searcher(qt.left_child)
    right_ans = progressive_searcher(qt.right_child)

    # for sub_query in qt[::-1]:
    # with node as qt.node:
    node = qt.node
    sub_query = node.text
    words = sub_query.lstrip(' ').rstrip(' ').split(' ')

    if words[0] in wh_words.keys() and words[1] in ['was', 'were', 'is', 'are', 'will', 'would', 'did', 'do']:
        return right_ans
        # check = True
        # if words[0] in prepositions:
        #     tmp = len(words[0])+1
        #     sub_query = sub_query[tmp:]
        #     check = False

    # if words[0] == "'s":
    #     print(left_ans+sub_query)
    #     result = search_engine.search(left_ans+sub_query)
    # else:
    #     print(sub_query+' '+right_ans)
    #     result = search_engine.search(sub_query+' ' +right_ans)
    # print(result)
    print(left_ans+sub_query+' ' +right_ans)
    result = search_engine.search(left_ans+sub_query+' ' +right_ans)
    print(result)
    final_result = result
        
    prefix = ''#words[0]
    if words[0] in wh_words.keys():
        prefix = wh_words[words[0]]
    final_result = prefix + ' ' +result

    return final_result

if __name__ == "__main__":
    # query = input("Enter query: ")
    query_tree = ['who is', 'the wife of', 'the president of usa', 'when gandhi was born']
    result = progressive_searcher(query_tree)
    print(result)

    

        