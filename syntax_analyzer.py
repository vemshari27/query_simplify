
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

class State_PREP:
    def __init__(self):
        # states
        self.noun1 = 0
        self.noun2 = 0
        # lists for current nouns being used from dict
        self.list_prep_noun1 = []
        self.list_prep_noun2 = []
        # query objects for prep
        self.prep_query = []
        self.prep_end = ""
        self.under_construction_prep = -1

    # calculate state of prep
    def check_state_prep(self) :
        if(self.noun1 == 0 and self.noun2 == 0):
            return -1
        elif(self.noun1 == 1 and self.noun2 == 0):
            return 0
        elif(self.noun1 == 1 and self.noun2 == 1):
            return 1 
        elif(self.noun1 >= 1 and self.noun2 == 0):
            return 1
        else:
            return 0

    def add_to_query_prep_end(self, state, node, add_insert):
        if(state == 1) :
                # print("completed")
                if(add_insert == 1) :
                    self.prep_query.append(str(node))
                # print(prep_query)
                prep.add_subquery(self.prep_query)
                self.prep_query.clear()
                self.noun2 = 0

    def add_to_query_prep(self, state, node):
        if(state == 0) :
                # print("underconstruction")
                self.prep_query.append(str(node))


    def print_states_prep(self):
        print(str(self.noun1) + "  " + str(self.noun2))
    
    def clear_prep(self):
        # states
        self.noun1 = 0
        self.noun2 = 0
        # lists for current nouns being used from dict
        self.list_prep_noun1.clear()
        self.list_prep_noun2.clear()
        # query objects for prep
        self.prep_query.clear()
        self.prep_end = ""
        self.under_construction_prep = -1

    # ---------------------------------------------------------------------------------------------------
    # GENERATING PREPOSITION QUERIES

    def check_prep_in_dicts(self,node) : # checking preorder for noun in prep dictionary
        # print("check prep start with " + str(node))

        if(self.list_prep_noun1 == [] or node != self.list_prep_noun1[0]) :
            list_prep = prep.in_PREP(node)
            
            if(list_prep != None) :
                # list_prep.reverse() # assuming a direct connection will not have same word used again
                self.list_prep_noun1.append(node)
                self.list_prep_noun2.append(list_prep)
                self.noun1 += 1
                self.check_prep_end(node)
                self.prep_end = list_prep[0]
                # print("found valid begin " + str(node))
            
            # print(list_prep_noun1)
            # print(list_prep_noun2)
            
        elif(node == self.list_prep_noun1[0]) :
            self.noun1 += 1
            # print("printing else " + str(list_prep_noun1))
            self.check_prep_end(node)
            self.prep_end = self.list_prep_noun2[0][0]
            # print(prep_end)
        self.check_prep_end(node)

    def check_prep_end(self, node): #checking preorder if end of the query is found 
        # print("check prep end with " + str(node))

        if(self.list_prep_noun2 != [] and self.list_prep_noun2 != [[]]):
            # print("list noun 2")
            # print(list_prep_noun2)
            list_first_obj = self.list_prep_noun2[0]

            if(node == list_first_obj[0]) :
                # print("found valid end " + str(node))
                
                # print("list end " + str(list_prep_noun2 ))
                self.noun2 = 1
                self.noun1 -= 1
                self.list_prep_noun2 = self.list_prep_noun2[1:]
                list_first_obj = list_first_obj[1:]
                # print(list_first_obj)
                

                if(list_first_obj == []):
                    # print("list end " + str(list_prep_noun2))
                    self.list_prep_noun1 = self.list_prep_noun1[1:]
                else :
                    self.list_prep_noun1.append(self.list_prep_noun1[0])
                    self.list_prep_noun1 = self.list_prep_noun1[1:]
                    self.list_prep_noun2.append(list_first_obj)
            # print("End found " + str(node.orth_))

        return 

    def found_prep_end(self, node): # finding inorder the end of prep
        # print("node in inorder search " + str(node) + " " + str(prep_end))
        if(node == self.prep_end):
            # print("found prep end " + str(node))
            # OPERATION PREP
            self.add_to_query_prep_end(1,node,1)
        return



