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
    def check_state_prep(self):
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

    def add_to_query_prep_end(self, state, node, add_insert, syntax_analyzer):
        if(state == 1):
            # print("completed")
            if(add_insert == 1):
                self.prep_query.append(node.orth_ + "_" + str(node.i))
            # print(prep_query)
            syntax_analyzer.add_prep_subquery(self.prep_query)
            self.prep_query.clear()
            self.noun2 = 0

    def add_to_query_prep(self, state, node):
        if(state == 0):
            # print("underconstruction")
            self.prep_query.append(node.orth_ + "_" + str(node.i))

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

    # checking preorder for noun in prep dictionary
    def check_prep_in_dicts(self, node, syntax_analyzer):
        n = node.orth_ + "_" + str(node.i)
        # print("check prep start with " + str(n))

        list_prep = syntax_analyzer.prep.in_PREP(n)

        if(list_prep != None):
            self.noun1 += 1
            self.check_prep_end(node)
            self.prep_end = list_prep[0]
            # print("found valid begin " + str(node))

        self.check_prep_end(node)

    def check_prep_end(self, node):  # checking preorder if end of the query is found
        n = node.orth_ + "_" + str(node.i)
        # print("check prep end with " + str(n))

        if(n == self.prep_end):
            # print("found valid end " + str(node))

            # print("list end " + str(n))
            self.noun2 = 1
            self.noun1 -= 1
        return

    def found_prep_end(self, node, syntax_analyzer):  # finding inorder the end of prep
        n = node.orth_ + "_" + str(node.i)
        # print("node in inorder search " + str(n) + " " + str(self.prep_end))
        if(n == self.prep_end):
            # print("found prep end " + str(node))
            # OPERATION PREP
            self.add_to_query_prep_end(1, node, 1, syntax_analyzer)
        return
