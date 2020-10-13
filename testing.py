import spacy

from querytree import sentence_parser
from query_tree import Query, QueryTree
from progressive_searcher import progressive_searcher

def app():
    text = input()
    result = sentence_parser(text)
    return result

if __name__ == "__main__":
    # en_nlp = spacy.load('en')

    # text = input()
    # doc = en_nlp(text)

    result = app()

    print(result)

