import copy

UNASSIGNED = 0
BLACK = 1
WHITE = 2
VISITED = 3
TERRITORY_BLACK = 4
TERRITORY_WHITE = 5

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
        if node.value == VISITED:
            continue

        # Node has not yet been visited
        if node.value == UNASSIGNED:
            __flood(node)

    territoryCountBlack = 0
    territoryCountWhite = 0
    territory = copy.deepcopy(stones)

    for node in graph.nodes:
        if node.value == TERRITORY_BLACK:
            territoryCountBlack += 1
        elif node.value == TERRITORY_WHITE:
            territoryCountWhite += 1

    index = 0

    for y, row in enumerate(territory):
        for x, _ in enumerate(row):
            territory[y][x] = graph.nodes[index].value
            index += 1

    return [territoryCountBlack, territoryCountWhite, territory]

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
        node.value = VISITED
        visited.append(node)

        for neighbour in node.neighbours:
            if neighbour.value == UNASSIGNED:
                stack.append(neighbour)
            elif neighbour.value == BLACK:
                black = True
            elif neighbour.value == WHITE:
                white = True

    # To separate territory from the stones we change black from 1 to 4 and white from 2 to 5
    for node in visited:
        if black and not white:
            node.value = TERRITORY_BLACK
        elif white and not black:
            node.value = TERRITORY_WHITE

#from draw import VisualBoard
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
#[territoryCountBlack, territoryCountWhite, territory] = count_territory(stones)
#print("Black: %d, white: %d" % (territoryCountBlack, territoryCountWhite))
#VisualBoard(19).generate_image(stones, territory).save("test.png")