# -------------------------------------------------------------------------------------------------------
# CODE FOR BREAKING ON POSSESSIVE ENDINGS
class State_POS:
    def __init__(self):
        # state
        self.noun1 = 0
        self.noun2 = 0
        # lists for current nouns being used from dict
        self.list_pos_noun1 = []
        self.list_pos_noun2 = []
        # query objects for prep
        self.pos_query = []
        self.pos_end = ""
        self.under_construction_pos = -1

    # calculate state of prep
    def check_state_pos(self) :
        if(self.noun1 == 0 and self.noun2 == 0):
            return -1
        elif(self.noun1 == 1 and self.noun2 == 0):
            return 0
        elif(self.noun1 == 1 and self.noun2 == 1):
            return 1 
        else:
            return -1

    def add_to_query_pos_end(self, state, node, add_insert):
        if(state == 1) :
                # print("completed")
                if(add_insert == 1) :
                    self.pos_query.append(str(node))
                # print(pos_query)
                pos.add_subquery(self.pos_query)
                self.pos_query.clear()
                self.noun2 = 0
                self.noun1 = 0

    def add_to_query_pos(self, state, node):
        if(state == 0) :
                # print("underconstruction")
                self.pos_query.append(str(node))



    def print_states_pos(self):
        print(str(self.noun1) + "  " + str(self.noun2))

    def clear_pos(self):
        # state
        self.noun1 = 0
        self.noun2 = 0
        # lists for current nouns being used from dict
        self.list_pos_noun1.clear()
        self.list_pos_noun2.clear()
        # query objects for prep
        self.pos_query.clear()
        self.pos_end = ""
        self.under_construction_pos = -1

    def add_left_children(self, node):
        p_query = []
        [self.iterate_left(child, p_query) for child in node.lefts]
    

    def iterate_left(self, node, p_query):
        
        if node.n_lefts + node.n_rights > 0 :
            [self.iterate_left(child, p_query) for child in node.lefts]

            self.pos_query.append(str(node))
            
            [self.iterate_left(child, p_query) for child in node.rights]
        else :
            self.pos_query.append(str(node))

    # ---------------------------------------------------------------------------------------------------
    # GENERATING POSSESSIVE ENDING QUERIES

    def check_pos_in_dicts(self, node) : # checking inorder for noun in pos dictionary
        # print("check pos start with " + str(node))

        if(self.list_pos_noun1 == [] or node.orth_ != self.list_pos_noun1[0]) :
            list_pos = pos.in_POS(node.orth_)
            
            
            if(list_pos != None) :
                self.list_pos_noun1.append(node.orth_)
                self.list_pos_noun2.append(list_pos)
                self.noun1 = 1
                if(self.pos_end == str(node)) : # connected POS
                    # print("directly connected")
                    self.pos_query.append("-")
                else : #unconnected,noun addons, added beginning
                    # print("not connected")
                    self.add_left_children(node) 
                self.pos_end = str(list_pos[0])
                # print("found valid begin " + str(node))
            
            # print(list_pos_noun1)
            # print(list_pos_noun2)
        else :
            self.noun1 = 1
            if(self.pos_end == str(node)):
                # print("directly connected")
                self.pos_query.append("-")
            else : #unconnected,noun addons, added beginning
                # print("not connected")
                self.add_left_children(node) 
            self.pos_end = str(self.list_pos_noun2[0][0])
            # print("found valid begin " + str(node))

    def check_pos_end(self, node): #checking inorder if end of the query is found 
        # print("check pos end with " + str(node))

        if(self.list_pos_noun2 != [] and self.list_pos_noun2 != [[]]):
            # print("list noun 2")
            # print(list_pos_noun2)
            list_first_obj = self.list_pos_noun2[0]

            if(node == list_first_obj[0]):
                # print("found valid end " + str(node))
                
                # print("list end " + str(list_pos_noun2))
                self.noun2 = 1
                self.list_pos_noun2 = self.list_pos_noun2[1:]
                list_first_obj = list_first_obj[1:]
                # print("print after removal " + str(list_first_obj))
                

                if(list_first_obj == []):
                    # print("list empty " + str(list_pos_noun2))
                    self.list_pos_noun1 = self.list_pos_noun1[1:]
                else :
                    self.list_pos_noun1.append(self.list_pos_noun1[0])
                    self.list_pos_noun1 = self.slist_pos_noun1[1:]
                    self.list_pos_noun2.append(list_first_obj)
                    # print(list_pos_noun2)
            # print("End found " + str(node.orth_))
        return 


