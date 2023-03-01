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

            self.assertEqual(
                '<qTrue>\n'
                '<instruction text="#J = 123" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n'
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

            self.assertEqual(
                '<qFalse>\n'
                '<instruction text="#C = 3" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n'
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

            self.assertEqual('<call text="PERFORM" comment="" color="ffffff" rotated="0" disabled="0"></call>\n',
                             output.getvalue())


class ToCaseNodeTest(unittest.TestCase):

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

        self.diagram_node = nodes.ToCaseNode(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<case text="&#34;()&#34;," comment="DECIDE ON FIRST VALUE OF #LN-MEM-CD" color="ffffff">\n'
                             '</case>\n',
                             output.getvalue())


class ToCaseBranchTest(unittest.TestCase):

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

        self.diagram_node = nodes.ToCaseBranch(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual(
                '<qCase>\n'
                '<instruction text="#C = 3" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n'
                '</qCase>\n',
                output.getvalue())


class ToCaseConditionTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.gp_decide_on = MagicMock()

        gp_on_condition = ExpressionNode(0,'<DECIDE_ON_condition>')
        gp_on_condition.add_node(1, TerminalNode(1, 'B'))

        gp_value_list = ExpressionNode(1, '<DECIDE_ON_value_list>')
        gp_on_condition.add_node(1, gp_value_list)

        gp_value_list.add_node(2, TerminalNode(2, ','))
        gp_value_list.add_node(2, TerminalNode(2, 'C'))

        self.diagram_node = nodes.ToCaseCondition(gp_on_condition, self.gp_decide_on)

    def test_build(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('branches')

        self.gp_decide_on.add_text.assert_called_with('branches', 'B , C')


class ToCaseNoneTest(unittest.TestCase):

    def setUp(self) -> None:
        gp_expression = ExpressionNode(0,'<DECIDE_ON_none>')
        gp_expression.add_node(1, TerminalNode(1, 'NONE'))

        gp_ignore = ExpressionNode(1, '<IGNORE>')
        gp_expression.add_node(1, gp_ignore)

        gp_ignore.add_node(2, TerminalNode (2, 'IGNORE'))

        self.diagram_node = nodes.ToNoneBranch(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual(
                '<qCase>\n'
                '<instruction text="IGNORE" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n'
                '</qCase>\n',
                output.getvalue())


class ToDecideOnTest(unittest.TestCase):
    """
    Combined ToCaseNode/ToCaseBranch test for the DECIDE ON statement
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

        self.diagram_node = nodes.ToCaseNode(gp_decide_on, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<case text="&#34;(#LN-MEM-CD)&#34;,&#34;1S&#34;,&#34;2S&#34;,&#34;NONE&#34;" comment="DECIDE ON FIRST VALUE" color="ffffff">\n'
                             '<qCase>\n'
                             '<instruction text="#C = 3" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n'
                             '</qCase>\n'
                             '<qCase>\n'
                             '<instruction text="#D = 4" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n'
                             '</qCase>\n'
                             '<qCase>\n'
                             '<instruction text="IGNORE" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n'
                             '</qCase>\n'
                             '</case>\n',
                             output.getvalue())


class ForCaseNodeTest(unittest.TestCase):

    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<DECIDE_FOR>')
        gp_expression.add_node(1, TerminalNode(1, 'DECIDE'))
        gp_expression.add_node(1, TerminalNode(1, 'FOR'))

        gp_decide_which = ExpressionNode(1, '<DECIDE_which>')
        gp_decide_which.add_node(2, TerminalNode(2, 'EVERY'))

        gp_expression.add_node(1, gp_decide_which)

        gp_expression.add_node(1, TerminalNode(1, 'CONDITION'))

        self.diagram_node = nodes.ForCaseNode(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<case text="&#34;(*)&#34;," comment="DECIDE FOR EVERY CONDITION" color="ffffff">\n'
                             '</case>\n',
                             output.getvalue())


class ForCaseBranchTest(unittest.TestCase):

    def setUp(self) -> None:
        gp_expression = ExpressionNode(0,'<DECIDE_FOR_branch>')

        gp_expression.add_node(1, TerminalNode(1, 'WHEN'))

        gp_condition = ExpressionNode(1, '<logical_criterion>')
        gp_expression.add_node(1, gp_condition)

        gp_condition.add_node(2, TerminalNode (2, '#FOO'))
        gp_condition.add_node(2, TerminalNode(2, 'EQ'))
        gp_condition.add_node(2, TerminalNode(2, '#BAR'))

        gp_assign = ExpressionNode(1, '<anon_ASSIGN>')
        gp_expression.add_node(1, gp_assign)

        gp_assign.add_node(2, TerminalNode(2, '#C'))
        gp_assign.add_node(2, TerminalNode(2, '='))
        gp_assign.add_node(2, TerminalNode(2, '3'))

        # ForCaseBranch requires a parent to report the branch condition to.
        # No parent -> kaboom.
        self.for_case_node = MagicMock()
        self.diagram_node = nodes.ForCaseBranch(gp_expression, self.for_case_node)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        self.for_case_node.add_text.assert_called_with('branches', '#FOO EQ #BAR')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<qCase>\n'
                             '<instruction text="#C = 3" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n'
                             '</qCase>\n',
                             output.getvalue())


class ForCaseNoneTest(unittest.TestCase):

    def setUp(self) -> None:
        gp_expression = ExpressionNode(0,'<DECIDE_FOR_none>')
        gp_expression.add_node(1, TerminalNode(1, 'WHEN'))
        gp_expression.add_node(1, TerminalNode(1, 'NONE'))

        gp_ignore = ExpressionNode(1, '<IGNORE>')
        gp_expression.add_node(1, gp_ignore)

        gp_ignore.add_node(2, TerminalNode (2, 'IGNORE'))

        self.diagram_node = nodes.ForNoneBranch(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual(
                '<qCase>\n'
                '<instruction text="IGNORE" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n'
                '</qCase>\n',
                output.getvalue())


class DecideForTest(unittest.TestCase):
    """
    Combined ToCaseNode/ToCaseBranch test for the DECIDE FOR statement
    """
    def setUp(self) -> None:
        gp_decide_for = ExpressionNode(0, '<DECIDE_FOR>')
        gp_decide_for.add_node(1, TerminalNode(1, 'DECIDE'))
        gp_decide_for.add_node(1, TerminalNode(1, 'FOR'))

        gp_decide_which = ExpressionNode(1, '<DECIDE_which>')
        gp_decide_for.add_node(1, gp_decide_which)

        gp_decide_which.add_node(2, TerminalNode(2, 'EVERY'))

        gp_decide_for.add_node(1, TerminalNode(1, 'CONDITION'))

        gp_branches = ExpressionNode(1, '<DECIDE_FOR_conditions>')
        gp_decide_for.add_node(1, gp_branches)

        # First branch
        gp_branch = ExpressionNode(2,'<DECIDE_FOR_branch>')
        gp_decide_for.add_node(2, gp_branch)

        gp_branch.add_node(3, TerminalNode(3, 'WHEN'))

        gp_condition = ExpressionNode(3, '<logical_expression>')
        gp_branch.add_node(3, gp_condition)

        gp_condition.add_node(4, TerminalNode(4, '#FOO'))
        gp_condition.add_node(4, TerminalNode(4, 'EQ'))
        gp_condition.add_node(4, TerminalNode(4, '#BAR'))

        gp_assign = ExpressionNode(3, '<anon_ASSIGN>')
        gp_branch.add_node(3, gp_assign)

        gp_assign.add_node(4, TerminalNode(4, '#C'))
        gp_assign.add_node(4, TerminalNode(4, '='))
        gp_assign.add_node(4, TerminalNode(4, '3'))

        # Second branch
        gp_branch = ExpressionNode(2,'<DECIDE_FOR_branch>')
        gp_decide_for.add_node(2, gp_branch)

        gp_branch.add_node(3, TerminalNode(3, 'WHEN'))

        gp_condition = ExpressionNode(3, '<logical_expression>')
        gp_branch.add_node(3, gp_condition)

        gp_condition.add_node(4, TerminalNode(4, '#BAZ'))
        gp_condition.add_node(4, TerminalNode(4, 'EQ'))
        gp_condition.add_node(4, TerminalNode(4, '123'))

        gp_assign = ExpressionNode(3, '<anon_ASSIGN>')
        gp_branch.add_node(3, gp_assign)

        gp_assign.add_node(4, TerminalNode(4, '#D'))
        gp_assign.add_node(4, TerminalNode(4, '='))
        gp_assign.add_node(4, TerminalNode(4, '4'))

        # None branch
        gp_none = ExpressionNode(2,'<DECIDE_FOR_none>')
        gp_decide_for.add_node(2, gp_none)

        gp_none.add_node(3, TerminalNode(3, 'WHEN'))
        gp_none.add_node(3, TerminalNode(3, 'NONE'))

        gp_ignore = ExpressionNode(3, '<IGNORE>')
        gp_none.add_node(3, gp_ignore)

        gp_ignore.add_node(4, TerminalNode (4, 'IGNORE'))

        self.diagram_node = nodes.ForCaseNode(gp_decide_for, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<case text="&#34;(*)&#34;,&#34;#FOO EQ #BAR&#34;,&#34;#BAZ EQ 123&#34;,&#34;NONE&#34;" comment="DECIDE FOR EVERY CONDITION" color="ffffff">\n'
                             '<qCase>\n'
                             '<instruction text="#C = 3" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n'
                             '</qCase>\n'
                             '<qCase>\n'
                             '<instruction text="#D = 4" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n'
                             '</qCase>\n'
                             '<qCase>\n'
                             '<instruction text="IGNORE" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n'
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

            self.assertEqual('<jump text="ESCAPE" comment="" color="ffff80" rotated="0" disabled="0"></jump>\n',
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

            self.assertEqual(
                '<jump text="REINPUT ''*WARNING*: You have changed the Override field from &#34;&#34;Y&#34;&#34;.''" comment="" color="ffff80" rotated="0" disabled="0"></jump>\n',
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
        self.grammar.add_node(1, gp_control)
        gp_control.add_node(2, TerminalNode(2, '#J'))

        gp_start = ExpressionNode(1, '<constant_integer_pos>')
        self.grammar.add_node(1, gp_start)
        gp_start.add_node(2, TerminalNode(2, '1'))

        gp_to = ExpressionNode(1, '<user_identifier>')
        self.grammar.add_node(1, gp_to)
        gp_to.add_node(2, TerminalNode(2, 'C*SOMETHING'))

        gp_step = ExpressionNode(1, '<constant_integer_neg>')
        self.grammar.add_node(1, gp_step)
        gp_step.add_node(2, TerminalNode(2, '-1'))

        gp_statements = ExpressionNode(1, '<statement_list>')
        self.grammar.add_node(1, gp_statements)
        gp_statements.add_node(2, TerminalNode(2, 'IGNORE'))

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

            self.assertEqual('<for text="FOR #J &#60;- 1 to C*SOMETHING by -1" comment="" color="ffffff">\n'
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

            self.assertEqual(
                '<instruction text="TEST" comment="" color="ffffff" rotated="0" disabled="0"></instruction>\n',
                output.getvalue())


class DatabaseUpdateTest(unittest.TestCase):
    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<UPDATE>')
        gp_expression.add_node(1, TerminalNode(1, 'UPDATE'))
        gp_expression.add_node(1, TerminalNode(1, '('))
        gp_expression.add_node(1, TerminalNode(1, '1234'))
        gp_expression.add_node(1, TerminalNode(1, ')'))

        db_source = ExpressionNode(1, '<UPDATE_source>')
        gp_expression.add_node(1, db_source)

        db_assign_1 = ExpressionNode(2, '<assignment_all>')
        db_source.add_node(2, db_assign_1)

        db_assign_1.add_node(3, TerminalNode(3, 'EXT-RPTGRP-ID'))
        db_assign_1.add_node(3, TerminalNode(3, '='))
        db_assign_1.add_node(3, TerminalNode(3, '#SSN'))

        db_assign_2 = ExpressionNode(2, '<assignment_all>')
        db_source.add_node(2, db_assign_2)

        db_assign_2.add_node(3, TerminalNode(3, 'APPLICANT-NAME'))
        db_assign_2.add_node(3, TerminalNode(3, '='))
        db_assign_2.add_node(3, TerminalNode(3, '#NAME'))

        self.diagram_node = nodes.DatabaseInstruction(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<instruction text="&#34;UPDATE ( 1234 )&#34;,&#34;  EXT-RPTGRP-ID = #SSN&#34;,&#34;  APPLICANT-NAME = #NAME&#34;" comment="" color="80ff80" rotated="0" disabled="0">\n'
                             '</instruction>\n',
                             output.getvalue())


class DatabaseStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<STORE>')
        gp_expression.add_node(1, TerminalNode(1, 'STORE'))
        gp_expression.add_node(1, TerminalNode(1, '('))
        gp_expression.add_node(1, TerminalNode(1, '1234'))
        gp_expression.add_node(1, TerminalNode(1, ')'))

        db_source = ExpressionNode(1, '<STORE_how>')
        gp_expression.add_node(1, db_source)

        db_assign_1 = ExpressionNode(2, '<assignment_all>')
        db_source.add_node(2, db_assign_1)

        db_assign_1.add_node(3, TerminalNode(3, 'EXT-RPTGRP-ID'))
        db_assign_1.add_node(3, TerminalNode(3, '='))
        db_assign_1.add_node(3, TerminalNode(3, '#SSN'))

        db_assign_2 = ExpressionNode(2, '<assignment_all>')
        db_source.add_node(2, db_assign_2)

        db_assign_2.add_node(3, TerminalNode(3, 'APPLICANT-NAME'))
        db_assign_2.add_node(3, TerminalNode(3, '='))
        db_assign_2.add_node(3, TerminalNode(3, '#NAME'))

        self.diagram_node = nodes.DatabaseInstruction(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('<instruction text="&#34;STORE ( 1234 )&#34;,&#34;  EXT-RPTGRP-ID = #SSN&#34;,&#34;  APPLICANT-NAME = #NAME&#34;" comment="" color="80ff80" rotated="0" disabled="0">\n'
                             '</instruction>\n',
                             output.getvalue())


class DBAssignmentTest(unittest.TestCase):

    def setUp(self) -> None:
        db_assign = ExpressionNode(0, '<assignment_all>')

        db_assign.add_node(1, TerminalNode(1, 'EXT-RPTGRP-ID'))
        db_assign.add_node(1, TerminalNode(1, '='))
        db_assign.add_node(1, TerminalNode(1, '#SSN'))

        self.db_node = MagicMock()
        self.assign_node = nodes.DBAssignment(db_assign, self.db_node)

    def test_build(self):
        self.assign_node.import_expressions(StatementFactory)
        self.assign_node.build('assignments')
        self.assertListEqual(['EXT-RPTGRP-ID', '=', '#SSN'], self.assign_node.node_text['instruction'])
        self.db_node.add_text.assert_called_with('assignments', 'EXT-RPTGRP-ID = #SSN')


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


class NullStatementTest(unittest.TestCase):
    def setUp(self) -> None:
        gp_expression = ExpressionNode(0, '<^>')
        gp_terminal = TerminalNode(1, 'TEST')
        gp_expression.add_node(1, gp_terminal)

        self.diagram_node = nodes.NullStatement(gp_expression, None)

    def test_render(self):
        self.diagram_node.import_expressions(StatementFactory)
        self.diagram_node.build('instruction')

        with io.StringIO() as output:
            self.diagram_node.render(output)

            self.assertEqual('', output.getvalue())


if __name__ == '__main__':
    unittest.main()
