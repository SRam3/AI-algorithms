"""Utility functions for the Degrees project."""

class Node():
    def __init__(self, state, parent, action):
        # Current node state
        self.state = state
        # Parent node
        self.parent = parent
        # Action that got us to this state
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        # node.state se refiere al atributo "state" de una instancia específica de la clase Node (es decir, un objeto de la clase Node)
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

