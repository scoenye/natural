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
import re
from abc import ABC, abstractmethod


class GrammarNode(ABC):
    """
    GP grammar node interface
    """
    def __init__(self, level, expression):
        self.level = level      # Depth of this node
        self.expression = expression

        self.parent = None      # Node immediately above this node

    @abstractmethod
    def render(self, factory):
        """
        Produce diagram contents for the grammar node
        :param factory: diagram node factory class
        :return:
        """

    def matches(self, lvalue):
        """
        Check if the left side of the expression is a match to the
        supplied text.
        :param lvalue: text to match
        :return: True if the expression matches, False if not
        """
        if self.expression.startswith(lvalue):
            return True
        else:
            return False


class ExpressionNode(GrammarNode):
    """
    GP grammar node to hold an expression. ExpressionNodes may contain
    other GrammarNodes.
    """

    def __init__(self, level, expression):
        super().__init__(level, expression)

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

    def traverse(self):
        """
        Go over the branch nodes in order
        :return:
        """
        yield from self.children

    def render(self, factory):
        """
        Produce a diagram node for this expression
        :param factory:
        :return:
        """
        lvalue = self.expression.split('::=')[0]

        renderer = factory.node(lvalue)
        content = renderer.render(factory, self)

        return content


class TerminalNode(GrammarNode):
    """
    GP grammar node to hold terminals. TerminalNodes are leaf nodes.
    """

    def add_node(self, level, child):
        """
        TerminalNodes do not have child nodes.
        :param level: depth at which the child belongs
        :param child: new child node
        :return:
        """
        pass

    def render(self, factory):
        """
        A TerminalNode returns its keyword
        :param factory: diagram node factory class
        :return:
        """
        return self.expression
