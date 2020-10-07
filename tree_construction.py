# def tree_construction(doc):
import spacy
# from syntax_analyzer import *

def print_state(type_array, curr_type, curr_q, chain):
    for type_ in type_array:
        print(type_['ind'])
    print('**variables**')
    print(curr_q)
    print(curr_type)
    print(chain)

def tree_construction(sent, pos_qs, prep_qs, wh_qs, when_qs):
    # print(type(prep_qs[0][0]))
    chain = []

    type_array = [{"sub_queries":pos_qs},{"sub_queries":prep_qs},{"sub_queries":wh_qs},{"sub_queries":when_qs}]
    for i in range(4):
        type_array[i]["ind"] = -1
        type_array[i]["words"] = []
        type_array[i]["end_points"] = []
        for k in type_array[i]["sub_queries"]:
            for j in k:
                type_array[i]["words"].append(j)
            type_array[i]["end_points"].append(len(type_array[i]["words"])-1)
        if len(type_array[i]['words']) > 0:
            type_array[i]["ind"] = 0


    curr_ind = 1
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

    pos_query = []
    pos_encountered = False
    for token in sent[1:]:
        print(token)
        i=0
        check=False

        if pos_encountered:
            type_ = type_array[0]
            if type_['ind']-1 in type_['end_points'] and (type_['ind'] == len(type_['words']) or type_['words'][type_['ind']] != '-'):
                pos_encountered = False
                pos_query.reverse()
                chain.extend(pos_query)
            else:
                if type_['ind']-1 in type_['end_points']:
                    type_['ind'] += 2
                if token.text == "'s":
                    curr_q += token.text
                else:
                    curr_q += ' ' + token.text
                if type_['ind'] in type_['end_points']:
                    pos_query.append(curr_q)
                    curr_q = ""
            print(pos_query, curr_q)

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
                            chain.append(curr_q)
                        curr_q = token.text
                        curr_type = i
                    elif type_['ind'] in type_['end_points']:
                        # if i==0:
                        #     pos_encountered = 2
                        #     curr_q += ' '+token.text
                        # else:
                        curr_q += ' '+token.text
                        chain.append(curr_q)
                        curr_q = ''
                    else:
                        # if i==0:
                        #     pos_encountered=1
                        curr_q += ' '+token.text
                    check = True
                type_['ind'] += 1
            i += 1
        curr_ind += 1

        # print_state(type_array, curr_type, curr_q, chain)

    if len(pos_query) != 0:
        pos_query.reverse()
        chain.extend(pos_query)

    print(chain)

    return chain

if __name__ == "__main__":
    en = spacy.load('en')
    text = "who was the wife of the president of usa when gandhi was born"
    doc = en(text)

    # pos_qs = []
    # prep_qs = [['the', 'birthday', 'of'], ['the', 'wife', 'of'], ['president', 'of', 'usa']]
    # wh_qs = [['what', 'is', 'the', 'birthday', 'of', 'the', 'wife', 'of', 'president', 'of', 'usa']]
    # when_qs =[]

    pos_qs = []
    prep_qs = [['the', 'wife', 'of'], ['the', 'president', 'of', 'usa']]
    wh_qs = [['who', 'was', 'the', 'wife', 'of', 'the', 'president', 'of', 'usa']]
    when_qs = [['when', 'gandhi', 'was', 'born']]


    tree_construction(doc, pos_qs, prep_qs, wh_qs, when_qs)