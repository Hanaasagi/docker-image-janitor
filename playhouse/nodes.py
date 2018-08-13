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


# meaningless value
void = type('Void', (object,), {})


__all__ = [
    'Node',
    'void',
]
