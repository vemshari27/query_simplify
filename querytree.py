# import contextualSpellCheck
import spacy
from nltk import Tree
import time
from syntax_analyzer import *

from query_tree import Query, QueryTree
from progressive_searcher import progressive_searcher

en_nlp = spacy.load('en')
# contextualSpellCheck.add_to_pipe(en_nlp)
# print(en_nlp.pipe_names)
count = 0


def tok_format(tok):
    return "_".join([tok.orth_, tok.tag_])


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)


def query_detection(doc):
    sent_break = []
    [syntax_check(sent.root, None) for sent in doc.sents]
    return


def syntax_check(node, parent):
    if node.n_lefts + node.n_rights > 0:
        syntax_analyzer_discover(node.tag_, node.orth_, parent) #preorder meet
        

        [syntax_check(child, node) for child in node.lefts] 
        syntax_analyzer_compute(node.tag_, node.orth_, parent) #inorder meet
        
        

        [syntax_check(child, node) for child in node.rights]
        syntax_analyzer_covered(node.tag_, node.orth_, parent) #post ordermeet
    else:
        syntax_analyzer_discover(node.tag_, node.orth_, parent)
        syntax_analyzer_compute(node.tag_, node.orth_, parent)
        syntax_analyzer_covered(node.tag_, node.orth_, parent) 





def sentence_parser(sentences): 
    doc = en_nlp(sentences)
    [to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
    query_detection(doc)
    print_syntax_analyzer()
    qt =  query_tree_generator(doc)
    result_dic = {}
    progressive_searcher(qt, result_dic)
    return result_dic
    # print(doc._.outcome_spellCheck)


class Run_Search_Engine:
    def run_query_processor(sentences):
        start = time.process_time()
        print("Parser Time Elapsed : " + str(time.process_time() - start))
        return sentence_parser(sentences['search'])