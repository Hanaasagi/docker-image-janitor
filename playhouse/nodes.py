class Node:
    """ Tree Node """

    def __init__(self, value):
        self._value = value
        self._children = []

    @property
    def value(self):
        return self._value

    @property
    def children(self):
        return self._children

    @property
    def has_children(self) -> bool:
        return len(self._children) != 0

    def append_sub_node(self, node):
        self.children.append(node)

    def __contains__(self, node):
        for n in self.children:
            if node.value == n.value:
                return True

    def find_sub_node(self, value):
        for node in self.children:
            if node.value == value:
                return node

    def __repr__(self):
        return "Node:({}, {})".format(self.value, self.children)


def flatten_tree(tree: Node):
    """BFS"""
    visited = []
    need_visit = []

    def inner(node):
        visited.append(node.value)
        for n in node.children:
            need_visit.append(n)

    need_visit.append(tree)
    while len(need_visit) > 0:
        inner(need_visit.pop(0))
    return visited


def merge_to_tree(tree, lst):
    """ create node from list values, and insert to tree """
    first_elem = lst.pop(0)
    n = find_position(tree, first_elem)
    if n is None:
        n = tree
    for elem in lst:
        next_node = n.find_sub_node(elem)
        if next_node is not None:
            n = next_node
        else:
            next_node = Node(elem)
            n.append_sub_node(next_node)
            n = next_node
    return tree


def find_position(node, value):
    """ find node from tree by value, if not found return None """
    if not node.children:
        return None
    for sub_node in node.children:
        if value == sub_node.value:
            return sub_node
        rtn = find_position(sub_node, value)
        if rtn is not None:
            return rtn


# meaningless value
void = type('Void', (object,), {})


__all__ = [
    'Node',
    'void',
]
