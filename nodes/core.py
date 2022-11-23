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

from abc import ABC, abstractmethod


class TreeNode(ABC):
    def __init__(self, level):
        self.parent = None      # TreeNode immediately above this node
        self.level = level      # Depth of this node
        self.terminals = []     # Terminals found under this node's expression

    @abstractmethod
    def add_node(self, level, child):
        """
        Add a node to the tree
        :param level:
        :param child:
        :return:
        """

    def add_terminal(self, terminal):
        """
        Add a new terminal to the node
        :param terminal: word to add to the collection
        :return:
        """
        self.terminals.append(terminal)


class CompositeNode(TreeNode):

    def __init__(self, level):
        super().__init__(level)

        self.children = []
        self.terminals = []     # The terminals that make up this instruction

    def add_node(self, level, child):
        """
        Insert a node in the tree. If the level is higher than the
        current node's level, the new node will be added as a child of
        the current node. Otherwise, the new child will be passed up
        the parent chain until the first node at a lower level is
        encountered.
        :param level: depth at which the child belongs
        :param child: new child TreeNode
        :return:
        """
        if level > self.level:
            self.children.append(child)
            child.parent = self
        else:
            self.parent.add_node(level, child)

class LeafNode(TreeNode):

    def add_node(self, level, child):
        pass
