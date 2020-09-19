# import contextualSpellCheck
import numpy
import spacy
from nltk import Tree
import time

# your code here    



en_nlp = spacy.load('en_core_web_sm')
# contextualSpellCheck.add_to_pipe(en_nlp)
# print(en_nlp.pipe_names)


def tok_format(tok):
    return "_".join([tok.orth_, tok.tag_])


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)

def to_nltk_format(node):
    if node.n_lefts + node.n_rights > 0:
        print(node.orth_ + " ---->  " + node.tag_ + "\n")
        [to_nltk_format(child) for child in node.children]
    else:
        print(node.orth_ + " ---->  " + node.tag_)

def sentence_parser(sentences): 
    doc = en_nlp(sentences)
    [to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
    [to_nltk_format(sent.root) for sent in doc.sents]

    # print(doc._.outcome_spellCheck)

def input_sentences():
    sentences = input("Enter your sentence :")
    start = time.process_time()
    sentence_parser(sentences)
    print("Parser Time Eslaped : " + str(time.process_time() - start))
    
input_sentences()


