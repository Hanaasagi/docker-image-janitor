import subprocess
from nodes import Node, void

white_images = (
)


def find_position(node, value):
    """
    find node from tree by value, if not found return None
    """
    if not node.children:
        return None
    for sub_node in node.children:
        if value == sub_node.value:
            return sub_node
        rtn = find_position(sub_node, value)
        if rtn is not None:
            return rtn


def merge_to_tree(tree, lst):
    """
    make node from list values, and insert to tree
    """
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


def flatten_tree(tree):
    """ BFS """
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


def get_layers(img_name):
    proc = subprocess.Popen(
        'docker history {} -q'.format(img_name),
        shell=True, encoding='utf-8',  # encoding add in 3.6
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    return [
        layer for layer in stdout.split() if layer != '<missing>'
    ]


def list_images():
    proc = subprocess.Popen(
        'docker images -qa',
        shell=True, encoding='utf-8',  # encoding add in 3.6
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    return stdout.split()


def del_images(img_list):
    p = subprocess.Popen('docker rmi {}'.format(' '.join(img_list)),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         shell=True)
    p.wait()


if __name__ == '__main__':
    layers = []
    for img_name in white_images:
        layers.extend(get_layers(img_name))

    all_imgs = list_images()
    img_need_deleted = set(all_imgs) - set(layers)

    root = Node(None)
    tree = root
    for img_name in img_need_deleted:
        lyers = list(reversed(get_layers(img_name)))
        lst = [l for l in lyers if l in img_need_deleted]
        tree = merge_to_tree(tree, lst)
    # first element is root node(None)
    rm_list = flatten_tree(tree)[1:]
    print(rm_list)
    # if len(rm_list):
        # del_images(list(reversed(rm_list)))