#------------------------------------------------------------------------------------------------------------
# CODE FOR BREAKING ON WH_WORDS

class State_WH:
    def __init__(self):
        # states
        self.verb = 0
        self.noun = 0
        # lists for verb and noun being used from dict
        self.list_wh_verb = []
        self.list_wh_noun = []
        # query objects for wh
        self.wh_query = []
        self.wh_end = ""
        self.under_construction_wh = -1

    # calculate state of wh
    def check_state_wh(self) :
        if(self.verb == 0 and self.noun == 0):
            return -1
        elif(self.verb == 1 and self.noun == 0):
            return 0
        elif(self.verb == 1 and self.noun == 1):
            return 0
        elif(self.verb == 2 and self.noun == 1):
            return 1 
        else:
            return 0

    def check_state_wh_noun(self) :
        if(self.noun == 1):
            return 1


    def add_to_query_wh_end(self, state, node, add_insert):
        if(state == 1) :
                # print("completed wh "  + str(node))
                if(add_insert == 1) :
                    self.wh_query.append(str(node))
                # print(self.wh_query)
                wh.add_subquery(self.wh_query)
                self.wh_query.clear()
                self.verb = 0
                self.noun = 0


    def add_to_query_wh(self, state, node):
        if(state == 0 or state == 1) :
                # print("underconstruction wh " + str(node))
                self.wh_query.append(str(node))
                # print(self.wh_query)


    def print_states_wh(self):
        print(str(self.verb) + "  " + str(self.noun))

    def clear_wh(self):
        # states
        self.verb = 0
        self.noun = 0
        # lists for verb and noun being used from dict
        self.list_wh_verb.clear()
        self.list_wh_noun.clear()
        # query objects for wh
        self.wh_query.clear()
        self.wh_end = ""
        self.under_construction_wh = -1

    # ---------------------------------------------------------------------------------------------------
    # GENERATING WH WORD QUERIES

    def check_wh_in_dicts(self, node) : # checking preorder for verb in wh dictionary
        # print("check wh start with " + str(node))

        if(self.list_wh_verb == [] or node != self.list_wh_verb[0]) :
            list_wh = wh.in_WH(node)
            # print(list_wh)
            
            if(list_wh != None) :
                self.list_wh_verb.append(node)
                self.list_wh_noun.append(list_wh)   
                # print(wh_end)
                self.verb = 1
                self.noun = 0
                self.wh_end = str(node)
                # print("found valid begin wh " + str(node))
            
            # print(list_wh_verb)
            # print(list_wh_noun)
        else :
            self.verb = 1
            self.noun = 0
            self.wh_end = str(self.list_wh_verb[0])
            # print("found valid begin wh " + str(node))

    def check_wh_end(self, node): #checking inorder if end of the query is found 
        global prev_state
        
        # print("check wh end with " + str(node))

        if(self.list_wh_noun != [] and self.list_wh_noun != [[]]):
            # print("list wh noun")
            # print(list_wh_noun)
            list_first_obj = self.list_wh_noun[0]

            if(node == list_first_obj[0]):
                # print("found valid end wh " + str(node))
                
                # print("list end " + str(list_wh_noun))
                self.noun = 1
                if(self.verb == 2):
                    prev_state = 1

                self.list_wh_noun = self.list_wh_noun[1:]
                list_first_obj = list_first_obj[1:]

                
                # print("print after removal " + str(list_first_obj))
                

                if(list_first_obj == []):
                    # print("list empty " + str(list_wh_noun))
                    self.list_wh_verb = self.list_wh_verb[1:]
                else :
                    self.list_wh_verb.append(self.list_wh_verb[0])
                    self.list_wh_verb = self.list_wh_verb[1:]
                    self.list_wh_noun.append(list_first_obj)
                    # print(list_wh_noun)
            # print("End found " + str(node.orth_))
        return 

    def found_wh_verb(self, node): # inorder confirmation the verb has been covered
        global prev_state
        # print(str(node) + " " + self.wh_end)
        if(node == self.wh_end) :
            self.verb = 2
            if(self.noun == 1):
                    prev_state = 1
                    # print("covered " + str(state_wh.verb) + " " + str(state_wh.noun))

