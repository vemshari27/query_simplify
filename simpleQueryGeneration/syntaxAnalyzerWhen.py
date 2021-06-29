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
        self.when_verb = ""
        self.under_construction_when = -1

    # calculate state of prep
    def check_state_when(self):
        if(self.verb == 0 and self.noun == 0):  # not started
            return -1
        elif(self.verb == 1 and self.noun == 0):  # started verb
            return 0
        elif(self.verb == 0 and self.noun == 1):  # added noun
            return 0
        elif(self.verb == 1 and self.noun == 1):  # added noun started verb
            return 1
        elif(self.verb == 2 and self.noun == 0):  # added verb
            return 1
        elif(self.verb == 2 and self.noun == 1):  # completed adding all
            return 2

    def add_to_query_when_end(self, state, node, add_insert, syntax_analyzer):
        if(state == 1):
            # print("completed when " + str(node))
            if(add_insert == 1):
                self.when_query.append(node.orth_ + "_" + str(node.i))
            # print(self.when_query)

            syntax_analyzer.add_when_subquery(self.when_query)
            self.when_query.clear()

    def add_to_query_when(self, state, node):
        if(state == 0 or state == 1 or state == 2):
            # print("underconstruction when " + str(node))
            self.when_query.append(node.orth_ + "_" + str(node.i))
            # print(self.when_query)

    def print_states_when(self):
        print("WHEN : " + str(self.verb) + "  " + str(self.noun))

    def set_verb_noun(self, verb, noun):
        self.verb = verb
        self.noun = noun

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
        self.when_verb = ""
        self.under_construction_when = -1

    # ---------------------------------------------------------------------------------------------------
    # GENERATING WHEN WORD QUERIES

    # checking preorder for verb in when dictionary
    def check_when_in_dicts(self, node, syntax_analyzer):
        n = node.orth_ + "_" + str(node.i)
        # print("check when start with " + str(n))

        list_when = syntax_analyzer.when.in_WHEN(n)
        # print(list_when)

        if(list_when != None):
            self.verb = 1
            self.noun = 0
            self.when_end = list_when[0]
            self.when_verb = n
            # print("found valid begin when " + str(node))
        return

    def check_when_end(self, node):  # checking inorder if end of the query is found
        # global prev_state
        n = node.orth_ + "_" + str(node.i)
        # print("check when end with " + str(n))

        if(n == self.when_end):
            # print("found valid end when " + str(node))
            self.noun = 1
            if(self.verb == 2):
                # prev_state = 1
                return 1
        return 0

    def found_when_verb(self, node):  # inorder confirmation the verb has been covered
        # global prev_state
        n = node.orth_ + "_" + str(node.i)
        # print(str(node) + " " + self.when_end)
        if(n == self.when_verb):
            self.verb = 2
            if(self.noun == 1):
                #   prev_state = 1
                # print("covered " + str(self.verb) +
                #   " " + str(self.noun))
                return 1
        return 0
