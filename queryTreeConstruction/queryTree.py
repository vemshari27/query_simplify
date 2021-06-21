class QueryNode:
    def __init__(self, left_text="", middle_text="", right_text="", type_=None):
        self.left_text = left_text
        self.middle_text = middle_text
        self.right_text = right_text
        self.type_ = type_
        self.ans = None

    def add_left_text(self, text):
        self.left_text = text

    def get_left_text(self):
        return self.left_text

    def add_middle_text(self, text):
        self.middle_text = text

    def get_middle_text(self):
        return self.middle_text

    def add_right_text(self, text):
        self.right_text = text

    def get_right_text(self):
        return self.right_text

    def get_first_word(self):
        if(self.left_text != ""):
            return self.left_text.split(" ")[0]
        elif(self.middle_text != ""):
            return self.middle_text.split(" ")[0]
        elif(self.right_text != ""):
            return self.right_text.split(" ")[0]
        else:
            return ""

    def __str__(self):
        return "{}-{}-{}, {}".format(self.left_text, self.middle_text, self.right_text, self.type_)


class QueryTree:
    def __init__(self, querynode=None, leftchild=None, rightchild=None, parent=None):
        self.node = querynode
        self.left_child = leftchild
        self.right_child = rightchild
        self.parent = parent
        self.is_empty = True

    def add_left_child(self, querynode):
        ret = None
        if self.node is None:
            self.node = querynode
            ret = self
        elif self.left_child is None:
            self.left_child = QueryTree(querynode, parent=self)
            ret = self.left_child
        else:
            qt = QueryTree(querynode, leftchild=self.left_child, parent=self)
            self.left_child = qt
            qt.left_child.parent = qt
            ret = self.left_child

        return ret

    def add_left_tree(self, queryTree):
        if self.node is None:
            self = queryTree

        elif self.left_child is None:
            self.left_child = queryTree

        # else:
        #     print("Insertion not allowed")
        return self

    def add_right_child(self, querynode):
        ret = None
        if self.node is None:
            self.node = querynode
            ret = self
        elif self.right_child is None:
            self.right_child = QueryTree(querynode, parent=self)
            ret = self.right_child
        else:
            qt = QueryTree(querynode, rightchild=self.right_child, parent=self)
            self.right_child = qt
            qt.left_child.parent = qt
            ret = self.right_child
        return ret

    def add_right_tree(self, queryTree):
        if self.node is None:
            self = queryTree

        elif self.right_child is None:
            self.right_child = queryTree

        # else:
        #     print("Insertion not allowed")
        return self

    def add_to_curr_node(self, text):
        if(self.left_child == None):
            if(str(text) != "'s"):
                self.node.add_left_text(
                    self.node.get_left_text() + " " + str(text))
            else:
                self.node.add_left_text(
                    self.node.get_left_text() + str(text))
        elif(self.right_child == None):
            if(str(text) != "'s"):
                self.node.add_middle_text(
                    self.node.get_middle_text() + " " + str(text))
            else:
                self.node.add_middle_text(
                    self.node.get_middle_text() + str(text))
        else:
            if(str(text) != "'s"):
                self.node.add_right_text(
                    self.node.get_right_text() + " " + str(text))
            else:
                self.node.add_right_text(
                    self.node.get_right_text() + str(text))

        if(self.is_empty == True):
            self.is_empty = False


def print_qt(qt):
    if qt is not None:
        l, r = None, None
        if qt.left_child is not None:
            l = qt.left_child.node
        if qt.right_child is not None:
            r = qt.right_child.node
        print("{};{};{}".format(qt.node, l, r))
        print_qt(qt.left_child)
        print_qt(qt.right_child)


if __name__ == "__main__":
    qt = QueryTree(QueryNode("1"))
    qt.add_left_child(QueryNode("2"))
    qt.add_right_child(QueryNode("3"))
    qt.left_child.add_right_child(QueryNode("5"))
    print_qt(qt)
