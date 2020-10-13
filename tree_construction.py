# def tree_construction(doc):
import spacy
from query_tree import Query, QueryTree, print_qt
# from syntax_analyzer import *

def print_state(type_array, curr_type, curr_q, qt, cn):
    for type_ in type_array:
        print(type_['ind'])
    print('**variables**')
    print(curr_q)
    print(curr_type)
    print(cn.node)
    print_qt(qt)

def tree_construction(sent, pos_qs, prep_qs, wh_qs, when_qs):
    # print(type(prep_qs[0][0]))
    # for ind, i in enumerate(wh_qs[:-1]):
    #     if i[-1] == wh_qs[ind+1][0] or i[-1] == 'when':
    #         i.pop(-1)
    # if wh_qs[-1][-1] == 'when':
    #     wh_qs[-1].pop(-1)

    # chain = []
    qt = QueryTree()
    prefixes = []
    prev_word=''

    type_array = [{"sub_queries":pos_qs},{"sub_queries":prep_qs},{"sub_queries":wh_qs},{"sub_queries":when_qs}]
    for i in range(4):
        type_array[i]["ind"] = -1
        type_array[i]["words"] = []
        type_array[i]["end_points"] = []
        for k in type_array[i]["sub_queries"]:
            for j in k:
                type_array[i]["words"].append(j)
            type_array[i]["end_points"].append(len(type_array[i]["words"])-1)
            if i==2:
                prefixes.append(prev_word)
                prev_word = type_array[i]['words'][-1]
        if len(type_array[i]['words']) > 0:
            type_array[i]["ind"] = 0

    curr_node = qt
    curr_ind = 1
    pre_ind = 0
    curr_type = 0
    token = sent[0]
    curr_q = token.text
    i=0
    check=False
    for type_ in type_array:
        if type_['ind'] == -1:
            i += 1
            continue
        if type_['words'][type_['ind']] == token.text:
            type_['ind'] += 1
            if not check:
                check = True
                curr_type = i
        i += 1

    pos_node = None
    pos_encountered = False
    for token in sent[1:]:
        # print(token)
        i=0
        check=False

        if pos_encountered:
            type_ = type_array[0]
            if type_['ind']-1 in type_['end_points'] and (type_['ind'] == len(type_['words']) or type_['words'][type_['ind']] != '-'):
                pos_encountered = False
                curr_node = curr_node.right_child
                # pos_node = None
            else:
                if type_['ind']-1 in type_['end_points']:
                    type_['ind'] += 2
                if token.text == "'s":
                    curr_q += token.text
                else:
                    curr_q += ' ' + token.text
                if type_['ind'] in type_['end_points']:
                    # if curr_node.node.type_ != 0:
                    #     curr_node = curr_node.add_right_child(Query(curr_q, 0))
                    #     pos_node = curr_node
                    # else:
                    curr_node.add_right_child(Query(curr_q, 0))
                    curr_q = ""

        for type_ in type_array:
            if type_['ind'] == -1 or type_['ind'] >= len(type_['words']):
                i += 1
                continue

            if type_['words'][type_['ind']] == token.text and (type_['ind'] in type_['end_points'] or type_['words'][type_['ind']+1] == sent[curr_ind+1].text):
                if not pos_encountered and not check:
                    if curr_type != i:
                        if i==0:
                            pos_encountered=True
                        if len(curr_q) != 0:
                            if curr_type==2:
                                curr_node = curr_node.add_right_child(Query(prefixes[pre_ind]+' '+curr_q, curr_type))
                                pre_ind += 1
                            else:
                                curr_node = curr_node.add_right_child(Query(curr_q, curr_type))
                        curr_q = token.text
                        curr_type = i
                    elif type_['ind'] in type_['end_points']:
                        curr_q += ' '+token.text
                        if curr_type==2:
                            curr_node = curr_node.add_right_child(Query(prefixes[pre_ind]+' '+curr_q, curr_type))
                            pre_ind += 1
                        else:
                            curr_node = curr_node.add_right_child(Query(curr_q, curr_type))
                        curr_q = ''
                    else:
                        curr_q += ' '+token.text
                    check = True
                type_['ind'] += 1
            i += 1
        curr_ind += 1

        # print_state(type_array, curr_type, curr_q, qt, curr_node)

    if pos_encountered:
        pos_encountered = False
        curr_node = pos_node
        pos_node = None

    # print_qt(qt)

    return qt

if __name__ == "__main__":
    en = spacy.load('en')
    text = "who is the president of usa"
    doc = en(text)

    # pos_qs = []
    # prep_qs = [['the', 'birthday', 'of'], ['the', 'wife', 'of'], ['president', 'of', 'usa']]
    # wh_qs = [['what', 'is', 'the', 'birthday', 'of', 'the', 'wife', 'of', 'president', 'of', 'usa']]
    # when_qs =[]

    pos_qs = []
    prep_qs = [['the', 'president', 'of', 'usa']]
    wh_qs = [['who', 'is', 'the', 'president', 'of', 'usa']]
    when_qs = []


    tree_construction(doc, pos_qs, prep_qs, wh_qs, when_qs)