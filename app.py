import spacy

from querytree import input_sentences
from progressive_searcher import progressive_searcher

def app():
    qt = input_sentences()
    result = progressive_searcher(qt)
    return result

if __name__ == "__main__":
    # en_nlp = spacy.load('en')

    # text = input()
    # doc = en_nlp(text)

    result = app()

    print(result)
