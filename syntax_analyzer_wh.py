# the president of the United States

exceptions = ["did", "do"]

class Syntax_Analyzer_WHEN:
    def __init__(self):
        self.encountered_WHEN = 0
        self.when_found = 0
        # self.noun_found = 0
        self.verb_found = 0
        # self.noun_string = ""
        self.verb_string = ""
        self.dict = {}
        self.when_queries = []



    def syntax_analyzer_when_detect(self, tag, node, parent): # inorder detection
        if(tag[0] == 'W' and (node == "When" or node == "when")):
            # print("When encountered  " + str(node))
            if(parent.tag_[0] == 'V' and parent.orth_ not in exceptions):
                # print("Verb encountered  " + str(parent))
                self.verb_found = 1
                self.verb_string = parent.orth_
            self.when_found = 1
            return 0

    
    def syntax_analyzer_when_verb(self, tag, node, parent): #inorder detection
        if(self.when_found == 1 and self.verb_found == 0):
            if(tag[0] == 'V'):
                if(node not in exceptions) :
                    # print("Verb encountered  " + str(node))
                    self.verb_found = 1
                    self.verb_string = node
                    return 0
                else :
                    if(parent.tag_[0] == 'V'):
                        self.verb_found = 1
                        self.verb_string = parent.orth_


    def syntax_analyzer_when_noun(self, tag, node, parent): #preorder detection
        if(self.when_found == 1 and self.verb_found == 1):
            if(tag[0] == 'N'):
                if(parent.tag_[0] == 'V'):
                    # print("encountered Noun for WHEN " + str(node) + " and VERB " + str(parent.orth_)) # parent of noun is the verb
                    self.when_found = 0
                    self.verb_found = 0
                    self.dict_update(self.verb_string, node)
                    return 1
                else :
                    self.when_found = 0
                    self.verb_found = 0
                    self.dict_update(self.verb_string, node)
                    return 1
        return 0

    def in_WHEN(self,node):
        return self.dict.get(node, None)

    def add_subquery(self,list):
        subquery = []
        if(len(list) <= 1):
            return
        for i in range(len(list)):
            subquery.append(list[i])
        self.when_queries.append(subquery)

    def dict_update(self,key,node) :
        if(key in self.dict.keys()):
            list = self.dict.get(key)
            list.append(node)
            self.dict.update({key : list})
        else:
            self.dict.update({key : [node]})    


    
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
        self.when_queries.clear()

#-------------------------------------------------------------------------------------------------------------

class Syntax_Analyzer_WH:
    def __init__(self):
        self.encountered_WH = 0
        self.wh_found = 0
        # self.noun_found = 0
        self.verb_found = 0
        # self.noun_string = ""
        self.verb_string = ""
        self.dict = {}
        self.wh_queries = []



    def syntax_analyzer_wh_detect(self, tag, node, parent): # inorder detection
        if(tag[0] == 'W' and node != "When" and node != "when"):
            # print("Wh encountered  " + str(node))
            if(parent.tag_[0] == 'V' and parent.orth_ not in exceptions) :
                # print("Verb encountered  " + str(parent))
                self.verb_found = 1
                self.verb_string = parent.orth_
            self.wh_found = 1
            return 0

    def syntax_analyzer_wh_verb(self, tag, node, parent): #inorder detection
        if(self.wh_found == 1 and self.verb_found == 0):
            if(tag[0] == 'V' and node not in exceptions) :
                # print("Verb encountered  " + str(node))
                self.verb_found = 1
                self.verb_string = node
                return 0
            else :
                if(parent.tag_[0] == 'V'):
                    self.verb_found = 1
                    self.verb_string = parent.orth_


    def syntax_analyzer_wh_noun(self, tag, node, parent): #preorder detection
        if(self.wh_found == 1 and self.verb_found == 1):
            if(tag[0] == 'N'):
                if(parent.tag_[0] == 'V'):
                    # print("encountered Noun for WH " + str(node) + " and VERB " + str(parent.orth_)) # parent of noun is the verb
                    self.wh_found = 0
                    self.verb_found = 0
                    self.dict_update(self.verb_string, node)
                    return 1
                else :
                    self.wh_found = 0
                    self.verb_found = 0
                    self.dict_update(self.verb_string, node)
                    print(self.verb_string)
                    return 1
        return 0

    def in_WH(self,node):
        return self.dict.get(node, None)

    def add_subquery(self,list):
        subquery = []
        if(len(list) <= 1):
            return
        for i in range(len(list)):
            subquery.append(list[i])
        self.wh_queries.append(subquery)
        return

    def dict_update(self,key,node) :
        if(key in self.dict.keys()):
            list = self.dict.get(key)
            list.append(node)
            self.dict.update({key : list})
        else:
            self.dict.update({key : [node]})
        
    
    def print_all_WH(self): 
        for x in self.dict.keys():
            print(x)
            print(self.dict[x])

    def clear_queries(self):
        self.encountered_WH = 0
        self.wh_found = 0
        # self.noun_found = 0
        self.verb_found = 0
        # self.noun_string = ""
        self.verb_string = ""
        self.dict.clear()
        self.wh_queries.clear()