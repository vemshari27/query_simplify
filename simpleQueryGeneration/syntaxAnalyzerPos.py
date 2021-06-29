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

class State_POS:
    def __init__(self):
        self.noun1 = 0
        self.noun2 = 0
        self.list_pos_noun1 = []
        self.list_pos_noun2 = []
        self.pos_query = []
        self.pos_end = ""
        self.under_construction_pos = -1

    # calculate state of prep
    def check_state_pos(self):
        if(self.noun1 == 0 and self.noun2 == 0):
            return -1
        elif(self.noun1 == 1 and self.noun2 == 0):
            return 0
        elif(self.noun1 == 1 and self.noun2 == 1):
            return 1
        else:
            return -1

    def add_to_query_pos_end(self, state, node, add_insert, syntax_analyzer):
        if(state == 1):
            # print("completed")
            if(add_insert == 1):
                self.pos_query.append(node.orth_ + "_" + str(node.i))
            # print(pos_query)

            syntax_analyzer.add_pos_subquery(self.pos_query)
            self.pos_query.clear()
            self.noun2 = 0
            self.noun1 = 0

    def add_to_query_pos(self, state, node):
        if(state == 0):
            self.pos_query.append(node.orth_ + "_" + str(node.i))

    def print_states_pos(self):
        print(str(self.noun1) + "  " + str(self.noun2))

    def clear_pos(self):
        # state
        self.noun1 = 0
        self.noun2 = 0
        self.list_pos_noun1.clear()
        self.list_pos_noun2.clear()
        self.pos_query.clear()
        self.pos_end = ""
        self.under_construction_pos = -1

    def add_left_children(self, node):
        p_query = []
        [self.iterate_left(child, p_query) for child in node.lefts]

    def iterate_left(self, node, p_query):
        if node.n_lefts + node.n_rights > 0:
            [self.iterate_left(child, p_query) for child in node.lefts]
            self.pos_query.append(node.orth_ + "_" + str(node.i))
            [self.iterate_left(child, p_query) for child in node.rights]
        else:
            self.pos_query.append(node.orth_ + "_" + str(node.i))

    # ---------------------------------------------------------------------------------------------------
    # GENERATING POSSESSIVE ENDING QUERIES

    # checking inorder for noun in pos dictionary
    def check_pos_in_dicts(self, node, syntax_analyzer):
        n = node.orth_ + "_" + str(node.i)
        # print("check pos end with " + str(n))

        list_pos = syntax_analyzer.pos.in_POS(n)
        if(list_pos != None):
            self.noun1 = 1
            if(self.pos_end == n):  # connected POS
                # print("directly connected")
                self.pos_query.append("-")
            else:  # unconnected,noun addons, added beginning
                # print("not connected")
                self.add_left_children(node)
            self.pos_end = str(list_pos[0])
            # print("found valid begin " + str(node))

    def check_pos_end(self, node):  # checking inorder if end of the query is found
        n = node.orth_ + "_" + str(node.i)
        # print("check pos end with " + str(n))

        if(n == self.pos_end):
            # print("found valid end " + str(n))
            self.noun2 = 1
        return
