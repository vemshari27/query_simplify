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

from .syntaxAnalyzerPos import *
from .syntaxAnalyzerPrep import *
from .syntaxAnalyzerWh import *
from .syntaxAnalyzerWhen import *


class Syntax_Analyzer:
    def __init__(self):
        self.when = Syntax_Analyzer_WHEN()
        self.wh = Syntax_Analyzer_WH()
        self.pos = Syntax_Analyzer_POS()
        self.prep = Syntax_Analyzer_PREP()

        self.pos_queries = []
        self.prep_queries = []
        self.when_queries = []
        self.wh_queries = []

    def syntax_analyzer_preorder(self, node, parent):
        result_WHEN = self.when.syntax_analyzer_when_noun(node, parent)
        result_WH = self.wh.syntax_analyzer_wh_noun(node, parent)

    def syntax_analyzer_inorder(self, node, parent):
        result_PREP = self.prep.syntax_analyzer_prep_detect(node, parent)
        result_WHEN = self.when.syntax_analyzer_when_detect(node, parent)
        result_WH = self.wh.syntax_analyzer_wh_detect(node, parent)
        result_WHEN = self.when.syntax_analyzer_when_verb(node, parent)
        result_WH = self.wh.syntax_analyzer_wh_verb(node, parent)

    def syntax_analyzer_postorder(self, node, parent):
        result_POS = self.pos.syntax_analyzer_pos_detect(node, parent)
        result_PREP = self.prep.syntax_analyzer_prep_noun_start(node, parent)
        result_PREP = self.prep.syntax_analyzer_prep_noun_end(node, parent)

    def print_syntax_analyzer(self):
        print("\nprinting pos")
        self.pos.print_all_POS()

        print("\nprinting prep")
        self.prep.print_all_PREP()

        print("\nprinting when")
        self.when.print_all_WHEN()

        print("\nprinting wh")
        self.wh.print_all_WH()

    def add_prep_subquery(self, list):
        subquery = []
        for i in range(len(list)):
            subquery.append(list[i])
        self.prep_queries.append(subquery)

    def add_pos_subquery(self, list):
        subquery = []
        for i in range(len(list)):
            subquery.append(list[i])
        self.pos_queries.append(subquery)

    def add_when_subquery(self, list):
        subquery = []
        for i in range(len(list)):
            subquery.append(list[i])
        self.when_queries.append(subquery)

    def add_wh_subquery(self, list):
        subquery = []
        for i in range(len(list)):
            subquery.append(list[i])
        self.wh_queries.append(subquery)

    def print_subqueries(self):
        print("\nprinting pos")
        print(self.pos_queries)

        print("\nprinting prep")
        print(self.prep_queries)

        print("\nprinting when")
        print(self.when_queries)

        print("\nprinting wh")
        print(self.wh_queries)

    def get_prep_queries(self):
        return self.prep_queries

    def get_pos_queries(self):
        return self.pos_queries

    def get_wh_queries(self):
        return self.wh_queries

    def get_when_queries(self):
        return self.when_queries

    def clear_all(self):
        self.pos_queries.clear()
        self.prep_queries.clear()
        self.when_queries.clear()
        self.wh_queries.clear()

        self.pos.clear_queries()
        self.prep.clear_queries()
        self.wh.clear_queries()
        self.when.clear_queries()
