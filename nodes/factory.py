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
from nodes import structorizer


class TreeNodeFactory:
    """
    Create a TreeNode for a GP parse tree instruction part
    """
    nodes = {
        'program': structorizer.DiagramNode
    }

    @staticmethod
    def node(gp_part):
        """
        Produce a TreeNode for a GP instruction. If no matching
        node can be found, an instruction node is returned.
        :param gp_part:
        :return:
        """
        temp_node = TreeNodeFactory.nodes.get(gp_part)

        if temp_node is None:
            return structorizer.InstructionNode()
        else:
            return temp_node()
