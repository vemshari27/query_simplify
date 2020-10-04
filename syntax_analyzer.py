
from syntax_analyzer_pos import *
from syntax_analyzer_in import *
from syntax_analyzer_wh import *
from tree_construction import *

import copy

  
# Initializing classes

pos = Syntax_Analyzer_POS()
prep = Syntax_Analyzer_IN()
when = Syntax_Analyzer_WHEN()
wh = Syntax_Analyzer_WH()
#------------------------------------------------------------------------------------------------------------
# CODE FOR BREAKING ON PREPOSITONS
# lists for current nouns being used from dict
list_prep_noun1 = []
list_prep_noun2 = []

# state of prepositions
class State_IN:
    def __init__(self):
        self.noun1 = 0
        self.noun2 = 0

# query objects for prep
state_prep = State_IN()
prep_query = []
prep_end = ""
under_construction_prep = -1

# calculate state of prep
def check_state_prep() :
    if(state_prep.noun1 == 0 and state_prep.noun2 == 0):
        return -1
    elif(state_prep.noun1 == 1 and state_prep.noun2 == 0):
        return 0
    elif(state_prep.noun1 == 1 and state_prep.noun2 == 1):
        return 1 
    elif(state_prep.noun1 >= 1 and state_prep.noun2 == 0):
        return 1
    else:
        return 0

def add_to_query_prep_end(state, node, add_insert):
    if(state == 1) :
            # print("completed")
            if(add_insert == 1) :
                prep_query.append(str(node))
            # print(prep_query)
            prep.add_subquery(prep_query)
            prep_query.clear()
            state_prep.noun2 = 0

def add_to_query_prep(state, node):
    if(state == 0) :
            # print("underconstruction")
            prep_query.append(str(node))


def print_states_prep():
    print(str(state_prep.noun1) + "  " + str(state_prep.noun2))

# -------------------------------------------------------------------------------------------------------
# CODE FOR BREAKING ON POSSESSIVE ENDINGS

# lists for current nouns being used from dict
list_pos_noun1 = []
list_pos_noun2 = []

# state of prepositions
class State_POS:
    def __init__(self):
        self.noun1 = 0
        self.noun2 = 0

# query objects for prep
state_pos = State_POS()
pos_query = []
pos_end = ""
under_construction_pos = -1

# calculate state of prep
def check_state_pos() :
    if(state_pos.noun1 == 0 and state_pos.noun2 == 0):
        return -1
    elif(state_pos.noun1 == 1 and state_pos.noun2 == 0):
        return 0
    elif(state_pos.noun1 == 1 and state_pos.noun2 == 1):
        return 1 
    else:
        return -1

def add_to_query_pos_end(state, node, add_insert):
    if(state == 1) :
            # print("completed")
            if(add_insert == 1) :
                pos_query.append(str(node))
            # print(pos_query)
            pos.add_subquery(pos_query)
            pos_query.clear()
            state_pos.noun2 = 0
            state_pos.noun1 = 0

def add_to_query_pos(state, node):
    if(state == 0) :
            # print("underconstruction")
            pos_query.append(str(node))



def print_states_pos():
    print(str(state_pos.noun1) + "  " + str(state_pos.noun2))

def add_left_children(node):
    p_query = []
    [iterate_left(child, p_query) for child in node.lefts]
    

def iterate_left(node, p_query):
    
    if node.n_lefts + node.n_rights > 0 :
        [iterate_left(child, p_query) for child in node.lefts]

        pos_query.append(str(node))
        
        [iterate_left(child, p_query) for child in node.rights]
    else :
        pos_query.append(str(node))

#------------------------------------------------------------------------------------------------------------
# CODE FOR BREAKING ON WH_WORDS
# lists for current nouns being used from dict
list_wh_verb = []
list_wh_noun = []

# state of prepositions
class State_WH:
    def __init__(self):
        self.verb = 0
        self.noun = 0

# query objects for prep
state_wh = State_WH()
wh_query = []
wh_end = ""
under_construction_wh = -1

# calculate state of prep
def check_state_wh() :
    if(state_wh.verb == 0 and state_wh.noun == 0):
        return -1
    elif(state_wh.verb == 1 and state_wh.noun == 0):
        return 0
    elif(state_wh.verb == 1 and state_wh.noun == 1):
        return 0
    elif(state_wh.verb == 2 and state_wh.noun == 1):
        return 1 
    else:
        return 0

