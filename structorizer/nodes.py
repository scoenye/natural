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

from datetime import date


class Statement:
    def __init__(self):
        self.node_text = []
        self.gp_children = None

    def open(self):
        """
        Generate the opening phrase
        :return:
        """
        pass

    def close(self):
        """
        Generate the closing phrase
        :return:
        """
        pass

    def _prime_generator(self, gp_node):
        # Removing retrieval of the generator from the render method makes
        # reuse by overriding descendants possible.
        if self.gp_children is None:
            self.gp_children = gp_node.traverse()

    def render(self, factory, gp_node):
        """
        Collect the entities that make up the grammar node. A Statement
        is created for each expression as processing descends down the
        grammar tree. When the lowest level is reached, all terminals
        are joined and returned as the outcome of the statement. This
        repeats as execution ascends back up the grammar tree, leading
        to a single line of text for gp_node.
        :param factory:
        :param gp_node:
        :return:
        """
        self._prime_generator(gp_node)

        for child in self.gp_children:
            child_content = child.render(factory)
            if child_content:
                self.node_text.append(child_content)

        return ' '.join(self.node_text)


class DiagramNode(Statement):
    """
    Structorizer diagram node
    """

    def open(self):
        # TODO: make the program name an attribute
        today = date.today().isoformat()

        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<root xmlns:nsd="https://structorizer.fisch.lu" version="3.30-12" '
              'preRepeat="until " postFor="to" preReturn="return" postForIn="in" preWhile="while " '
              'output="OUTPUT" input="INPUT" preFor="for" preExit="exit" preLeave="leave" ignoreCase="true" '
              'preThrow="throw" preForIn="foreach" stepFor="by" author="sven" created="{}" '
              'changedby="" changed="" origin="GPStruct" '
              'text="{}" comment="" color="ffffff" type="program" style="nice">'.format(today, 'PROGRAM'))
        print('  <children>')

    def close(self):
        print('  </children>')
        print('</root>')

    def render(self, factory, gp_node):
        self.open()
        super().render(factory, gp_node)
        self.close()

        return ''       # The node text has been printed so we return an empty string


class WhileNode(Statement):
    """
    Shell of the WHILE statement
    """
    def open(self):
        print('<while text="{}" comment="" color="ffffff">'.format(' '.join(self.node_text)))
        print('  <qWhile>')

    def close(self):
        print('  </qWhile>')
        print('</while>')

    def render(self, factory, gp_node):
        """
        Natural database statements are represented with WHILE nodes.
        The header has many optional clauses but the loop contents
        start with a loop_statement_list expression. This implementation
        collects and renders all clauses up to the statement list as the
        text of the WHILE node.
        :param factory:
        :param gp_node:
        :return:
        """
        self._prime_generator(gp_node)

        # Roll up everything until <loop_statement_list> is encountered? That one is always present.
        # TODO: evaluate with an empty loop
        for child in self.gp_children:
            if child.matches('<loop_statement_list>'):
                break
            child_content = child.render(factory)
            if child_content:
                self.node_text.append(child_content)

        self.open()     # Output loop statement with the current contents of node_text

        self.node_text = [child.render(factory)]    # Restart with the first loop_statement_list
        super().render(factory, gp_node)
        self.close()

        return ''       # The node text has been printed so we return an empty string


class AlternativeNode(Statement):
    """
    Shell of the IF statement
    """

    # Problem: logical expression starts at the same level as IF
    def open(self):
        print('<alternative text="{}" comment="" color="ffffff">'.format(' '.join(self.node_text)))

    def close(self):
        print('</alternative>')

    def render(self, factory, gp_node):
        # Problem: the logical expression is needed by open() but it is not known at this time.
        # super() will collect it, but will also inject any child instructions first. Not very usable.
        # Out on a limb: the first child node is the IF statement itself, the 2nd the expression.
        # Hack our way out: drop the 1st child (also takes care of the unwanted IF), process the
        # 2nd child here.
        self._prime_generator(gp_node)

        # Collect the <IF> expression - contains the IF terminal
        expression = next(self.gp_children)
        # Although not necessary, keep node_text a list in order to maintain consistency
        self.node_text = [expression.render(factory)]

        # This is (should be...) the logical expression.
        expression = next(self.gp_children)
        self.node_text = [expression.render(factory)]   # list for consistency

        self.open()                             # This embeds the expression in the element open statement

        self.node_text = []                     # Start over for the qTrue/qFalse branches
        super().render(factory, gp_node)        # Process remaining gp_node children

        self.close()

        return ''       # The node text has been printed so we return an empty string


class AlternativeTrueNode(Statement):
    """
    Alternative statement True branch
    """
    def open(self):
        print('<qTrue>')

    def close(self):
        print('</qTrue>')

    def render(self, factory, gp_node):
        self.open()
        super().render(factory, gp_node)
        self.close()

        return ''       # The node text has been printed so we return an empty string


class AlternativeFalseNode(Statement):
    """
    Alternative statement False branch
    """
    def open(self):
        print('<qFalse>')

    def close(self):
        print('</qFalse>')

    def render(self, factory, gp_node):
        self.open()
        super().render(factory, gp_node)
        self.close()

        return ''       # The node text has been printed so we return an empty string


class InstructionNode(Statement):
    """
    Node for non-container instructions. Instructions can be made up of
    multiple parser lines. The terminals for all parser lines are
    concatenated and returned as the content.
    """
    def open(self):
        # Instructions contain no other elements so the closing tag is included.
        print('<instruction text="&#34;{}&#34;" comment="" color="ffffff" rotated="0" disabled="0">'
              '</instruction>'.format(' '.join(self.node_text)))

    def render(self, factory, gp_node):
        super().render(factory, gp_node)
        self.open()

        return ''       # The node text has been printed so we return an empty string


class CallNode(InstructionNode):
    """
    Node for subroutine calls. It is a non-container instruction with
    a distinct rendering.
    """
    def open(self):
        # Calls contain no other elements so the closing tag is included.
        print('<call text="{}" comment="" color="ffffff" rotated="0" disabled="0">'
              '</call>'.format(' '.join(self.node_text)))
