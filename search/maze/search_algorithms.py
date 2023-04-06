class Node():
    """
    Data structure to keep track of:
    A state
    Its parent node, through which the current node was generated
    The action that was applied to the state of the parent to get to the current node
    The path cost from the initial state to this nod
    """
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

# Frontier: Mechanism that “manages” the nodes
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    # Define the function that removes a node from the frontier and returns it.
    def remove(self):
        # Terminate the search if the frontier is empty, because this means that there is no solution.
        if self.empty():
            raise Exception("empty frontier")
        else:
            # Save the last item in the list (which is the newest node added)
            node = self.frontier[-1]
            # Save all the items on the list besides the last node (i.e. removing the last node)
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            # Save the oldest item on the list (which was the first one to be added)
            node = self.frontier[0]
            # Save all the items on the list besides the first one (i.e. removing the first node)
            self.frontier = self.frontier[1:]
            return node
        

class GreedyBestFirstSearchFrontier(StackFrontier):
    def __init__(self, goal):
        super().__init__()
        self.goal = goal

    def add(self, node):
        # Calculate the distance between the current node and the goal
        # Manhattan distance: the sum of the absolute differences of their Cartesian coordinates
        distance = abs(node.state[0] - self.goal[0]) + abs(node.state[1] - self.goal[1])
        # Add the node and its distance to the frontier
        self.frontier.append((node, distance))

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            # Sort the frontier by the distance between the node and the goal
            self.frontier.sort(key=lambda x: x[1])
            # Save the node with the smallest distance
            node = self.frontier[0][0]
            # Save all the items on the list besides the first one (i.e. removing the first node)
            self.frontier = self.frontier[1:]
            return node
        

# class AStarFrontier(StackFrontier):
#     def __init__(self, goal):
#         super().__init__()
#         self.goal = goal

#     def add(self, node):
#         # Calculate the distance between the current node and the goal
#         distance = abs(node.state[0] - self.goal[0]) + abs(node.state[1] - self.goal[1])
#         # Add the node and its distance to the frontier
#         self.frontier.append((node, distance))

#     def remove(self):
#         if self.empty():
#             raise Exception("empty frontier")
#         else:
#             # Sort the frontier by the distance between the node and the goal
#             self.frontier.sort(key=lambda x: x[1])
#             # Save the node with the smallest distance
#             node = self.frontier[0][0]
#             # Save all the items on the list besides the first one (i.e. removing the first node)
#             self.frontier = self.frontier[1:]
#             return node