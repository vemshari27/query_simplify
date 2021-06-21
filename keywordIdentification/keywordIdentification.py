from .syntaxAnalyzer import *


def query_detection(doc, syntax_analyzer):
    [syntax_check(sent.root, None, syntax_analyzer) for sent in doc.sents]
    return


def syntax_check(node, parent, syntax_analyzer):
    logging.info("Current Node = " + str(node))
    if node.n_lefts + node.n_rights > 0:
        syntax_analyzer.syntax_analyzer_preorder(node, parent)

        [syntax_check(child, node, syntax_analyzer) for child in node.lefts]
        syntax_analyzer.syntax_analyzer_inorder(node, parent)

        [syntax_check(child, node, syntax_analyzer) for child in node.rights]
        syntax_analyzer.syntax_analyzer_postorder(node, parent)
    else:
        syntax_analyzer.syntax_analyzer_preorder(node, parent)
        syntax_analyzer.syntax_analyzer_inorder(node, parent)
        syntax_analyzer.syntax_analyzer_postorder(node, parent)


def keyword_identification(doc, syntax_analyzer):
    # logging.info("Keyword Identification Running")
    query_detection(doc, syntax_analyzer)
    # syntax_analyzer.print_syntax_analyzer()
