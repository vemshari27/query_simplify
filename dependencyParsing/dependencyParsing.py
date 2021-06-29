    # Copyright © 2021 Eric John, Srihari Vemuru. All rights reserved
    
    # This file is part of PTGQ.

    # PTGQ is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # PTGQ is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with PTGQ.  If not, see <https://www.gnu.org/licenses/>.

import spacy
from nltk import Tree
import time
import re

en_nlp = spacy.load('en_core_web_sm')
# print(en_nlp.pipe_names)


def tok_format(tok):
    return "_".join([tok.orth_, tok.tag_])


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)


def get_sent_as_list(sentence):
    return re.split(' ', sentence)


def dependency_parsing(sentence):
    doc = en_nlp(sentence)

    # [to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
    return doc


def runner():
    text = input("Query: ")
    result = dependency_parsing(text)


if __name__ == "__main__":
    runner()
