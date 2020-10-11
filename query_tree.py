def print_qt(qt):
    if qt is not None:
        l,r = None, None
        if qt.left_child is not None:
            l = qt.left_child.node
        if qt.right_child is not None:
            r = qt.right_child.node
        print("{};{};{}".format(qt.node, l, r))
        print_qt(qt.left_child)
        print_qt(qt.right_child)

class Query:
    def __init__(self, text, type_=None):
        self.text = text
        self.type_ = type_
        self.ans = None
    def __str__(self):
        return "{}, {}".format(self.text, self.type_)


class QueryTree:
    def __init__(self, q=None, lc=None, rc=None):
        self.node = q
        self.left_child = lc
        self.right_child = rc

    def add_left_child(self, q):
        ret = None
        if self.node is None:
            self.node = q
            ret = self
        elif self.left_child is None:
            self.left_child = QueryTree(q)
            ret = self.left_child
        else:
            qt = QueryTree(q, lc=self.left_child)
            self.left_child = qt
            ret = self.left_child
        return ret

    def add_right_child(self, q):
        ret = None
        if self.node is None:
            self.node = q
            ret = self
        elif self.right_child is None:
            self.right_child = QueryTree(q)
            ret = self.right_child
        else:
            qt = QueryTree(q, lc=self.right_child)
            self.right_child = qt
            ret = self.right_child
        return ret

    # def printing()

    # def __str__(self, ):
    #     if 
    #     return "{};{};{}".format(self.node, self.__str__(self.left_child), self.__str__(self.left_child)))

if __name__ == "__main__":
    qt = QueryTree(Query("1"))
    qt.add_left_child(Query("2"))
    qt.add_right_child(Query("3"))
    qt.left_child.add_right_child(Query("5"))

    print_qt(qt)