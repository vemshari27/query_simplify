import os
import search_engine
from query_tree import Query, QueryTree, print_qt

def progressive_searcher(qt, result_dic):
    if qt is None:
        return "",""
    wh_words = {'what':'', 'where':'in', 'when':'in', 'who':'of', 'whom':''}
    # prepositions = [i.strip('\n').strip(' ') for i in open('prepositions.txt').readlines()]

    # prev_res = ""
    final_result = ""
    left_ans, right_ans = "", ""
    extra = ""
    left_ans,_ = progressive_searcher(qt.left_child, result_dic)
    right_ans, extra = progressive_searcher(qt.right_child, result_dic)

    # for sub_query in qt[::-1]:
    # with node as qt.node:
    node = qt.node
    sub_query = node.text
    words = sub_query.lstrip(' ').rstrip(' ').split(' ')

    if len(left_ans)==0 and ((len(words) == 1 and node.type_ != 2 and node.type_ != 3) or words[0] in ['was', 'were', 'is', 'are', 'will', 'would', 'did', 'do']):
        print('ss', sub_query+' '+right_ans+' '+extra)
        return "",sub_query+' '+right_ans+' '+extra
    if len(extra) != 0 and words[0] in wh_words.keys() and (len(words) ==1 or words[1] in ['was', 'were', 'is', 'are', 'will', 'would', 'did', 'do']):
        return right_ans, extra
    
    to_search = left_ans+sub_query+' ' +right_ans
    if node.type_ == 2 or node.type_ == 3:
        to_search = to_search+' '+extra
        extra = ""
    print(to_search)
    result = search_engine.search(to_search)
    print(result)
    final_result = result
        
    prefix = ''#words[0]
    if words[0] in wh_words.keys():
        prefix = wh_words[words[0]]
    final_result = prefix + ' ' +result

    result_dic[to_search] = result

    return final_result, extra

if __name__ == "__main__":
    # query = input("Enter query: ")
    query_tree = ['who is', 'the wife of', 'the president of usa', 'when gandhi was born']
    result = progressive_searcher(query_tree)
    print(result)
