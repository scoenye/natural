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

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<alternative text="(#TEST EQ 2)" comment="" color="ffffff">\n'
                             '</alternative>\n',
                             output.getvalue())


class AlternativeTrueTest(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar = ExpressionNode(0, '<THEN_closed>')
        gp_then = ExpressionNode(1, '<THEN>')
        self.grammar.add_node(1, gp_then)
        gp_assign = ExpressionNode(1, '<anon_ASSIGN>')
        self.grammar.add_node(1, gp_assign)
        gp_assign.add_node(2, TerminalNode(2, '#J'))
        gp_assign.add_node(2, TerminalNode(2, '='))
        gp_assign.add_node(2, TerminalNode(2, '123'))

        self.diagram_node = nodes.AlternativeTrueNode(self.grammar, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<qTrue>\n'
                             '<instruction text="#J = 123" comment="" color="ffffff" rotated="0" disabled="0">\n'
                             '</instruction>\n'
                             '</qTrue>\n',
                             output.getvalue())


class AlternativeFalseTest(unittest.TestCase):
    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<ELSE_open>')
        gp_else = ExpressionNode(1, '<ELSE>')
        gp_expression.add_node(1, gp_else)
        gp_else.add_node(2, TerminalNode(2, 'ELSE'))
        gp_assign = ExpressionNode(1, '<anon_ASSIGN>')
        gp_expression.add_node(1, gp_assign)
        gp_assign.add_node(2, TerminalNode(2, '#C'))
        gp_assign.add_node(2, TerminalNode(2, '='))
        gp_assign.add_node(2, TerminalNode(2, '3'))

        self.diagram_node = nodes.AlternativeFalseNode(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<qFalse>\n'
                             '<instruction text="#C = 3" comment="" color="ffffff" rotated="0" disabled="0">\n'
                             '</instruction>\n'
                             '</qFalse>\n',
                             output.getvalue())


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


class CaseNodeTest(unittest.TestCase):

    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<DECIDE_ON>')
        gp_expression.add_node(1, TerminalNode(1, 'DECIDE'))
        gp_expression.add_node(1, TerminalNode(1, 'ON'))

        gp_decide_which = ExpressionNode(1, '<DECIDE_which>')
        gp_decide_which.add_node(2, TerminalNode(2, 'FIRST'))
        gp_decide_which.add_node(2, TerminalNode(2, 'VALUE'))
        gp_decide_which.add_node(2, TerminalNode(2, 'OF'))
        gp_decide_which.add_node(2, TerminalNode(2, '#LN-MEM-CD'))

        gp_expression.add_node(1, gp_decide_which)

        self.diagram_node = nodes.CaseNode(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<case text="&#34;()&#34;," comment="DECIDE ON FIRST VALUE OF #LN-MEM-CD" color="ffffff">\n'
                             '</case>\n',
                             output.getvalue())


class CaseBranchTest(unittest.TestCase):

    def setUp(self) -> None:
        gp_expression = ExpressionNode(0,'<DECIDE_ON_branch>')

        gp_expression.add_node(1, TerminalNode(1, 'VALUE'))

        gp_value = ExpressionNode(1, '<constant_alpha>')
        gp_value.add_node(2, TerminalNode (2, '1S'))

        gp_expression.add_node(1, gp_value)

        gp_assign = ExpressionNode(1, '<anon_ASSIGN>')
        gp_expression.add_node(1, gp_assign)
        gp_assign.add_node(2, TerminalNode(2, '#C'))
        gp_assign.add_node(2, TerminalNode(2, '='))
        gp_assign.add_node(2, TerminalNode(2, '3'))

        self.diagram_node = nodes.CaseBranch(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<qCase>\n'
                             '<instruction text="#C = 3" comment="" color="ffffff" rotated="0" disabled="0">\n'
                             '</instruction>\n'
                             '</qCase>\n',
                             output.getvalue())


class CaseNoneTest(unittest.TestCase):

    def setUp(self) -> None:
        gp_expression = ExpressionNode(0,'<DECIDE_ON_none>')
        gp_expression.add_node(1, TerminalNode(1, 'NONE'))

        gp_ignore = ExpressionNode(1, '<IGNORE>')
        gp_expression.add_node(1, gp_ignore)

        gp_ignore.add_node(2, TerminalNode (2, 'IGNORE'))

        self.diagram_node = nodes.NoneBranch(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<qCase>\n'
                             '<instruction text="IGNORE" comment="" color="ffffff" rotated="0" disabled="0">\n'
                             '</instruction>\n'
                             '</qCase>\n',
                             output.getvalue())


class DecideOnTest(unittest.TestCase):
    """
    Combined CaseNode/CaseBranch test
    """
    def setUp(self) -> None:
        gp_decide_on = ExpressionNode(0, '<DECIDE_ON>')
        gp_decide_on.add_node(1, TerminalNode(1, 'DECIDE'))
        gp_decide_on.add_node(1, TerminalNode(1, 'ON'))

        gp_decide_which = ExpressionNode(1, '<DECIDE_which>')
        gp_decide_on.add_node(1, gp_decide_which)
        gp_decide_which.add_node(2, TerminalNode(2, 'FIRST'))
        gp_decide_which.add_node(2, TerminalNode(2, 'VALUE'))

        gp_decide_of = ExpressionNode(1, '<OF>')
        gp_decide_on.add_node(1, gp_decide_of)
        gp_decide_of.add_node(2, TerminalNode(2, 'OF'))

        gp_decide_control = ExpressionNode(1, '<user_variable>')
        gp_decide_on.add_node(1, gp_decide_control)
        gp_decide_control.add_node(2, TerminalNode(2, '#LN-MEM-CD'))

        # First branch
        gp_branch = ExpressionNode(2,'<DECIDE_ON_branch>')
        gp_decide_on.add_node(2, gp_branch)

        gp_branch.add_node(3, TerminalNode(3, 'VALUE'))

        gp_value = ExpressionNode(3, '<constant_alpha>')
        gp_value.add_node(4, TerminalNode (4, '1S'))

        gp_branch.add_node(3, gp_value)

        gp_assign = ExpressionNode(3, '<anon_ASSIGN>')
        gp_branch.add_node(3, gp_assign)

        gp_assign.add_node(4, TerminalNode(4, '#C'))
        gp_assign.add_node(4, TerminalNode(4, '='))
        gp_assign.add_node(4, TerminalNode(4, '3'))

        # Second branch
        gp_branch = ExpressionNode(2,'<DECIDE_ON_branch>')
        gp_decide_on.add_node(2, gp_branch)

        gp_branch.add_node(3, TerminalNode(3, 'VALUE'))

        gp_value = ExpressionNode(3, '<constant_alpha>')
        gp_value.add_node(4, TerminalNode (4, '2S'))

        gp_branch.add_node(3, gp_value)

        gp_assign = ExpressionNode(3, '<anon_ASSIGN>')
        gp_branch.add_node(3, gp_assign)

        gp_assign.add_node(4, TerminalNode(4, '#D'))
        gp_assign.add_node(4, TerminalNode(4, '='))
        gp_assign.add_node(4, TerminalNode(4, '4'))

        # None branch
        gp_none = ExpressionNode(1, '<DECIDE_ON_none>')
        gp_decide_on.add_node(1, gp_none)

        gp_none.add_node(2, TerminalNode(2, 'NONE'))

        gp_ignore = ExpressionNode(2, '<IGNORE>')
        gp_ignore.add_node(3, TerminalNode(3, 'IGNORE'))
        gp_none.add_node(2, gp_ignore)

        self.diagram_node = nodes.CaseNode(gp_decide_on, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<case text="&#34;(#LN-MEM-CD)&#34;,&#34;1S&#34;,&#34;2S&#34;,&#34;NONE&#34;" comment="DECIDE ON FIRST VALUE" color="ffffff">\n'
                             '<qCase>\n'
                             '<instruction text="#C = 3" comment="" color="ffffff" rotated="0" disabled="0">\n'
                             '</instruction>\n'
                             '</qCase>\n'
                             '<qCase>\n'
                             '<instruction text="#D = 4" comment="" color="ffffff" rotated="0" disabled="0">\n'
                             '</instruction>\n'
                             '</qCase>\n'
                             '<qCase>\n'
                             '<instruction text="IGNORE" comment="" color="ffffff" rotated="0" disabled="0">\n'
                             '</instruction>\n'
                             '</qCase>\n'
                             '</case>\n',
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


class ReinputTest(unittest.TestCase):
    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<REINPUT>')
        gp_expression.add_node(1, TerminalNode(1, 'REINPUT'))
        gp_expression.add_node(1, TerminalNode(1, '''*WARNING*: You have changed the Override field from "Y".'''))

        self.diagram_node = nodes.ExitNode(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<jump text="REINPUT ''*WARNING*: You have changed the Override field from &#34;&#34;Y&#34;&#34;.''" comment="" color="ffff80" rotated="0" disabled="0">\n'
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

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<for text="FOR #J &#60;- 1 to C*SOMETHING" comment="" color="ffffff">\n'
                             '  <qFor>\n'
                             '  </qFor>\n'
                             '</for>\n',
                             output.getvalue())


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