def check_state_wh_noun() :
    if(state_wh.noun == 1):
        return 1


def add_to_query_wh_end(state, node, add_insert):
    if(state == 1) :
            # print("completed wh "  + str(node))
            if(add_insert == 1) :
                wh_query.append(str(node))
            # print(wh_query)
            wh.add_subquery(wh_query)
            wh_query.clear()
            state_wh.verb = 1
            state_wh.noun = 0


def add_to_query_wh(state, node):
    if(state == 0 or state == 1) :
            # print("underconstruction wh " + str(node))
            wh_query.append(str(node))
            # print(wh_query)


def print_states_wh():
    print(str(state_wh.verb) + "  " + str(state_wh.noun))

#------------------------------------------------------------------------------------------------------------
# CODE FOR BREAKING ON WHEN
# lists for current nouns being used from dict
# lists for current nouns being used from dict
list_when_verb = []
list_when_noun = []

# state of prepositions
class State_WHEN:
    def __init__(self):
        self.verb = 0
        self.noun = 0

# query objects for prep
state_when = State_WHEN()
when_query = []
when_end = ""
under_construction_when = -1

# calculate state of prep
def check_state_when() :
    if(state_when.verb == 0 and state_when.noun == 0):
        return -1
    elif(state_when.verb == 1 and state_when.noun == 0):
        return 0
    elif(state_when.verb == 1 and state_when.noun == 1):
        return 0
    elif(state_when.verb == 2 and state_when.noun == 1):
        return 1 
    else:
        return 0


def add_to_query_when_end(state, node, add_insert):
    if(state == 1) :
            # print("completed when "  + str(node))
            if(add_insert == 1) :
                when_query.append(str(node))
            # print(when_query)
            when.add_subquery(when_query)
            when_query.clear()
            wh_query.clear()
            state_when.verb = 0
            state_when.noun = 0


def add_to_query_when(state, node):
    if(state == 0 or state == 1) :
            # print("underconstruction when " + str(node))
            when_query.append(str(node))
            # print(when_query)


def print_states_when():
    print(str(state_when.verb) + "  " + str(state_when.noun))

# ----------------------------------------------------------------------------------------------------------
# CODE FOR CHECKING OVERLAPPING WH or WHEN
prev_state = -1
#check if all analyzers are sleeping
def check_state_all() :
    global prev_state
    if(check_state_when() == 1 and check_state_wh() == 0 and check_state_wh_noun() == 1 and prev_state == 1):
        prev_state = 0
        return [1,1]

    elif((check_state_when() == 0 or check_state_wh() == 0) and prev_state == 1 ):
        prev_state = 0
        if(check_state_when() == 1):
            return [1,1]
        else :
            return [1,0]
    
    else :
        return [0,0]

#------------------------------------------------------------------------------------------------------------
#  CODE FOR SYNTAX ANALYZERS TO CREATE RESPECTIVE DICTIONARIES

def syntax_analyzer_discover(tag, node, parent, count) : 
    # print(str(count) + node)

    result_WHEN = when.syntax_analyzer_when_noun(tag, node, parent)
    result_WH = wh.syntax_analyzer_wh_noun(tag, node, parent)

def syntax_analyzer_compute(tag, node, parent, count) :
    # print(str(count) + node)
    
    result_PREP = prep.syntax_analyzer_in_detect(tag, node, parent)
    result_WHEN = when.syntax_analyzer_when_detect(tag, node, parent)
    result_WH = wh.syntax_analyzer_wh_detect(tag, node, parent)
    result_WHEN = when.syntax_analyzer_when_verb(tag, node, parent)
    result_WH = wh.syntax_analyzer_wh_verb(tag, node, parent)
        

def syntax_analyzer_covered(tag, node, parent, count) :
    # print(str(count) + node)

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

    print("\nCLEAR\n")

# -------------------------------------------------------------------------------------------------------
# CODE FOR USING DICTIONARIES AND DEPENDENCY TREE TO CREATE SUBQUERIES
def query_tree_generator(doc):
    [tree_creator(sent.root, None) for sent in doc.sents]
    wh.add_subquery(wh_query)
    when.add_subquery(when_query)

    print("printing subqueries")
    # print(pos.pos_queries) 
    # print(prep.prep_queries)
    # print(wh.wh_queries)
    # print(when.when_queries)

    pos_queries =  copy.deepcopy(pos.pos_queries)
    prep_queries =  copy.deepcopy(prep.prep_queries)
    wh_queries =  copy.deepcopy(wh.wh_queries)
    when_queries =  copy.deepcopy(when.when_queries)

    print(pos_queries)
    print(prep_queries)
    print(wh_queries)
    print(when_queries)

    # tree_construction(doc)



