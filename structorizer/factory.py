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

from structorizer import nodes


class StatementFactory:
    """
    Create a TreeNode for a GP parse tree instruction part
    """

    nodes = {
        'program': nodes.DiagramNode,
        'ADD': nodes.InstructionNode,
        'ASSIGN': nodes.InstructionNode,
        'anon_ASSIGN': nodes.InstructionNode,
        'CALLNAT': nodes.CallNode,
        'COMPRESS': nodes.InstructionNode,
        'COMPUTE': nodes.InstructionNode,
        'DECIDE_ON': nodes.CaseNode,
        'DECIDE_ON_branch': nodes.CaseBranch,
        'DECIDE_ON_none': nodes.NoneBranch,
        'DEFINE_DATA': nodes.InstructionNode,
        'DEFINE_WINDOW': nodes.InstructionNode,
        'DEFINE_SUBROUTINE': nodes.WhileNode,
        'ESCAPE': nodes.ExitNode,
        'FETCH': nodes.ExternalExitNode,
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
        'OBTAIN': nodes.InstructionNode,
        'PERFORM': nodes.CallNode,
        'READ': nodes.DatabaseLoop,
        'REINPUT': nodes.ExitNode,
        'REDEFINE': nodes.NullStatement,
        'REPEAT': nodes.ForeverNode,
        'REPEAT_WHILE': nodes.WhileNode,
        'RESET': nodes.InstructionNode,
        'SET_KEY': nodes.InstructionNode,
        'SUBTRACT': nodes.InstructionNode,
        'STACK': nodes.InstructionNode,
        'STORE': nodes.DatabaseInstruction,         # TODO: place assignments on separate lines
        'UPDATE': nodes.DatabaseInstruction,        # TODO: place assignments on separate lines
        'END': nodes.InstructionNode,
        '^': nodes.NullStatement
    }

    @staticmethod
    def node(gp_node, parent):
        """
        Produce a diagram node for a GP instruction. If no matching
        node can be found, a base Statement node is returned.
        :param gp_node: GrammarNode to render
        :param parent: diagram node above the node being created
        :return:
        """
        temp_node = StatementFactory.nodes.get(gp_node.lvalue())

        if temp_node is None:
            return nodes.Statement(gp_node, parent)  # The null renderer
        else:
            return temp_node(gp_node, parent)

    @staticmethod
    def terminal(gp_node, parent):
        """
        Produce a TreeNode for a GP instruction. If no matching
        node can be found, an instruction node is returned.
        :param gp_node:
        :param parent: diagram node above the node being created
        :return:
        """
        terminal = nodes.DiagramTerminal(gp_node, parent)

        return terminal

