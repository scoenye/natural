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

from goldparser.grammar import ExpressionNode, TerminalNode
from structorizer.factory import StatementFactory
from structorizer.nodes import InstructionNode, DiagramTerminal


class ExpressionNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.gp_node = ExpressionNode(0, '<ADD> ::= <rvalue>')
        self.gp_node.add_node(1, TerminalNode(1, 'TEST'))

    def test_lvalue(self):
        self.assertEqual('ADD', self.gp_node.lvalue())

    def test_export_node(self):
        self.assertIsInstance(self.gp_node.export_node(StatementFactory, None), InstructionNode)

    def test_render(self):
        # ExpressionNode renders to the screen so there is nothing to return.
        self.assertEqual('', self.gp_node.render(StatementFactory, None))


class TerminalNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.node = TerminalNode(0, 'TEST')

    def test_export_node(self):
        self.assertIsInstance(self.node.export_node(StatementFactory, None), DiagramTerminal)

    def test_render(self):
        self.assertEqual('TEST', self.node.render(StatementFactory, None))


if __name__ == '__main__':
    unittest.main()
