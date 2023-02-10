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

from goldparser import grammar
from structorizer.factory import StatementFactory as Factory
from structorizer import nodes


class StatementFactoryTest(unittest.TestCase):
    def test_terminal(self):
        self.assertIsInstance(Factory.terminal(None, None), nodes.DiagramTerminal)

    def test_program(self):
        gp_node = grammar.ExpressionNode(0, '<program>')
        self.assertIsInstance(Factory.node(gp_node, None), nodes.DiagramNode)

    def test_add(self):
        gp_node = grammar.ExpressionNode(1, '<ADD>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_assign(self):
        gp_node = grammar.ExpressionNode(1, '<ASSIGN>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_anon_assign(self):
        gp_node = grammar.ExpressionNode(1, '<anon_ASSIGN>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_callnat(self):
        gp_node = grammar.ExpressionNode(1, '<CALLNAT>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.CallNode)

    def test_compress(self):
        gp_node = grammar.ExpressionNode(1, '<COMPRESS>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_compute(self):
        gp_node = grammar.ExpressionNode(1, '<COMPUTE>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_decide_on(self):
        gp_node = grammar.ExpressionNode(1, '<DECIDE_ON>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.CaseNode)

    def test_decide_on_branch(self):
        gp_node = grammar.ExpressionNode(1, '<DECIDE_ON_branch>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.CaseBranch)

    def test_decide_on_none(self):
        gp_node = grammar.ExpressionNode(1, '<DECIDE_ON_none>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.NoneBranch)

    def test_define_data(self):
        gp_node = grammar.ExpressionNode(1, '<DEFINE_DATA>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_define_window(self):
        gp_node = grammar.ExpressionNode(1, '<DEFINE_WINDOW>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_escape(self):
        gp_node = grammar.ExpressionNode(1, '<ESCAPE>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.ExitNode)

    def test_find_with_loop(self):
        gp_node = grammar.ExpressionNode(1, '<FIND_with_loop>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.DatabaseLoop)

    def test_for(self):
        gp_node = grammar.ExpressionNode(1, '<FOR>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.ForNode)

    def test_get(self):
        gp_node = grammar.ExpressionNode(1, '<GET>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.DatabaseInstruction)

    def test_if_closed(self):
        gp_node = grammar.ExpressionNode(1, '<IF_closed>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.AlternativeNode)

    def test_if_open(self):
        gp_node = grammar.ExpressionNode(1, '<IF_open>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.AlternativeNode)

    def test_input(self):
        gp_node = grammar.ExpressionNode(1, '<INPUT>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_then_closed(self):
        gp_node = grammar.ExpressionNode(1, '<THEN_closed>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.AlternativeTrueNode)

    def test_then_open(self):
        gp_node = grammar.ExpressionNode(1, '<THEN_open>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.AlternativeTrueNode)

    def test_else_closed(self):
        gp_node = grammar.ExpressionNode(1, '<ELSE_closed>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.AlternativeFalseNode)

    def test_else_open(self):
        gp_node = grammar.ExpressionNode(1, '<ELSE_open>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.AlternativeFalseNode)

    def test_ignore(self):
        gp_node = grammar.ExpressionNode(1, '<IGNORE>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_include(self):
        gp_node = grammar.ExpressionNode(1, '<INCLUDE>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_move(self):
        gp_node = grammar.ExpressionNode(1, '<MOVE>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_obtain(self):
        gp_node = grammar.ExpressionNode(1, '<OBTAIN>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_perform(self):
        gp_node = grammar.ExpressionNode(1, '<PERFORM>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.CallNode)

    def test_read(self):
        gp_node = grammar.ExpressionNode(1, '<READ>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.DatabaseLoop)

    def test_reinput(self):
        gp_node = grammar.ExpressionNode(1, '<REINPUT>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.ExitNode)

    def test_repeat(self):
        gp_node = grammar.ExpressionNode(1, '<REPEAT>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.ForeverNode)

    def test_repeat_while(self):
        gp_node = grammar.ExpressionNode(1, '<REPEAT_WHILE>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.WhileNode)

    def test_reset(self):
        gp_node = grammar.ExpressionNode(1, '<RESET>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_subtract(self):
        gp_node = grammar.ExpressionNode(1, '<SUBTRACT>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_set_key(self):
        gp_node = grammar.ExpressionNode(1, '<SET_KEY>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_stack(self):
        gp_node = grammar.ExpressionNode(1, '<STACK>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_store(self):
        gp_node = grammar.ExpressionNode(1, '<STORE>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.DatabaseInstruction)

    def test_update(self):
        gp_node = grammar.ExpressionNode(1, '<UPDATE>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.DatabaseInstruction)

    def test_end(self):
        gp_node = grammar.ExpressionNode(1, '<END>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.InstructionNode)

    def test_null(self):
        gp_node = grammar.ExpressionNode(1, '<^>')
        self.assertIsInstance(Factory.node(gp_node, None),  nodes.NullStatement)


if __name__ == '__main__':
    unittest.main()
