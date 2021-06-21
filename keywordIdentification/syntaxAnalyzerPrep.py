class Syntax_Analyzer_PREP:
    def __init__(self):
        self.encountered_IN = 0
        self.noun_end = 0
        self.end_string = ""
        self.dict = {}
        self.exceptions = ["at"]

    # inorder detection and parent store
    def syntax_analyzer_prep_detect(self, node, parent):
        if("IN" == node.tag_ and node.orth_ not in self.exceptions):
            self.encountered_IN += 1
            return self.encountered_IN
        else:
            return -1

    # postorder detection
    def syntax_analyzer_prep_noun_start(self, node, parent):

        if(self.encountered_IN > 0 and self.noun_end == 1):

            if(node.tag_[0] == 'N'):
                n = node.orth_ + "_" + str(node.i)
                self.dict_update(n, self.end_string)
                self.encountered_IN -= 1
                self.noun_end = 0
                return 1

            elif(node.tag_ == "IN" and parent.tag_[0] == 'N'):
                p = parent.orth_ + "_" + str(parent.i)
                self.dict_update(p, self.end_string)
                self.encountered_IN -= 1
                self.noun_end = 0
                return 1

        else:
            return -1

    def syntax_analyzer_prep_noun_end(self, node, parent):  # post detection
        if("IN" != node.tag_ and self.encountered_IN > 0 and self.noun_end == 0):
            if((node.tag_[0] == 'N' or node.tag_ == "CD") and parent.tag_ == "IN"):
                self.noun_end = 1
                self.end_string = node.orth_ + "_" + str(node.i)
                return 1

        else:
            return -1

    def in_PREP(self, key):
        return self.dict.get(key, None)

    def dict_update(self, key, node):
        if(key in self.dict.keys()):
            list = self.dict.get(key)
            list.append(node)
            self.dict.update({key: list})
        else:
            self.dict.update({key: [node]})

    def print_all_PREP(self):
        for x in self.dict.keys():
            print(x)
            print(self.dict[x])

    def clear_queries(self):
        self.encountered_IN = 0
        self.noun_end = 0
        self.end_string = ""
        self.dict.clear()