def tree_creator(node, parent):
    if node.n_lefts + node.n_rights > 0:
        # PREORDER DETECTION

        # print("current node " +str(node))

        # print_states_prep()
        # print_states_pos()
        # print_states_wh()
        # print_states_when()

        # PREP
        check_prep_in_dicts(node.orth_) 
        under_construction_prep = check_state_prep()
        add_to_query_prep_end(under_construction_prep, node.orth_, 0)

        # POS
        

        # WH
        check_wh_in_dicts(node.orth_)

        #WHEN
        check_when_in_dicts(node.orth_)

        [tree_creator(child, node) for child in node.lefts]
        # INORDER DETECTION

        # print("current node " +str(node))

        # print_states_prep()
        # print_states_pos()
        # print_states_wh()
        # print_states_when()

        # PREP
        found_prep_end(node.orth_) #inorder end
        under_construction_prep = check_state_prep()
        add_to_query_prep(under_construction_prep, node.orth_)
        
        # POS
        check_pos_end(node) 
        under_construction_pos = check_state_pos()
        add_to_query_pos_end(under_construction_pos,node,1)
        check_pos_in_dicts(node)
        under_construction_pos = check_state_pos()
        add_to_query_pos(under_construction_pos,node)
        

        # WH 
        check_wh_end(node.orth_)
        found_wh_verb(node.orth_)
        under_construction_wh = check_state_wh()
        under_construction_others, wh_type = check_state_all() # check if valid end
        add_to_query_wh_end((under_construction_others and not wh_type), node.orth_, 1)
        add_to_query_wh(under_construction_wh, node.orth_)

        #WHEN
        check_when_end(node.orth_)
        found_when_verb(node.orth_)
        under_construction_when = check_state_when()
        under_construction_others, wh_type = check_state_all() # check if valid end
        add_to_query_when_end((under_construction_others and wh_type), node.orth_, 1)
        add_to_query_when(under_construction_when, node.orth_)
        

        
        [tree_creator(child, node) for child in node.rights]

        # POSTORDER DETECTION

    else:

        # print("current node " +str(node))

        # print_states_prep()
        # print_states_pos()
        # print_states_wh()
        # print_states_when()

        # PREP
        check_prep_in_dicts(node.orth_)  #preorder detection
        found_prep_end(node.orth_) #inorder end
        under_construction_prep = check_state_prep()
        add_to_query_prep_end(under_construction_prep, node.orth_, 1)
        add_to_query_prep(under_construction_prep, node.orth_)

        # POS
        check_pos_end(node)
        under_construction_pos = check_state_pos()
        add_to_query_pos_end(under_construction_pos, node, 1)
        check_pos_in_dicts(node)
        under_construction_pos = check_state_pos()
        add_to_query_pos(under_construction_pos, node)

        # WH
        check_wh_end(node.orth_)
        under_construction_wh = check_state_wh()
        under_construction_others, wh_type = check_state_all() # check if valid end
        add_to_query_wh_end((under_construction_others and not wh_type), node.orth_, 1)
        add_to_query_wh(under_construction_wh, node.orth_)
        
        #WHEN
        check_when_end(node.orth_)
        under_construction_when = check_state_when()
        under_construction_others, wh_type = check_state_all() # check if valid end
        add_to_query_when_end((under_construction_others and wh_type), node.orth_, 1)
        add_to_query_when(under_construction_when, node.orth_)
        
        
        
    
# ---------------------------------------------------------------------------------------------------
# GENERATING PREPOSITION QUERIES