#------------------------------------------------------------------------------------------------------------
# CODE FOR BREAKING ON WHEN

class State_WHEN:
    def __init__(self):
        # states
        self.verb = 0
        self.noun = 0
        # lists for verb and noun being used from dict
        self.list_when_verb = []
        self.list_when_noun = []
        # query objects for prep
        self.when_query = []
        self.when_end = ""
        self.under_construction_when = -1

    # calculate state of prep
    def check_state_when(self) :
        if(self.verb == 0 and self.noun == 0):
            return -1
        elif(self.verb == 1 and self.noun == 0):
            return 0
        elif(self.verb == 1 and self.noun == 1):
            return 0
        elif(self.verb == 2 and self.noun == 1):
            return 1 
        else:
            return 0


    def add_to_query_when_end(self, state, node, add_insert):
        if(state == 1) :
                # print("completed when "  + str(node))
                if(add_insert == 1) :
                    self.when_query.append(str(node))
                # print(self.when_query)
                when.add_subquery(self.when_query)
                self.when_query.clear()
                state_wh.wh_query.clear()
                self.verb = 0
                self.noun = 0


    def add_to_query_when(self, state, node):
        if(state == 0 or state == 1) :
                # print("underconstruction when " + str(node))
                self.when_query.append(str(node))
                # print(self.when_query)


    def print_states_when(self):
        print(str(self.verb) + "  " + str(self.noun))
    
    def clear_when(self):
        # states
        self.verb = 0
        self.noun = 0
        # lists for verb and noun being used from dict
        self.list_when_verb.clear()
        self.list_when_noun.clear()
        # query objects for prep
        self.when_query.clear()
        self.when_end = ""
        self.under_construction_when = -1

    # ---------------------------------------------------------------------------------------------------
    # GENERATING WHEN WORD QUERIES

    def check_when_in_dicts(self, node) : # checking preorder for verb in when dictionary
        # print("check when start with " + str(node))

        if(self.list_when_verb == [] or node != self.list_when_verb[0]) :
            list_when = when.in_WHEN(node)
            # print(list_when)
            
            if(list_when != None) :
                self.list_when_verb.append(node)
                self.list_when_noun.append(list_when)
                self.verb = 1
                self.noun = 0
                self.when_end = node
                # print("found valid begin when " + str(node))
            
            # print(list_when_verb)
            # print(list_when_noun)
        else :
            self.verb = 1
            self.noun = 0
            self.when_end = self.list_when_verb[0]
            # print("found valid begin when " + str(node))

    def check_when_end(self, node): #checking inorder if end of the query is found 
        global prev_state
        
        # print("check when end with " + str(node))

        if(self.list_when_noun != [] and self.list_when_noun != [[]]):
            # print("list when noun")
            # print(list_when_noun)
            list_first_obj = self.list_when_noun[0]

            if(node == list_first_obj[0]):
                # print("found valid end when " + str(node))
                
                # print("list end " + str(list_when_noun))
                self.noun = 1
                if(self.verb == 2):
                    prev_state = 1

                self.list_when_noun = self.list_when_noun[1:]
                list_first_obj = list_first_obj[1:]

                
                # print("print after removal " + str(list_first_obj))
                

                if(list_first_obj == []):
                    # print("list empty " + str(list_when_noun))
                    self.list_when_verb = self.list_when_verb[1:]
                else :
                    self.list_when_verb.append(self.list_when_verb[0])
                    self.list_when_verb = self.list_when_verb[1:]
                    self.list_when_noun.append(list_first_obj)
                    # print(list_when_noun)
            # print("End found " + str(node.orth_))
        return 

    def found_when_verb(self, node): # inorder confirmation the verb has been covered
        global prev_state
        # print(str(node) + " " + self.when_end)
        if(node == self.when_end) :
            self.verb = 2
            if(self.noun == 1):
                    prev_state = 1
                    # print("covered " + str(state_when.verb) + " " + str(state_when.noun))
        return

