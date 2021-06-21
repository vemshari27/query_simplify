from .syntaxAnalyzerPos import *
from .syntaxAnalyzerPrep import *
from .syntaxAnalyzerWh import *
from .syntaxAnalyzerWhen import *

# ---------------------------------------OVERLAPPING WH/WHEN-------------------------------------------------
prev_state = -1
# check if all analyzers are sleeping


def check_state_all():
    global prev_state
    if(prev_state == 1):
        if(state_when.check_state_when() == 2 and state_wh.check_state_wh() != -1):
            # print("When followed by Wh")
            prev_state = 0
            state_when.set_verb_noun(0, 0)
            return [1, 1, 0]
        elif(state_wh.check_state_wh() == 2 and state_when.check_state_when() != -1):
            # print("Wh followed by When")
            prev_state = 0
            state_wh.set_verb_noun(0, 0)
            return [1, 0, 0]
        elif(state_wh.check_state_wh() == 0 and state_when.check_state_when() == -1):
            # print("Wh followed by Wh")
            prev_state = 0
            state_wh.set_verb_noun(1, 0)
            return [1, 0, 1]
        else:
            return [0, 0, 1]
    return [0, 0, 1]
    # if(state_when.check_state_when() == 2 and state_wh.check_state_wh() == 0 and state_wh.check_state_wh_noun() == 1 and prev_state == 1):

    #     prev_state = 0
    #     return [1, 1]

    # elif((state_when.check_state_when() == 0 or state_wh.check_state_wh() == 0) and prev_state == 1):
    #     prev_state = 0
    #     # when followed by wh
    #     if(state_when.check_state_when() == 2):
    #         return [1, 1]
    #     # wh followed by wh
    #     elif(state_wh.check_state_wh() == 0):
    #         return [1, 0]
    #     # wh followed by when
    #     elif(state_wh.check_state_wh() == 2):
    #         return [1, 0]

    # else:
    #     return [0, 0]


# ------------------------------------------------------------------------------------------------------------
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
    prev_state = -1

# CODE FOR USING DICTIONARIES AND DEPENDENCY TREE TO CREATE SUBQUERIES


def simple_query_generator(doc, syntax_analyzer):
    # prep.clean_dict()

    [simple_query_creator(sent.root, None, syntax_analyzer)
     for sent in doc.sents]
    if(state_wh.wh_query != []):
        syntax_analyzer.add_wh_subquery(state_wh.wh_query)
    if(state_when.when_query != []):
        syntax_analyzer.add_when_subquery(state_when.when_query)
    # if(state_prep.prep_query != []):
    #     prep.add_subquery(state_prep.prep_query)
    # if(state_pos.pos_query != []):
    #     pos.add_subquery(state_pos.pos_query)

    clear_all()
    return


def simple_query_creator(node, parent, syntax_analyzer):
    global prev_state
    if node.n_lefts + node.n_rights > 0:
        # print(node.orth_)

        # PREORDER CONSTRUCTION

        # PREP
        state_prep.check_prep_in_dicts(node, syntax_analyzer)
        state_prep.under_construction_prep = state_prep.check_state_prep()
        state_prep.add_to_query_prep_end(
            state_prep.under_construction_prep, node, 0, syntax_analyzer)

        # POS

        # WH
        state_wh.check_wh_in_dicts(node, syntax_analyzer)

        # WHEN
        state_when.check_when_in_dicts(node, syntax_analyzer)

        [simple_query_creator(child, node, syntax_analyzer)
         for child in node.lefts]

        # INORDER CONSTRUCTION

        # PREP
        state_prep.found_prep_end(node, syntax_analyzer)  # inorder end
        state_prep.under_construction_prep = state_prep.check_state_prep()
        state_prep.add_to_query_prep(
            state_prep.under_construction_prep, node)

        # POS
        state_pos.check_pos_end(node)
        state_pos.under_construction_pos = state_pos.check_state_pos()
        state_pos.add_to_query_pos_end(
            state_pos.under_construction_pos, node, 1, syntax_analyzer)
        state_pos.check_pos_in_dicts(node, syntax_analyzer)
        state_pos.under_construction_pos = state_pos.check_state_pos()
        state_pos.add_to_query_pos(state_pos.under_construction_pos, node)

        # WH
        if(state_wh.check_wh_end(node) == 1):
            prev_state = 1
        if(state_wh.found_wh_verb(node) == 1):
            prev_state = 1
        state_wh.under_construction_wh = state_wh.check_state_wh()
        under_construction_others, wh_type, execute = check_state_all()  # check if valid end

        state_wh.add_to_query_wh_end(
            (under_construction_others and not wh_type), node, 1, syntax_analyzer)
        if(execute == 1):
            state_wh.add_to_query_wh(state_wh.under_construction_wh, node)

        # WHEN
        if(state_when.check_when_end(node) == 1):
            prev_state = 1
        if(state_when.found_when_verb(node) == 1):
            prev_state = 1
        state_when.under_construction_when = state_when.check_state_when()
        under_construction_others, wh_type, execute = check_state_all()  # check if valid end

        state_when.add_to_query_when_end(
            (under_construction_others and wh_type), node, 1, syntax_analyzer)
        if(execute == 1):
            state_when.add_to_query_when(
                state_when.under_construction_when, node)

        # state_wh.print_states_wh()
        # state_when.print_states_when()

        [simple_query_creator(child, node, syntax_analyzer)
         for child in node.rights]

        # POSTORDER CONSTRUCTION

    else:
        # print(node.orth_)

        # PREP
        # check_prep_end(node) #preorder detection
        state_prep.check_prep_in_dicts(
            node, syntax_analyzer)  # preorder detection
        state_prep.found_prep_end(node, syntax_analyzer)  # inorder end
        state_prep.under_construction_prep = state_prep.check_state_prep()
        state_prep.add_to_query_prep_end(
            state_prep.under_construction_prep, node, 1, syntax_analyzer)
        state_prep.add_to_query_prep(
            state_prep.under_construction_prep, node)

        # POS
        state_pos.check_pos_end(node)
        state_pos.under_construction_pos = state_pos.check_state_pos()
        state_pos.add_to_query_pos_end(
            state_pos.under_construction_pos, node, 1, syntax_analyzer)
        state_pos.check_pos_in_dicts(node, syntax_analyzer)
        state_pos.under_construction_pos = state_pos.check_state_pos()
        state_pos.add_to_query_pos(state_pos.under_construction_pos, node)

        # WH
        if(state_wh.check_wh_end(node) == 1):
            prev_state = 1
        state_wh.under_construction_wh = state_wh.check_state_wh()
        under_construction_others, wh_type, execute = check_state_all()  # check if valid end

        state_wh.add_to_query_wh_end(
            (under_construction_others and not wh_type), node, 0, syntax_analyzer)
        if(execute == 1):
            state_wh.add_to_query_wh(state_wh.under_construction_wh, node)

        # WHEN
        if(state_when.check_when_end(node) == 1):
            prev_state = 1
        state_when.under_construction_when = state_when.check_state_when()
        under_construction_others, wh_type, execute = check_state_all()  # check if valid end

        state_when.add_to_query_when_end(
            (under_construction_others and wh_type), node, 0, syntax_analyzer)
        if(execute == 1):
            state_when.add_to_query_when(
                state_when.under_construction_when, node)

        # state_wh.print_states_wh()
        # state_when.print_states_when()