def check_prep_in_dicts(node) : # checking preorder for noun in prep dictionary
    global prep_end
    # print("check prep start with " + str(node))

    if(list_prep_noun1 == [] or node != list_prep_noun1[0]) :
        list_prep = prep.in_PREP(node)
          
        if(list_prep != None) :
            # list_prep.reverse() # assuming a direct connection will not have same word used again
            list_prep_noun1.append(node)
            list_prep_noun2.append(list_prep)
            state_prep.noun1 += 1
            check_prep_end(node)
            prep_end = list_prep[0]
            # print("found valid begin " + str(node))
        
        # print(list_prep_noun1)
        # print(list_prep_noun2)
        
    elif(node == list_prep_noun1[0]) :
        state_prep.noun1 += 1
        # print("printing else " + str(list_prep_noun1))
        check_prep_end(node)
        prep_end = list_prep_noun2[0][0]
        # print(prep_end)
        

    check_prep_end(node)

def check_prep_end(node): #checking preorder if end of the query is found 
    global list_prep_noun2
    global list_prep_noun1
    
    # print("check prep end with " + str(node))

    if(list_prep_noun2 != [] and list_prep_noun2 != [[]]):
        # print("list noun 2")
        # print(list_prep_noun2)
        list_first_obj = list_prep_noun2[0]

        if(node == list_first_obj[0]) :
            # print("found valid end " + str(node))
            
            # print("list end " + str(list_prep_noun2 ))
            state_prep.noun2 = 1
            state_prep.noun1 -= 1
            list_prep_noun2 = list_prep_noun2[1:]
            list_first_obj = list_first_obj[1:]
            # print(list_first_obj)
            

            if(list_first_obj == []):
                # print("list end " + str(list_prep_noun2))
                list_prep_noun1 = list_prep_noun1[1:]
            else :
                list_prep_noun1.append(list_prep_noun1[0])
                list_prep_noun1 = list_prep_noun1[1:]
                list_prep_noun2.append(list_first_obj)
        # print("End found " + str(node.orth_))

    return 

def found_prep_end(node): # finding inorder the end of prep
    # print("node in inorder search " + str(node) + " " + str(prep_end))
    if(node == prep_end):
        # print("found prep end " + str(node))
        # OPERATION PREP
        add_to_query_prep_end(1,node,1)
    return



# ---------------------------------------------------------------------------------------------------
# GENERATING POSSESSIVE ENDING QUERIES

def check_pos_in_dicts(node) : # checking inorder for noun in pos dictionary
    global pos_end
    # print("check pos start with " + str(node))

    if(list_pos_noun1 == [] or node.orth_ != list_pos_noun1[0]) :
        list_pos = pos.in_POS(node.orth_)
        
        
        if(list_pos != None) :
            list_pos_noun1.append(node.orth_)
            list_pos_noun2.append(list_pos)
            state_pos.noun1 = 1
            if(pos_end == str(node)) : # connected POS
                # print("directly connected")
                pos_query.append("-")
            else : #unconnected,noun addons, added beginning
                # print("not connected")
                add_left_children(node) 
            pos_end = str(list_pos[0])
            # print("found valid begin " + str(node))
        
        # print(list_pos_noun1)
        # print(list_pos_noun2)
    else :
        state_pos.noun1 = 1
        if(pos_end == str(node)):
            # print("directly connected")
            pos_query.append("-")
        else : #unconnected,noun addons, added beginning
            # print("not connected")
            add_left_children(node) 
        pos_end = str(list_pos_noun2[0][0])
        # print("found valid begin " + str(node))

def check_pos_end(node): #checking inorder if end of the query is found 
    global list_pos_noun2
    global list_pos_noun1
    
    # print("check pos end with " + str(node))

    if(list_pos_noun2 != [] and list_pos_noun2 != [[]]):
        # print("list noun 2")
        # print(list_pos_noun2)
        list_first_obj = list_pos_noun2[0]

        if(node == list_first_obj[0]):
            # print("found valid end " + str(node))
            
            # print("list end " + str(list_pos_noun2))
            state_pos.noun2 = 1
            list_pos_noun2 = list_pos_noun2[1:]
            list_first_obj = list_first_obj[1:]
            # print("print after removal " + str(list_first_obj))
            

            if(list_first_obj == []):
                # print("list empty " + str(list_pos_noun2))
                list_pos_noun1 = list_pos_noun1[1:]
            else :
                list_pos_noun1.append(list_pos_noun1[0])
                list_pos_noun1 = list_pos_noun1[1:]
                list_pos_noun2.append(list_first_obj)
                # print(list_pos_noun2)
        # print("End found " + str(node.orth_))
    return 

# ---------------------------------------------------------------------------------------------------
# GENERATING WH WORD QUERIES

