import numpy as np
from termcolor import colored


class Place():
    """A place class to store the node name and its location"""

    def __init__(self, name=None, location=None):
        self.name = name
        self.location = location


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        # Adjacent squares
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            # Get node position
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) **
                       2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def calculate_and_print_maze(maze, start_place, end_place):
    start = start_place.location
    end = end_place.location
    path = astar(maze, start, end)
    for tup in path:
        maze[tup[0]][tup[1]] = 2

    for row in maze:
        print("")
        for number in row:
            if number == 0:
                print(colored('0', 'green'), end=' ')
            if number == 1:
                print(colored('*', 'red'), end=' ')
            if number == 2:
                print(colored('+', 'yellow'), end=' ')


def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item):
            return item


def get_place_string(list_of_places, end_or_start):
    return input("Pick a place to " + end_or_start + " : " +
                 ', '.join(list(map(lambda x: x.name, list_of_places))) + ' : ')

def decode_place(place_str):
    alejos_office = Place("Alejo's office", (3, 8))
    first_entrance = Place("Entrance one", (9, 1))
    classroom = Place("Classroom", (4, 5))
    bathroom = Place("Bathroom", (9,8)) 

    if place_str == "alejo's office":
        return alejos_office

    if place_str == "bathroom":
        return bathroom

    if place_str == "fishbowl":
        return classroom

    return None

