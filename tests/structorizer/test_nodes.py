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

from structorizer import nodes
from structorizer.factory import StatementFactory

from goldparser.grammar import ExpressionNode, TerminalNode


class CallNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<PERFORM>')
        gp_terminal = TerminalNode(1, 'PERFORM')
        gp_expression.add_node(1, gp_terminal)

        self.diagram_node = nodes.ExitNode(gp_expression, None)
        # Gross violation of encapsulation, but otherwise we have to get the factory involved
        # and a mistake there means this test may not be testing what it should be.
        self.diagram_node.child_nodes.append(nodes.DiagramTerminal(gp_terminal, self.diagram_node))

    def test_build(self):
        self.diagram_node.build('instruction')
        self.assertListEqual(['PERFORM'], self.diagram_node.node_text['instruction'])


class ExitNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<ESCAPE>')
        gp_terminal = TerminalNode(1, 'ESCAPE')
        gp_expression.add_node(1, gp_terminal)

        self.diagram_node = nodes.ExitNode(gp_expression, None)
        # Gross violation of encapsulation, but otherwise we have to get the factory involved
        # and a mistake there means this test may not be testing what it should be.
        self.diagram_node.child_nodes.append(nodes.DiagramTerminal(gp_terminal, self.diagram_node))

    def test_build(self):
        self.diagram_node.build('instruction')
        self.assertListEqual(['ESCAPE'], self.diagram_node.node_text['instruction'])


class InstructionNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<DEFINE_DATA>')
        gp_terminal = TerminalNode(1, 'TEST')
        gp_expression.add_node(1, gp_terminal)

        self.diagram_node = nodes.InstructionNode(gp_expression, None)
        self.diagram_node.child_nodes.append(nodes.DiagramTerminal(gp_terminal, self.diagram_node))

    # def test_render(self):
    #     self.diagram_node.render(StatementFactory, self.gp_node)
    #     self.assertEqual(['TEST'], self.diagram_node.node_text['instruction'])

    def test_build(self):
        self.diagram_node.build('instruction')
        self.assertListEqual(['TEST'], self.diagram_node.node_text['instruction'])

    def test_import_expression(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.assertIsInstance(self.diagram_node.child_nodes[0], nodes.DiagramTerminal)


if __name__ == '__main__':
    unittest.main()
