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
import re
import sys

import nodes.factory
from nodes.factory import TreeNodeFactory


class GPStruct:
    """
    Read a GOLDParser exported parse tree and convert it to
    Structorizer XML
    """
    expression_l = re.compile(r'<(.+)> ::=')


    def __init__(self):
        self.root = None

    def parse(self, gp_file):
        # Parse tree files have two sections, each with a header. The header and section
        # are separated by a blank line.
        for line in gp_file:            # Skip the Parse Tree header
            if line.strip() == '':      # strip because line endings
                break

        # The first line should be at level 0. If not, we punt.
        line = gp_file.readline().strip()
        # Each line has a level part and an expression part, separated by +--
        parts = line.split('+--', maxsplit=1)  # In case the definition contains an expression
        parts[0] = parts[0].count('|')  # Replace tree depth string with the equivalent number

        if parts[0] != 0:
            print('Bad parsetree file. Initial statement is not at level 0')
            print('Found {} at level {}'. format(parts[1], parts[0]))
        else:
            # Expressions start with a keyword in angle brackets
            lvalue = self.expression_l.match(parts[1]).group(1)

            if lvalue is None:
                print('Unable to detect a starting expression.')
            else:
                root = TreeNodeFactory.node(lvalue)

                root.process(gp_file)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Read a GOLDParser parse tree file and convert it to Structorizer XML'
    )

    arg_parser.parse_args()

    gp_parser = GPStruct()
    gp_parser.parse(sys.stdin)
