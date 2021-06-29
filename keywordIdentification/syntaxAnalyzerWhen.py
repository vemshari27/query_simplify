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

class Syntax_Analyzer_WHEN:
    def __init__(self):
        self.encountered_WHEN = 0
        self.when_found = 0
        # self.noun_found = 0
        self.verb_found = 0
        # self.noun_string = ""
        self.verb_string = ""
        self.dict = {}
        self.exceptions = ["did", "do"]

    def syntax_analyzer_when_detect(self, node, parent):  # inorder detection
        if(node.tag_[0] == 'W' and (node.orth_ == "When" or node.orth_ == "when")):
            if(parent.tag_[0] == 'V' and parent.orth_ not in self.exceptions):
                self.verb_found = 1
                self.verb_string = parent.orth_ + "_" + str(parent.i)
            self.when_found = 1
            return 0

        else:
            return -1

    def syntax_analyzer_when_verb(self, node, parent):  # inorder detection
        if(self.when_found == 1 and self.verb_found == 0):
            if(node.tag_[0] == 'V'):
                if(node.orth_ not in self.exceptions):
                    self.verb_found = 1
                    self.verb_string = node.orth_ + "_" + str(node.i)
                    return 0
                else:
                    if(parent.tag_[0] == 'V'):
                        self.verb_found = 1
                        self.verb_string = parent.orth_ + \
                            "_" + str(parent.i)
                        return 0
                    else:
                        return -1
        return -1

    def syntax_analyzer_when_noun(self, node, parent):  # preorder detection
        if(self.when_found == 1 and self.verb_found == 1):
            if(node.tag_[0] == 'N'):
                if(parent.tag_[0] == 'V'):
                    self.when_found = 0
                    self.verb_found = 0
                    n = node.orth_ + "_" + str(node.i)
                    self.dict_update(self.verb_string, n)
                    return 1
                else:
                    self.when_found = 0
                    self.verb_found = 0
                    n = node.orth_ + "_" + str(node.i)
                    self.dict_update(self.verb_string, n)
                    return 2
        return -1

    def in_WHEN(self, node):
        return self.dict.get(node, None)

    def dict_update(self, key, node):
        if(key in self.dict.keys()):
            list = self.dict.get(key)
            list.append(node)
            self.dict.update({key: list})
        else:
            self.dict.update({key: [node]})

    def print_all_WHEN(self):
        for x in self.dict.keys():
            print(x)
            print(self.dict[x])

    def clear_queries(self):
        self.encountered_WHEN = 0
        self.when_found = 0
        # self.noun_found = 0
        self.verb_found = 0
        # self.noun_string = ""
        self.verb_string = ""
        self.dict.clear()
