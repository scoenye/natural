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

import io
import unittest

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

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<call text="PERFORM" comment="" color="ffffff" rotated="0" disabled="0">\n'
                             '</call>\n',
                             output.getvalue())


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

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<jump text="ESCAPE" comment="" color="ffff80" rotated="0" disabled="0">\n'
                             '</jump>\n',
                             output.getvalue())


class ForeverNodeTest(unittest.TestCase):

    def setUp(self) -> None:
        self.grammar = ExpressionNode(0, '<REPEAT>')
        self.diagram_node = nodes.ForeverNode(self.grammar, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<forever comment="" color="ffffff">\n'
                             '  <qForever>\n'
                             '  </qForever>\n'
                             '</forever>\n',
                             output.getvalue())


class ForNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar = ExpressionNode(0, '<FOR>')
        self.grammar.add_node(1, TerminalNode(1, 'FOR'))
        gp_control = ExpressionNode(1, '<user_identifier>')
        gp_control.add_node(2, TerminalNode(2, '#J'))
        self.grammar.add_node(1, gp_control)
        gp_start = ExpressionNode(1, '<constant_integer_pos>')
        gp_start.add_node(2, TerminalNode(2, '1'))
        self.grammar.add_node(1, gp_start)
        gp_to = ExpressionNode(1, '<user_identifier>')
        gp_to.add_node(2, TerminalNode(2, 'C*SOMETHING'))
        self.grammar.add_node(1, gp_to)

        self.diagram_node = nodes.ForNode(self.grammar, None)

    def test_import_expression(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.assertIsInstance(self.diagram_node.child_nodes[0], nodes.DiagramTerminal)

    def test_build(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')
        self.assertListEqual(['FOR'], self.diagram_node.node_text['instruction'])
        self.assertListEqual(['#J'], self.diagram_node.node_text['for_control'])
        self.assertListEqual(['1'], self.diagram_node.node_text['for_from'])
        self.assertListEqual(['C*SOMETHING'], self.diagram_node.node_text['for_to'])


class InstructionNodeTest(unittest.TestCase):
    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<DEFINE_DATA>')
        gp_terminal = TerminalNode(1, 'TEST')
        gp_expression.add_node(1, gp_terminal)

        self.diagram_node = nodes.InstructionNode(gp_expression, None)

    def test_import_expression(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.assertIsInstance(self.diagram_node.child_nodes[0], nodes.DiagramTerminal)

    def test_build(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')
        self.assertListEqual(['TEST'], self.diagram_node.node_text['instruction'])

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<instruction text="TEST" comment="" color="ffffff" rotated="0" disabled="0">\n'
                             '</instruction>\n',
                             output.getvalue())


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

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<while text="RPT-GRP0314" comment="" color="ffffff">\n'
                             '  <qWhile>\n'
                             '  </qWhile>\n'
                             '</while>\n',
                             output.getvalue())


if __name__ == '__main__':
    unittest.main()
