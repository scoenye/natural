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


class AlternativeNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar = ExpressionNode(0, '<IF_open>')
        gp_IF = TerminalNode(1, 'IF')
        gp_condition = ExpressionNode(1, '<logical_expression>')
        gp_test = TerminalNode(2, '#TEST')
        gp_eq = TerminalNode(2, 'EQ')
        gp_2 = TerminalNode(2, '2')

        self.grammar.add_node(1, gp_IF)
        self.grammar.add_node(1, gp_condition)
        gp_condition.add_node(2, gp_test)
        gp_condition.add_node(2, gp_eq)
        gp_condition.add_node(2, gp_2)

        self.diagram_node = nodes.AlternativeNode(self.grammar, None)

    def test_import_expression(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.assertIsInstance(self.diagram_node.child_nodes[0], nodes.DiagramTerminal)

    def test_build(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')
        self.assertListEqual(['#TEST', 'EQ', '2'], self.diagram_node.node_text['instruction'])


class CallNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<PERFORM>')
        gp_terminal = TerminalNode(1, 'PERFORM')
        gp_expression.add_node(1, gp_terminal)

        self.diagram_node = nodes.CallNode(gp_expression, None)

    def test_import_expression(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.assertIsInstance(self.diagram_node.child_nodes[0], nodes.DiagramTerminal)

    def test_build(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')
        self.assertListEqual(['PERFORM'], self.diagram_node.node_text['instruction'])


class ExitNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<ESCAPE>')
        gp_terminal = TerminalNode(1, 'ESCAPE')
        gp_expression.add_node(1, gp_terminal)

        self.diagram_node = nodes.ExitNode(gp_expression, None)

    def test_import_expression(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.assertIsInstance(self.diagram_node.child_nodes[0], nodes.DiagramTerminal)

    def test_build(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')
        self.assertListEqual(['ESCAPE'], self.diagram_node.node_text['instruction'])


class InstructionNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<DEFINE_DATA>')
        gp_terminal = TerminalNode(1, 'TEST')
        gp_expression.add_node(1, gp_terminal)

        self.diagram_node = nodes.InstructionNode(gp_expression, None)

    # def test_render(self):
    #     self.diagram_node.render(StatementFactory, self.gp_node)
    #     self.assertEqual(['TEST'], self.diagram_node.node_text['instruction'])

    def test_import_expression(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.assertIsInstance(self.diagram_node.child_nodes[0], nodes.DiagramTerminal)

    def test_build(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')
        self.assertListEqual(['TEST'], self.diagram_node.node_text['instruction'])


class WhileNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar = ExpressionNode(0, '<READ>')
        gp_terminal1 = TerminalNode(1, 'RPT-GRP0314')
        gp_loop = ExpressionNode(1, '<loop_statement_list>')
        gp_terminal2 = TerminalNode(2, 'LOOP')

        self.grammar.add_node(1, gp_terminal1)
        self.grammar.add_node(1, gp_loop)
        gp_loop.add_node(2, gp_terminal2)

        self.diagram_node = nodes.WhileNode(self.grammar, None)

    def test_import_expression(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.assertIsInstance(self.diagram_node.child_nodes[0], nodes.DiagramTerminal)

    def test_build(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')
        self.assertListEqual(['RPT-GRP0314'], self.diagram_node.node_text['instruction'])


if __name__ == '__main__':
    unittest.main()
