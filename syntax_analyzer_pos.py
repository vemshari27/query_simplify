# Barak Obama's wife's daughter
class Syntax_Analyzer_POS:
    def __init__(self):
        self.encountered_POS = 0
        
        self.dict = {}
        self.pos_queries = []


    def syntax_analyzer_pos_detect(self, tag, node, parent): # postorder detection
        if("POS" == tag): 
            # print("encountered POS " + str(self.encountered_POS))
            self.encountered_POS += 1 
            return 0
        
        elif("POS" != tag and self.encountered_POS > 0):
            if(tag[0] == 'N'):
                # print("encountered Noun Start for POS " + str(node) + " end " + str(parent))
                n = node
                p = parent

                self.encountered_POS -= 1 
                self.dict_update(n, p)
                return 1              
        
    def in_POS(self,node):
        return self.dict.get(node, None)
    
    def add_subquery(self,list):
        subquery = []
        for i in range(len(list)):
            subquery.append(list[i])
        self.pos_queries.append(subquery)

    def dict_update(self,key,node) :
        if(key in self.dict.keys()):
            list = self.dict.get(key)
            list.append(node)
            self.dict.update({key : list})
        else:
            self.dict.update({key : [node]})

    def print_all_POS(self): 
        for x in self.dict.keys():
            print(x)
            print(self.dict[x])
        
    def clear_queries(self):
        self.encountered_POS = 0
        self.dict.clear()
        self.pos_queries.clear()

        
		


	