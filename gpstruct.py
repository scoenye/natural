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


class GPStruct:
    """
    Read a GOLDParser exported parse tree and convert it to
    Structorizer XML
    """

    def parse(self, gp_file):
        for line in gp_file:
            print(line)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Read a GOLDParser parse tree file and convert it to Structorier XML'
    )

    arg_parser.parse_args()

    gp_parser = GPStruct()
    gp_parser.parse(sys.stdin)
