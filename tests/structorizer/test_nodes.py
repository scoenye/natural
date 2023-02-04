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

from structorizer.nodes import InstructionNode, DiagramTerminal
from structorizer.factory import StatementFactory

from goldparser.grammar import ExpressionNode, TerminalNode


class InstructionNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.gp_node = ExpressionNode(0, '<DEFINE_DATA>')
        self.gp_node.add_node(1, TerminalNode(1, 'TEST'))
        self.diagram_node = InstructionNode(self.gp_node, None)

    def test_render(self):
        self.diagram_node.render(StatementFactory, self.gp_node)
        self.assertEqual(['TEST'], self.diagram_node.node_text['instruction'])

    def test_import_expression(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.assertIsInstance(self.diagram_node.child_nodes[0], DiagramTerminal)


if __name__ == '__main__':
    unittest.main()