# ----------------------------------------------------------------------------------------------------------
# CODE FOR CHECKING OVERLAPPING WH or WHEN
prev_state = -1
#check if all analyzers are sleeping
def check_state_all() :
    global prev_state
    if(state_when.check_state_when() == 1 and state_wh.check_state_wh() == 0 and state_wh.check_state_wh_noun() == 1 and prev_state == 1):

        prev_state = 0
        return [1,1]

    elif((state_when.check_state_when() == 0 or state_wh.check_state_wh() == 0) and prev_state == 1 ):
        prev_state = 0
        if(state_when.check_state_when() == 1):
            return [1,1]
        else :
            return [1,0]
    
    else :
        return [0,0]

#------------------------------------------------------------------------------------------------------------
#  CODE FOR SYNTAX ANALYZERS TO CREATE RESPECTIVE DICTIONARIES

def syntax_analyzer_discover(tag, node, parent) : 


    result_WHEN = when.syntax_analyzer_when_noun(tag, node, parent)
    result_WH = wh.syntax_analyzer_wh_noun(tag, node, parent)

def syntax_analyzer_compute(tag, node, parent) :
    
    result_PREP = prep.syntax_analyzer_in_detect(tag, node, parent)
    result_WHEN = when.syntax_analyzer_when_detect(tag, node, parent)
    result_WH = wh.syntax_analyzer_wh_detect(tag, node, parent)
    result_WHEN = when.syntax_analyzer_when_verb(tag, node, parent)
    result_WH = wh.syntax_analyzer_wh_verb(tag, node, parent)
        

def syntax_analyzer_covered(tag, node, parent) :

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
state_prep = State_PREP()
state_pos = State_POS()
state_wh = State_WH()
state_when = State_WHEN()

def clear_all():
    global prev_state
    state_prep.clear_prep()
    state_pos.clear_pos()
    state_wh.clear_wh()
    state_when.clear_when()
    prep.clear_queries()
    pos.clear_queries()
    wh.clear_queries()
    when.clear_queries()
    prev_state = -1

# CODE FOR USING DICTIONARIES AND DEPENDENCY TREE TO CREATE SUBQUERIES
def query_tree_generator(doc):
    
    [tree_creator(sent.root, None) for sent in doc.sents]
    wh.add_subquery(state_wh.wh_query)
    when.add_subquery(state_when.when_query)

    print("printing subqueries")
    print(pos.pos_queries) 
    print(prep.prep_queries)
    print(wh.wh_queries)
    print(when.when_queries)

    # pos_queries =  copy.deepcopy(pos.pos_queries)
    # prep_queries =  copy.deepcopy(prep.prep_queries)
    # wh_queries =  copy.deepcopy(wh.wh_queries)
    # when_queries =  copy.deepcopy(when.when_queries)

    # print(pos_queries)
    # print(prep_queries)
    # print(wh_queries)
    # print(when_queries)

    # tree_construction(doc)
    qt = tree_construction(doc, pos.pos_queries, prep.prep_queries, wh.wh_queries, when.when_queries)

    clear_all()
    # return str(pos_queries) + " " + str(prep_queries) + " " + str(wh_queries) + " " + str(when_queries)
    return qt



