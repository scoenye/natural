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

import unittest

from unittest.mock import MagicMock

from grammar import ExpressionNode, TerminalNode
from structorizer.factory import StatementFactory


class ExpressionNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.factory = StatementFactory
        self.node = ExpressionNode(0, '<program> ::=')
        self.node.add_node(1, TerminalNode(1, 'TEST'))

    def test_render(self):
        self.assertEqual(['TEST'], self.node.render(self.factory, None))


class TerminalNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.factory = MagicMock
        self.node = TerminalNode(0, 'TEST')

    def test_render(self):
        self.assertEqual('TEST', self.node.render(self.factory, None))


if __name__ == '__main__':
    unittest.main()