def check_wh_in_dicts(node) : # checking preorder for verb in wh dictionary
    global wh_end
    # print("check wh start with " + str(node))

    if(list_wh_verb == [] or node != list_wh_verb[0]) :
        list_wh = wh.in_WH(node)
        # print(list_wh)
        
        if(list_wh != None) :
            list_wh_verb.append(node)
            list_wh_noun.append(list_wh)
            state_wh.verb = 1
            state_wh.noun = 0
            wh_end = node
            # print("found valid begin wh " + str(node))
        
        # print(list_wh_verb)
        # print(list_wh_noun)
    else :
        state_wh.verb = 1
        state_wh.noun = 0
        wh_end = list_wh_verb[0]
        # print("found valid begin wh " + str(node))

def check_wh_end(node): #checking inorder if end of the query is found 
    global list_wh_verb
    global list_wh_noun
    global prev_state
    
    # print("check wh end with " + str(node))

    if(list_wh_noun != [] and list_wh_noun != [[]]):
        # print("list wh noun")
        # print(list_wh_noun)
        list_first_obj = list_wh_noun[0]

        if(node == list_first_obj[0]):
            # print("found valid end wh " + str(node))
            
            # print("list end " + str(list_wh_noun))
            state_wh.noun = 1
            if(state_wh.verb == 2):
                prev_state = 1

            list_wh_noun = list_wh_noun[1:]
            list_first_obj = list_first_obj[1:]

            
            # print("print after removal " + str(list_first_obj))
            

            if(list_first_obj == []):
                # print("list empty " + str(list_wh_noun))
                list_wh_verb = list_wh_verb[1:]
            else :
                list_wh_verb.append(list_wh_verb[0])
                list_wh_verb = list_wh_verb[1:]
                list_wh_noun.append(list_first_obj)
                # print(list_wh_noun)
        # print("End found " + str(node.orth_))
    return 

def found_wh_verb(node): # inorder confirmation the verb has been covered
    global prev_state
    if(node == wh_end) :
        state_wh.verb = 2
        if(state_wh.noun == 1):
                prev_state = 1
                # print("covered " + str(state_wh.verb) + " " + str(state_wh.noun))

# ---------------------------------------------------------------------------------------------------
# GENERATING WHEN WORD QUERIES

def check_when_in_dicts(node) : # checking preorder for verb in when dictionary
    global when_end
    # print("check when start with " + str(node))

    if(list_when_verb == [] or node != list_when_verb[0]) :
        list_when = when.in_WHEN(node)
        # print(list_when)
        
        if(list_when != None) :
            list_when_verb.append(node)
            list_when_noun.append(list_when)
            state_when.verb = 1
            state_when.noun = 0
            when_end = node
            # print("found valid begin when " + str(node))
        
        # print(list_when_verb)
        # print(list_when_noun)
    else :
        state_when.verb = 1
        state_when.noun = 0
        when_end = list_when_verb[0]
        # print("found valid begin when " + str(node))

def check_when_end(node): #checking inorder if end of the query is found 
    global list_when_verb
    global list_when_noun
    global prev_state
    
    # print("check when end with " + str(node))

    if(list_when_noun != [] and list_when_noun != [[]]):
        # print("list when noun")
        # print(list_when_noun)
        list_first_obj = list_when_noun[0]

        if(node == list_first_obj[0]):
            # print("found valid end when " + str(node))
            
            # print("list end " + str(list_when_noun))
            state_when.noun = 1
            if(state_when.verb == 2):
                prev_state = 1

            list_when_noun = list_when_noun[1:]
            list_first_obj = list_first_obj[1:]

            
            # print("print after removal " + str(list_first_obj))
            

            if(list_first_obj == []):
                # print("list empty " + str(list_when_noun))
                list_when_verb = list_when_verb[1:]
            else :
                list_when_verb.append(list_when_verb[0])
                list_when_verb = list_when_verb[1:]
                list_when_noun.append(list_first_obj)
                # print(list_when_noun)
        # print("End found " + str(node.orth_))
    return 

def found_when_verb(node): # inorder confirmation the verb has been covered
    global prev_state
    if(node == when_end) :
        state_when.verb = 2
        if(state_when.noun == 1):
                prev_state = 1
                # print("covered " + str(state_when.verb) + " " + str(state_when.noun))
    return

# -------------------------------------------------------------------------------------------------------