from .queryTree import QueryNode, QueryTree, print_qt
import logging
logging.basicConfig(filename='../app.log', filemode='a+',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# positions to break on when exiting a nested prepositions
breakpoints = ["WDT", "WP", "WP$", "WRB", "NN",
               "NNP", "NNS", "NNPS", "JJ", "JJR", "JJS"]


def tree_constructor(sentence, pos_qs, prep_qs, when_qs, wh_qs):
    # initialize
    main_qt = QueryTree()
    pos_qt = QueryTree()

    prefixes = []
    prev_word = ''

    type_array = [{"sub_queries": pos_qs}, {"sub_queries": prep_qs}, {
        "sub_queries": when_qs}, {"sub_queries": wh_qs}]

    analyzer_content = []
    curr_index = []

    for i in range(len(type_array)):
        dict = {'index': -1, 'word': [], 'endpoint': []}
        analyzer_content.append(dict)
        curr_index.append(0)

    for i in range(4):
        for k in type_array[i]["sub_queries"]:
            for j in k:
                analyzer_content[i]["word"].append(j)
            analyzer_content[i]["endpoint"].append(
                len(analyzer_content[i]["word"])-1)
        if len(analyzer_content[i]['word']) > 0:
            analyzer_content[i]["index"] = 0

    # print(analyzer_content)

    # initialize the query trees
    curr_node = main_qt
    curr_pos_node = pos_qt

    # encountered pos -1 not init, 0 began pos, 1 nested pos found, 2 nested pos end reached
    encountered_pos = -1
    # currently active analyzer
    analyzer = -1
    # previously active analyzer
    prev_analyzer = 1000
    # has reached a new subquery in highest priority analyzer
    reached_next = -1
    # previous state of reached next
    prev_reached_next = -1

    curr_query_node = QueryNode()

    for token in sentence[0:]:
        # print(" ")
        # print("Working on token: ", token)

        analyzer, encountered_pos, reached_next = identify_current_analyzer(
            token, analyzer_content, curr_index, encountered_pos)

        # Found a stronger active analyzer
        if(analyzer < prev_analyzer):
            # print("Found a stronger analyzer")
            if(analyzer != 0):
                # print("Not a pos analyzer")
                if(prev_analyzer == 1000):
                    # print("Beginning")
                    curr_node.add_right_child(QueryNode())
                    curr_node.add_to_curr_node(token)
                    # print(curr_node.node)
                else:
                    # print("Not Beginning")
                    curr_node = curr_node.add_right_child(QueryNode())
                    curr_node.add_to_curr_node(token)
                    # print(curr_node.node)

            else:
                # print("Is a pos analyzer")
                # print("Found a stronger active pos analyzer")
                curr_pos_node.add_right_child(QueryNode())
                curr_pos_node.add_to_curr_node(token)
                # print(curr_pos_node.node)

        elif(analyzer == prev_analyzer):
            # print("Found an equivalent analyzer")
            if(analyzer != 0):
                # print("Not a pos analyzer")
                # Found a equivanlent active analyzer with new subquery beginning
                if(prev_reached_next == 1):
                    # print("Beginning")
                    curr_node = curr_node.add_right_child(QueryNode())
                    curr_node.add_to_curr_node(token)
                    # print(curr_node.node)
                 # Adding remaining to current active analyzer
                else:
                    # print("Not Beginning")
                    curr_node.add_to_curr_node(token)
                    # print(curr_node.node)
            else:
                # print("Is a pos analyzer")
                if(prev_reached_next == -1):
                    # print("Adding to current pos tree")
                    curr_pos_node.add_to_curr_node(token)
                    # print(curr_pos_node.node)

                elif(prev_reached_next == 1):
                    # print("Adding to current pos tree's parent")
                    temp_node = QueryTree()
                    temp_node.add_right_child(QueryNode())
                    temp_node.add_left_tree(curr_pos_node)
                    # print(temp_node.node)
                    temp_node.add_to_curr_node(token)
                    curr_pos_node = temp_node
                    # print(curr_pos_node.node)

                elif(prev_reached_next == 2):
                    # print("adding to pos and creating new node")
                    curr_node.add_left_tree(curr_pos_node)
                    curr_pos_node = QueryTree()
                    curr_pos_node.add_right_child(QueryNode())
                    curr_node.add_to_curr_node(token)
                    # print(curr_node.node)
                    # curr_node.add_to_curr_node(token)

        # Found a weaker active analyzer with the current nested pos analyzer ending
        elif(analyzer > prev_analyzer):
            # print("Found a weaker analyzer")
            if(prev_analyzer == 0):
                # print("Nested pos analyzer ending in previous iter")
                if(curr_node.node == None):
                    curr_node.node = QueryNode()
                curr_node.add_left_tree(curr_pos_node)
                curr_pos_node = QueryTree()
                curr_pos_node.add_right_child(QueryNode())

                # print(curr_node.left_child.node)

                if(token.tag_ in breakpoints):
                    # print("Found a Breaking token")
                    curr_node = curr_node.add_right_child(QueryNode())
                    curr_node.add_to_curr_node(token)
                else:
                    # print("Not a Breaking token")
                    curr_node.add_to_curr_node(token)

                # print(curr_node.node)

                # curr_node = curr_node.add_left_tree(curr_pos_qt)
            elif(prev_analyzer != 0 and prev_reached_next == 1):
                # print("Active analyzer starting anew")
                curr_node = curr_node.add_right_child(QueryNode())
                curr_node.add_to_curr_node(token)
                # print(curr_node.node)

        # Adding remaing to current
        if(encountered_pos == 2):
            # print("Found end of nested pos resetting")
            encountered_pos = -1

        # print(analyzer, prev_analyzer, encountered_pos, token,reached_next, prev_reached_next)

        prev_reached_next = reached_next
        prev_analyzer = analyzer

    # exited with nested preposition ending
    if(analyzer == 0):
        curr_node.add_left_tree(curr_pos_node)

    if(curr_node.is_empty == True):
        return curr_pos_node

    return main_qt


def identify_current_analyzer(token, analyzer_content, curr_index, encountered_nested_pos):
    # print("identifying current analyzer ", token)
    n = token.orth_ + "_" + str(token.i)
    # print(n)
    first_found = -1
    reached_next = -1
    for i in range(len(analyzer_content)):
        if(analyzer_content[i]["index"] != -1):
            if(first_found == -1):
                # print("current index : ", i, curr_index[i])
                if(encountered_nested_pos == 0):
                    # print("Continuing on nested pos")
                    first_found = i
                    if(curr_index[i] in analyzer_content[i]["endpoint"]):
                        # print("Intermediate end")
                        reached_next = 1
                        encountered_nested_pos = 1
                        if(curr_index[i]+1 < len(analyzer_content[i]["word"])):
                            if(analyzer_content[i]["word"][curr_index[i]+1] != "-"):
                                # print("Endpoint reached on nested pos")
                                encountered_nested_pos = 2  # nested pos end
                                reached_next = 2
                        else:
                            # print("Endpoint reached on nested pos")
                            encountered_nested_pos = 2  # nested pos end
                            reached_next = 2

                    curr_index[i] += 1

                # checking if the words match
                elif(curr_index[i] < len(analyzer_content[i]["word"])):
                    if(analyzer_content[i]["word"][curr_index[i]] == n):
                        # print("Continuing on normal")
                        if(curr_index[i] in analyzer_content[i]["endpoint"]):
                            # print("Reached next")
                            reached_next = 1
                        curr_index[i] += 1
                        first_found = i

                    # checking if nested pos
                    elif(analyzer_content[i]["word"][curr_index[i]] == "-"):
                        # print("Found a nested pos delimiter")
                        curr_index[i] += 3
                        first_found = i
                        encountered_nested_pos = 0
                        # reached_next = 1
            else:
                if(curr_index[i] < len(analyzer_content[i]["word"])):
                    if(analyzer_content[i]["word"][curr_index[i]] == n):
                        curr_index[i] += 1

    return first_found, encountered_nested_pos, reached_next


if __name__ == "__main__":
    en = spacy.load('en')
    text = "who is the president of usa"
    doc = en(text)

    # pos_qs = []
    # prep_qs = [['the', 'birthday', 'of'], ['the', 'wife', 'of'], ['president', 'of', 'usa']]
    # wh_qs = [['what', 'is', 'the', 'birthday', 'of', 'the', 'wife', 'of', 'president', 'of', 'usa']]
    # when_qs =[]

    pos_qs = []
    prep_qs = [['the', 'president', 'of', 'usa']]
    wh_qs = [['who', 'is', 'the', 'president', 'of', 'usa']]
    when_qs = []

    tree_construction(doc, pos_qs, prep_qs, wh_qs, when_qs)