def tree_creator(node, parent):
    if node.n_lefts + node.n_rights > 0:
        # PREORDER DETECTION

        # PREP
        state_prep.check_prep_in_dicts(node.orth_) 
        state_prep.under_construction_prep = state_prep.check_state_prep()
        state_prep.add_to_query_prep_end(state_prep.under_construction_prep, node.orth_, 0)

        # POS

        # WH
        state_wh.check_wh_in_dicts(node.orth_)

        #WHEN
        state_when.check_when_in_dicts(node.orth_)


        # print_states_prep()
        # print_states_pos()
        # print_states_wh()

        [tree_creator(child, node) for child in node.lefts]
        # INORDER DETECTION

        # print("current node " +str(node))

        # print_states_prep()
        # print_states_pos()
        # print_states_wh()

        # PREP
        state_prep.found_prep_end(node.orth_) #inorder end
        state_prep.under_construction_prep = state_prep.check_state_prep()
        state_prep.add_to_query_prep(state_prep.under_construction_prep, node.orth_)
        
        # POS
        state_pos.check_pos_end(node) 
        state_pos.under_construction_pos = state_pos.check_state_pos()
        state_pos.add_to_query_pos_end(state_pos.under_construction_pos,node,1)
        state_pos.check_pos_in_dicts(node)
        state_pos.under_construction_pos = state_pos.check_state_pos()
        state_pos.add_to_query_pos(state_pos.under_construction_pos,node)
        

        # WH 
        state_wh.check_wh_end(node.orth_)
        state_wh.found_wh_verb(node.orth_)
        state_wh.under_construction_wh = state_wh.check_state_wh()
        under_construction_others, wh_type = check_state_all() # check if valid end
        state_wh.add_to_query_wh_end((under_construction_others and not wh_type), node.orth_, 1)
        state_wh.add_to_query_wh(state_wh.under_construction_wh, node.orth_)

        #WHEN
        state_when.check_when_end(node.orth_)
        state_when.found_when_verb(node.orth_)
        state_when.under_construction_when = state_when.check_state_when()
        under_construction_others, wh_type = check_state_all() # check if valid end
        state_when.add_to_query_when_end((under_construction_others and wh_type), node.orth_, 1)
        state_when.add_to_query_when(state_when.under_construction_when, node.orth_)
        

        # print_states_prep()
        # print_states_pos()
        # print_states_wh()

        
        [tree_creator(child, node) for child in node.rights]

        # POSTORDER DETECTION

    else:

        # print("current node " +str(node))

        # PREP
        # check_prep_end(node) #preorder detection
        state_prep.check_prep_in_dicts(node.orth_)  #preorder detection
        state_prep.found_prep_end(node.orth_) #inorder end
        state_prep.under_construction_prep = state_prep.check_state_prep()
        state_prep.add_to_query_prep_end(state_prep.under_construction_prep, node.orth_, 1)
        state_prep.add_to_query_prep(state_prep.under_construction_prep, node.orth_)

        # POS
        state_pos.check_pos_end(node)
        state_pos.under_construction_pos = state_pos.check_state_pos()
        state_pos.add_to_query_pos_end(state_pos.under_construction_pos, node, 1)
        state_pos.check_pos_in_dicts(node)
        state_pos.under_construction_pos = state_pos.check_state_pos()
        state_pos.add_to_query_pos(state_pos.under_construction_pos, node)

        # WH
        state_wh.check_wh_end(node.orth_)
        state_wh.under_construction_wh = state_wh.check_state_wh()
        under_construction_others, wh_type = check_state_all() # check if valid end
        state_wh.add_to_query_wh_end((under_construction_others and not wh_type), node.orth_, 0)
        state_wh.add_to_query_wh(state_wh.under_construction_wh, node.orth_)
        
        #WHEN
        state_when.check_when_end(node.orth_)
        state_when.under_construction_when = state_when.check_state_when()
        under_construction_others, wh_type = check_state_all() # check if valid end
        state_when.add_to_query_when_end((under_construction_others and wh_type), node.orth_, 0)
        state_when.add_to_query_when(state_when.under_construction_when, node.orth_)
        
        # print_states_prep()
        # print_states_pos()
        # print_states_wh()
        

# -------------------------------------------------------------------------------------------------------