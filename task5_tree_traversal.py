import uuid

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.id = str(uuid.uuid4()) # Unique identifier for each node


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        # Add the node to the graph using its unique ID and store its value and color
        graph.add_node(node.id, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def depth_first_traversal(node, order):
    if node is None:
        return
    order.append(node)
    depth_first_traversal(node.left, order)
    depth_first_traversal(node.right, order)


def breadth_first_traversal(node, order):
    queue = [node]
    while queue:
        cur = queue.pop(0)
        order.append(cur)
        if cur.left:
            queue.append(cur.left)
        if cur.right:
            queue.append(cur.right)


def generate_color(index, total):
    """
    Generate a smooth gradient from dark-blue to light-blue.
    """

    # Normalize t from 0.0 to 1.0
    t = index / max(total - 1, 1)

    # Start (dark blue)
    r1, g1, b1 = 0x30, 0x40, 0xA0

    # End (bright blue)
    r2, g2, b2 = 0x12, 0x96, 0xF0

    # Linear interpolation
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)

    return f"#{r:02x}{g:02x}{b:02x}"


def draw_tree(tree_root, traversal_type):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    order = []
    if traversal_type == "DFS":
        depth_first_traversal(tree_root, order)
    else:
        breadth_first_traversal(tree_root, order)
    total = len(order)

    colors = {node.id: generate_color(i, total) for i, node in enumerate(order)}
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    draw_colors = [colors[nid] for nid in labels.keys()]

    plt.figure(figsize=(8, 6))
    plt.title(f"{traversal_type} traversal")
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=draw_colors)
    plt.show()


if __name__ == "__main__":
    root = Node(50)
    root.left = Node(21)
    root.left.left = Node(13)
    root.left.right = Node(37)
    root.right = Node(84)
    root.right.left = Node(72)
    root.right.right = Node(95)

    draw_tree(root, 'DFS')
    draw_tree(root, 'BFS')
