class Query:
    def __init__(self, text):
        self.text = text
        self.type = None


class QueryTree:
    def __init__(self, q=None, lc=None, rc=None):
        self.node = q
        self.left_child = lc
        self.right_child = rc

    def add_left_child(self, q):
        if self.left_child is None:
            self.left_child = QueryTree(q)
        else:
            qt = QueryTree(q, lc=self.left_child)
            self.left_child = qt

    def add_right_child(self, q):
        if self.right_child is None:
            self.right_child = QueryTree(q)
        else:
            qt = QueryTree(q, lc=self.right_child)
            self.right_child = qt
