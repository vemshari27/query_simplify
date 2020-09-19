from queue import LifoQueue 
from syntax_analyzer_pos import *
from syntax_analyzer_in import *
from syntax_analyzer_wh import *
  
# Initializing
# stack = LifoQueue(maxsize = 100) 
pos = Syntax_Analyzer_POS()
prep = Syntax_Analyzer_IN()
when = Syntax_Analyzer_WHEN()
wh = Syntax_Analyzer_WH()



def syntax_analyzer_discover(tag, node, parent, count) : 
    print(count)

    result_WHEN = when.syntax_analyzer_when_noun(tag, node, parent)
    result_WH = wh.syntax_analyzer_wh_noun(tag, node, parent)

def syntax_analyzer_compute(tag, node, parent, count) :
    
    
    result_PREP = prep.syntax_analyzer_in_detect(tag, node, parent)
    result_WHEN = when.syntax_analyzer_when_detect(tag, node, parent)
    result_WH = wh.syntax_analyzer_wh_detect(tag, node, parent)
    result_WHEN = when.syntax_analyzer_when_verb(tag, node, parent)
    result_WH = wh.syntax_analyzer_wh_verb(tag, node, parent)
        

def syntax_analyzer_covered(tag, node, parent, count) :
    print(count)

    result_POS = pos.syntax_analyzer_pos_detect(tag, node, parent)
    result_PREP = prep.syntax_analyzer_in_noun_start(tag, node, parent)
    result_PREP = prep.syntax_analyzer_in_noun_end(tag, node, parent)

    

def print_syntax_analyzer() :


    print("\nprinting pos")
    pos.print_all_POS()

    print("\nprinting prep")
    prep.print_all_IN()

    print("\nprinting when")
    when.print_all_WHEN()

    print("\nprinting wh")
    wh.print_all_WH()

# -------------------------------------------------------------------------------------------------------

def query_tree_generator(doc):
    [tree_generator(sent.root, None) for sent in doc.sents]

def tree_creator(node, parent):
    if node.n_lefts + node.n_rights > 0:
        [syntax_check(child, node) for child in node.lefts]
        check_form_in_dicts(node)
        # syntax_analyzer_compute(node.tag_, node.orth_, parent)  #inorder meet
        [syntax_check(child, node) for child in node.rights]

    else:
        syntax_analyzer_compute(node.tag_, node.orth_, parent)

def check_form_in_dicts(node) :
    in_when = when.in_WHEN(node)
    in_wh = wh.in_WH(node)
    in_pos = pos.in_POS(node)
    in_prep = prep.in_PREP(node)