import os
import search_engine

def progressive_searcher(qt):
    wh_words = {'what':'', 'where':'in', 'when':'in', 'who':'of', 'whom':''}
    # prepositions = [i.strip('\n').strip(' ') for i in open('prepositions.txt').readlines()]

    prev_res = ""
    final_result = ""
    for sub_query in qt[::-1]:
        words = sub_query.split(' ')

        if words[0] in wh_words.keys() and words[1] in ['was', 'were', 'is', 'are', 'will', 'would', 'did', 'do']:
            final_result = prev_res
            continue
        # check = True
        # if words[0] in prepositions:
        #     tmp = len(words[0])+1
        #     sub_query = sub_query[tmp:]
        #     check = False

        if words[0] == "'s":
            print(prev_res+sub_query)
            result = search_engine.search(prev_res+sub_query)
        else:
            print(sub_query+' '+prev_res)
            result = search_engine.search(sub_query+' ' +prev_res)
        print(result)
        final_result = result
        
        prefix = ''#words[0]
        if words[0] in wh_words.keys():
            prefix = wh_words[words[0]]
        prev_res = prefix + ' ' +result

    return final_result

if __name__ == "__main__":
    # query = input("Enter query: ")
    query_tree = ['who is', 'the wife of', 'the president of usa', 'when gandhi was born']
    result = progressive_searcher(query_tree)
    print(result)

    

        