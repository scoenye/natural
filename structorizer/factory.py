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
        'DEFINE_DATA': nodes.InstructionNode,
        'END': nodes.InstructionNode
    }

    @staticmethod
    def node(gp_part):
        """
        Produce a TreeNode for a GP instruction. If no matching
        node can be found, an instruction node is returned.
        :param gp_part:
        :return:
        """
        lvalue = StatementFactory.expression_l.match(gp_part)

        temp_node = StatementFactory.nodes.get(lvalue.group(1))

        if temp_node is None:
            return nodes.Statement()    # The null renderer
        else:
            return temp_node()
