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

class Syntax_Analyzer_POS:
    def __init__(self):
        self.encountered_POS = 0
        self.dict = {}

    # In post order - Check if POS tag has the parent as a noun.
    def syntax_analyzer_pos_detect(self, node, parent):
        if("POS" == node.tag_):
            self.encountered_POS += 1
            return 0

        elif("POS" != node.tag_ and self.encountered_POS > 0):
            if(node.tag_[0] == 'N'):
                n = node.orth_ + "_" + str(node.i)
                p = parent.orth_ + "_" + str(parent.i)
                self.encountered_POS -= 1
                self.dict_update(n, p)
                return 1
        else:
            # logging.warning("Pos Not Detected")
            return -1

    def in_POS(self, node):
        return self.dict.get(node, None)

    def dict_update(self, key, node):
        if(key in self.dict.keys()):
            list = self.dict.get(key)
            list.append(node)
            self.dict.update({key: list})
        else:
            self.dict.update({key: [node]})

        # logging.info("Pos Dict Updated")

    def print_all_POS(self):
        for x in self.dict.keys():
            print(x)
            print(self.dict[x])

    def clear_queries(self):
        self.encountered_POS = 0
        self.dict.clear()
