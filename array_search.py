class Graph:
    """A simple undirected graph."""

    def __init__(self, array):
        """Instantiates a new graph from a given 2D-array.

        Arguments:
        array -- The 2D-array of values to construct the graph from
        """

        self.nodes = []

        nodeArray = [[Node([], value) for value in row] for row in array]

        for y, row in enumerate(nodeArray):
            for x, node in enumerate(row):
                neighbours = []

                if y > 0:
                    neighbours.append(nodeArray[y - 1][x])
                if y < len(nodeArray) - 1:
                    neighbours.append(nodeArray[y + 1][x])
                if x > 0:
                    neighbours.append(nodeArray[y][x - 1])
                if x < len(row) - 1:
                    neighbours.append(nodeArray[y][x + 1])

                node.neighbours = neighbours

        for row in nodeArray:
            for node in row:
                self.nodes.append(node)

class Node:
    """A simple node in an undirected graph."""

    def __init__(self, neighbours, value):
        """Instantiates a new node with an array of neighbours and a value.

        Arguments:
        neighbours -- The node list of neighbours
        value -- The node value
        """

        self.neighbours = neighbours
        self.value = value

def count_territory(stones):
    """Counts the territory controlled by the players.

    Arguments:
    stones -- The 2D-array of stones where 1 = black, 2 = white and 0 = no stone
    """

    graph = Graph(stones)

    # We introduce the new value 3 which means the node has been visited but is not part of a player's territory
    for node in graph.nodes:
        if node.value == 3:
            continue

        # Node has not yet been visited
        if node.value == 0:
            __flood(node)

    territoryBlack = 0
    territoryWhite = 0

    for node in graph.nodes:
        if node.value == 1:
            territoryBlack += 1
        elif node.value == 2:
            territoryWhite += 1

    return [territoryBlack, territoryWhite]

def __flood(start):
    """Performs a simple depth-first search for all adjacent nodes without stones, starting from the given node.
    If we hit a black stone, mark everything as black territory.
    If we hit a white stone, mark everything as white territory.
    If we hit both, it's neither.

    Arguments:
    start -- The starting node
    """

    stack = [start]
    visited = []
    black = False
    white = False

    while stack:
        node = stack.pop()
        node.value = 3
        visited.append(node)

        for neighbour in node.neighbours:
            if neighbour.value == 0:
                stack.append(neighbour)
            elif neighbour.value == 1:
                black = True
            elif neighbour.value == 2:
                white = True

    for node in visited:
        if black and not white:
            node.value = 1
        elif white and not black:
            node.value = 2

#stones = [
#    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0]
#]
#[blackTerritory, whiteTerritory] = count_territory(stones)
#print("Black: %d, white: %d" % (blackTerritory, whiteTerritory))
