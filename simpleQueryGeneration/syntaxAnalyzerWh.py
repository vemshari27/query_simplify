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
        self.wh_verb = ""
        self.under_construction_wh = -1

    # calculate state of wh
    def check_state_wh(self):
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

    def check_state_wh_noun(self):
        if(self.noun == 1):
            return 1

    def add_to_query_wh_end(self, state, node, add_insert, syntax_analyzer):
        if(state == 1):
            # print("completed wh " + str(node))
            if(add_insert == 1):
                self.wh_query.append(node.orth_ + "_" + str(node.i))
            # print(self.wh_query)

            syntax_analyzer.add_wh_subquery(self.wh_query)
            self.wh_query.clear()

    def add_to_query_wh(self, state, node):
        if(state == 0 or state == 1 or state == 2):
            # print("underconstruction wh " + str(node))
            self.wh_query.append(node.orth_ + "_" + str(node.i))
            # print(self.wh_query)

    def print_states_wh(self):
        print("WH : " + str(self.verb) + "  " + str(self.noun))

    def set_verb_noun(self, verb, noun):
        self.verb = verb
        self.noun = noun

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
        self.wh_verb = ""
        self.under_construction_wh = -1

    # ---------------------------------------------------------------------------------------------------
    # GENERATING WH WORD QUERIES

    # checking preorder for verb in wh dictionary
    def check_wh_in_dicts(self, node, syntax_analyzer):
        n = node.orth_ + "_" + str(node.i)
        # print("check wh start with " + str(n))

        list_wh = syntax_analyzer.wh.in_WH(n)
        # print(list_wh)

        if(list_wh != None):
            self.verb = 1
            self.noun = 0
            self.wh_end = str(list_wh[0])
            self.wh_verb = n
            # print("found valid begin wh " + str(n))

    def check_wh_end(self, node):  # checking inorder if end of the query is found
        # global prev_state
        n = node.orth_ + "_" + str(node.i)
        # print("check wh end with " + str(n))

        if(n == self.wh_end):
            # print("found valid end wh " + str(n))
            self.noun = 1
            if(self.verb == 2):
                # prev_state = 1
                return 1
        return 0  # conditional

    def found_wh_verb(self, node):  # inorder confirmation the verb has been covered
        # global prev_state
        n = node.orth_ + "_" + str(node.i)
        # print(str(n) + " " + self.wh_end)
        if(n == self.wh_verb):
            self.verb = 2
            if(self.noun == 1):
                # prev_state = 1
                # print("covered " + str(self.verb) + " " + str(self.noun))
                return 1

        return 0  # conditional
