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

from structorizer.factory import StatementFactory as Factory
from structorizer import nodes


class StatementFactoryTest(unittest.TestCase):
    def test_terminal(self):
        self.assertIsInstance(Factory.terminal('test', None), nodes.DiagramTerminal)

    def test_program(self):
        self.assertIsInstance(Factory.node('<program>', None), nodes.DiagramNode)

    def test_add(self):
        self.assertIsInstance(Factory.node('<ADD>', None),  nodes.InstructionNode)

    def test_assign(self):
        self.assertIsInstance(Factory.node('<ASSIGN>', None),  nodes.InstructionNode)

    def test_anon_assign(self):
        self.assertIsInstance(Factory.node('<anon_ASSIGN>', None),  nodes.InstructionNode)

    def test_callnat(self):
        self.assertIsInstance(Factory.node('<CALLNAT>', None),  nodes.CallNode)

    def test_compress(self):
        self.assertIsInstance(Factory.node('<COMPRESS>', None),  nodes.InstructionNode)

    def test_define_data(self):
        self.assertIsInstance(Factory.node('<DEFINE_DATA>', None),  nodes.InstructionNode)

    def test_define_window(self):
        self.assertIsInstance(Factory.node('<DEFINE_WINDOW>', None),  nodes.InstructionNode)

    def test_escape(self):
        self.assertIsInstance(Factory.node('<ESCAPE>', None),  nodes.ExitNode)

    def test_find_with_loop(self):
        self.assertIsInstance(Factory.node('<FIND_with_loop>', None),  nodes.DatabaseLoop)

    def test_for(self):
        self.assertIsInstance(Factory.node('<FOR>', None),  nodes.ForNode)

    def test_get(self):
        self.assertIsInstance(Factory.node('<GET>', None),  nodes.DatabaseInstruction)

    def test_if_closed(self):
        self.assertIsInstance(Factory.node('<IF_closed>', None),  nodes.AlternativeNode)

    def test_if_open(self):
        self.assertIsInstance(Factory.node('<IF_open>', None),  nodes.AlternativeNode)

    def test_input(self):
        self.assertIsInstance(Factory.node('<INPUT>', None),  nodes.InstructionNode)

    def test_then_closed(self):
        self.assertIsInstance(Factory.node('<THEN_closed>', None),  nodes.AlternativeTrueNode)

    def test_then_open(self):
        self.assertIsInstance(Factory.node('<THEN_open>', None),  nodes.AlternativeTrueNode)

    def test_else_closed(self):
        self.assertIsInstance(Factory.node('<ELSE_closed>', None),  nodes.AlternativeFalseNode)

    def test_else_open(self):
        self.assertIsInstance(Factory.node('<ELSE_open>', None),  nodes.AlternativeFalseNode)

    def test_ignore(self):
        self.assertIsInstance(Factory.node('<IGNORE>', None),  nodes.InstructionNode)

    def test_include(self):
        self.assertIsInstance(Factory.node('<INCLUDE>', None),  nodes.InstructionNode)

    def test_move(self):
        self.assertIsInstance(Factory.node('<MOVE>', None),  nodes.InstructionNode)

    def test_perform(self):
        self.assertIsInstance(Factory.node('<PERFORM>', None),  nodes.CallNode)

    def test_read(self):
        self.assertIsInstance(Factory.node('<READ>', None),  nodes.DatabaseLoop)

    def test_repeat(self):
        self.assertIsInstance(Factory.node('<REPEAT>', None),  nodes.ForeverNode)

    def test_reset(self):
        self.assertIsInstance(Factory.node('<RESET>', None),  nodes.InstructionNode)

    def test_subtract(self):
        self.assertIsInstance(Factory.node('<SUBTRACT>', None),  nodes.InstructionNode)

    def test_set_key(self):
        self.assertIsInstance(Factory.node('<SET_KEY>', None),  nodes.InstructionNode)

    def test_store(self):
        self.assertIsInstance(Factory.node('<STORE>', None),  nodes.DatabaseInstruction)

    def test_update(self):
        self.assertIsInstance(Factory.node('<UPDATE>', None),  nodes.DatabaseInstruction)

    def test_end(self):
        self.assertIsInstance(Factory.node('<END>', None),  nodes.InstructionNode)


if __name__ == '__main__':
    unittest.main()
