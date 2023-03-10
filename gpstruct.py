#! /usr/bin/env python3

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

import argparse
import sys

from goldparser.grammar import ExpressionNode, TerminalNode
from structorizer.factory import StatementFactory


class GPStruct:
    """
    Read a GOLDParser exported parse tree and convert it to
    Structorizer XML
    """

    def __init__(self):
        self.gp_root = None
        self.diagram_root = None

    @staticmethod
    def _split_line(line):
        # Each line has a level part and an expression part, separated by +--
        # Split the line on the +-- and replace the vertical bars with the bar count.
        parts = line.split('+--', maxsplit=1)  # In case the definition contains an expression
        parts[0] = parts[0].count('|')  # Replace tree level string with the equivalent number

        return parts

    def parse(self, gp_file):
        """
        Process a GoldParser grammar tree export file. The result is a
        tree made of GrammarNodes.
        :param gp_file:
        :return:
        """
        # Parse tree files have two sections, each with a header. The header and section
        # are separated by a blank line.
        for line in gp_file:            # Skip the Parse Tree header
            if line.strip() == '':      # strip because line endings
                break

        parts = self._split_line(gp_file.readline().strip())        # Normally the <program> line

        # The first line should be at level 0. If not, we punt.
        if parts[0] != 0:
            print('Bad parsetree file. Initial statement is not at level 0')
            print('Found {} at level {}'. format(parts[1], parts[0]))
        else:
            # Expressions start with a keyword in angle brackets
            if parts[1][0] != '<':
                print('Unable to detect a starting expression.')
            else:
                self.gp_root = ExpressionNode(parts[0], parts[1])
                last_node = self.gp_root

                for line in gp_file:  # Process the parse tree and stop at the end of the section
                    line = line.strip()
                    if line == '':
                        break

                    parts = self._split_line(line)      # Break up in level and expression

                    # line contains a terminal if it starts with <, but just < means 'less than'
                    if parts[1][0] != '<' or parts[1] == '<':
                        new_node = TerminalNode(parts[0], parts[1])
                        last_node.add_node(parts[0], new_node)
                    else:
                        new_node = ExpressionNode(parts[0], parts[1])
                        last_node.add_node(parts[0], new_node)
                        last_node = new_node    # Descend to the next level

    def build_render_nodes(self, factory):
        """
        Create the diagram nodes for the parse tree
        :param factory:
        :return:
        """
        self.diagram_root = self.gp_root.export_node(factory, None)

    def build_diagram(self):
        """
        Tell the diagram nodes to collect what they need to render
        the final output.
        :return:
        """
        self.diagram_root.build('instruction')

    def render(self, out_file):
        """
        Render the parsed GP file as Structorizer XML
        :return:
        """
        self.diagram_root.render(out_file)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Read a GOLDParser parse tree file and convert it to Structorizer XML'
    )

    arg_parser.parse_args()

    gp_parser = GPStruct()
    gp_parser.parse(sys.stdin)
    gp_parser.build_render_nodes(StatementFactory)
    gp_parser.build_diagram()

    gp_parser.render(sys.stdout)
