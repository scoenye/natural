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
    @abstractmethod
    def process(self, gp_file):
        """
        Porcess the GP parse tree file and build the node
        :param gp_file:
        :return:
        """


class CompositeNode(TreeNode):
    def __init__(self):
        super().__init__()

        self.level = 0
        self.children = []

    def process(self, gp_file):
        """
        Process the GP parse tree file and build the node's children
        :param gp_file:
        :return:
        """
        for line in gp_file:        # Process the parse tree and stop at the end of the section
            line = line.strip()
            if line == '':
                break

            # Each line has a level part and an expression part, separated by +--
            parts = line.split('+--', maxsplit=1)   # In case the definition contains an expression
            parts[0] = parts[0].count('|')          # Replace tree depth string with the equivalent number

            print(parts)


class LeafNode(TreeNode):
    def process(self, gp_file):
        pass
