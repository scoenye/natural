"""
    gpstruct.py Convert a GOLDParser parse tree export to Structorizer XML

    Copyright (C) 2022  Sven Coenye

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class ExpressionNode:

    def __init__(self, level, expression):
        self.level = level      # Depth of this node
        self.expression = expression

        self.parent = None      # Node immediately above this node
        self.terminals = []     # Terminals found under this node's expression
        self.children = []

    def add_node(self, level, child):
        """
        Insert a node in the tree. If the level is higher than the
        current node's level, the new node will be added as a child of
        the current node. Otherwise, the new child will be passed up
        the parent chain until the first node at a lower level is
        encountered.
        :param level: depth at which the child belongs
        :param child: new child node
        :return:
        """
        if level > self.level:
            self.children.append(child)
            child.parent = self
        else:
            self.parent.add_node(level, child)

    def add_terminal(self, terminal):
        """
        Add a new terminal to the node
        :param terminal: word to add to the collection
        :return:
        """
        self.terminals.append(terminal)

    def render(self, factory):
        """
        Render the formatted grammar
        :param factory: formatting factory
        :return:
        """
        renderer = factory.node(self.expression)

        renderer.render_open(self.terminals)

        for child in self.children:
            child.render(factory)

        renderer.render_close()

