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
import re

from structorizer import nodes


class StatementFactory:
    """
    Create a TreeNode for a GP parse tree instruction part
    """
    expression_l = re.compile(r'<(.+)>')

    nodes = {
        'program': nodes.DiagramNode,
        'ADD': nodes.InstructionNode,
        'ASSIGN': nodes.InstructionNode,
        'anon_ASSIGN': nodes.InstructionNode,
        'CALLNAT': nodes.CallNode,
        'COMPRESS': nodes.InstructionNode,
        'DEFINE_DATA': nodes.InstructionNode,
        'DEFINE_WINDOW': nodes.InstructionNode,
#        'DEFINE_SUBROUTINE': nodes.InstructionNode,
        'ESCAPE': nodes.ExitNode,
        'FIND_with_loop': nodes.DatabaseLoop,
        'FOR': nodes.ForNode,
        'GET': nodes.DatabaseInstruction,
        'IF_closed': nodes.AlternativeNode,
        'IF_open': nodes.AlternativeNode,
        'INPUT': nodes.InstructionNode,
        'THEN_closed': nodes.AlternativeTrueNode,
        'THEN_open': nodes.AlternativeTrueNode,
        'ELSE_closed': nodes.AlternativeFalseNode,
        'ELSE_open': nodes.AlternativeFalseNode,
        'IGNORE': nodes.InstructionNode,
        'INCLUDE': nodes.InstructionNode,
        'MOVE': nodes.InstructionNode,
        'PERFORM': nodes.CallNode,
        'READ': nodes.DatabaseLoop,
#        'REDEFINE': nodes.InstructionNode,
        'REPEAT': nodes.ForeverNode,
        'RESET': nodes.InstructionNode,
        'SUBTRACT': nodes.InstructionNode,
        'SET_KEY': nodes.InstructionNode,
        'STORE': nodes.DatabaseInstruction,         # TODO: place assignments on separate lines
        'UPDATE': nodes.DatabaseInstruction,        # TODO: place assignments on separate lines
        'END': nodes.InstructionNode
    }

    @staticmethod
    def node(gp_part, parent):
        """
        Produce a diagram node for a GP instruction. If no matching
        node can be found,  node is returned.
        :param gp_part:
        :param parent: diagram node above the node being created
        :return:
        """
        lvalue = StatementFactory.expression_l.match(gp_part)

        temp_node = StatementFactory.nodes.get(lvalue.group(1))

        if temp_node is None:
            return nodes.Statement(parent)    # The null renderer
        else:
            return temp_node(parent)

    @staticmethod
    def terminal(gp_part, parent):
        """
        Produce a TreeNode for a GP instruction. If no matching
        node can be found, an instruction node is returned.
        :param gp_part:
        :param parent: diagram node above the node being created
        :return:
        """
        terminal = nodes.DiagramTerminal(parent)
        terminal.add_text('instruction', gp_part)

        return terminal

