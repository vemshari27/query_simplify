# the president of the United States

class Syntax_Analyzer_IN:
    def __init__(self):
        self.encountered_IN = 0
        self.noun_end = 0
        self.end_string = ""
        self.dict = {}



    def syntax_analyzer_in_detect(self, tag, node, parent): # inorder detection and parent store
        
        if("IN" == tag): 
            # print( "Encountered IN " + str(self.encountered_IN) )
            self.encountered_IN += 1 
            return 0

    def syntax_analyzer_in_noun_start(self, tag, node, parent) : #postorder detection
        
        if(self.encountered_IN > 0 and self.noun_end == 1):
            
            # if(tag[0] == 'N' and tag == "NNP"):
            #     self.encountered_IN -= 1
            #     self.noun_end = 0
            #     return 1

            # elif(tag[0] == 'N') :
            #     self.dict.update({node : self.end_string})
            #     self.encountered_IN -= 1
            #     self.noun_end = 0
            #     return 1
            if(tag[0] == 'N') :
                self.dict_update(node, self.end_string)
                # print("  Noun Start and End for PREP " + str(node) + " PREP " + str(self.end_string))
                self.encountered_IN -= 1
                self.noun_end = 0
                return 1
                
            elif(tag == "IN" and parent.tag_[0] == 'N') :
                # print(" Noun start " + str(node) + " " + str(parent)) 
                self.dict_update(parent.orth_, self.end_string)
                # print("  Noun Start and End for PREP " + str(parent.orth_) + " PREP " + str(self.end_string))
                self.encountered_IN -= 1
                self.noun_end = 0
                return 1

    def syntax_analyzer_in_noun_end(self, tag, node, parent): #post detection
        if("IN" != tag and self.encountered_IN > 0 and self.noun_end == 0):
            if((tag[0] == 'N' or tag ==  "CD") and parent.tag_ == "IN"):
                # print("  Noun End for PREP " + str(node) + " PREP " + str(parent.orth_))
                self.noun_end = 1
                self.end_string = node
                
    def in_PREP(self,node):
        return self.dict.get('Key', None)

    def dict_update(self,key,node) :
        if(key in self.dict.keys()):
            list = self.dict.get(key)
            list.append(node)
            self.dict.update({key : list})
        else:
            self.dict.update({key : [node]})

        
    
    def print_all_IN(self): 
        for x in self.dict.keys():
            print(x)
            print(self.dict[x])

    