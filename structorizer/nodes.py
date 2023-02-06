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
    color = 'ffffff'

    def __init__(self, gp_node, parent):
        self.gp_node = gp_node      # GrammarNode being rendered by this Statement
        self.parent = parent
        self.gp_children = None     # GP child node generator
        self.child_nodes = []       # Statement nodes corresponding to the GP children

        self.node_text = {}

    def open(self, out_file):
        """
        Generate the opening phrase
        :param out_file:
        :return:
        """
        pass

    def close(self, out_file):
        """
        Generate the closing phrase
        :param out_file:
        :return:
        """
        pass

    def add_text(self, field, text):
        """
        Attempt to add the text for a field. If the node does not know
        the field, it is passed up to the parent.
        :param field: name of the field to set the text for
        :param text: text to add
        :return:
        """
        if self.node_text.get(field) is not None:
            self.node_text[field].append(text)
        elif self.parent:   # Terminals for not yet supported instructions can reach the diagram root and crash
            self.parent.add_text(field, text)

    def _prime_generator(self, gp_node):
        # Removing retrieval of the generator from the render method makes
        # reuse by overriding descendants possible.
        if self.gp_children is None:
            self.gp_children = gp_node.traverse()

    def import_expressions(self, factory):
        """
        Build the Statement nodes for the GP children of this
        node's ExpressionNode.
        :return:
        """
        self._prime_generator(self.gp_node)

        for child in self.gp_children:
            self.child_nodes.append(child.export_node(factory, self))

    def build(self, field):
        """
        Collect any information needed from the child nodes in order
        to successfully create the NSD XML during the render pass.
        :return:
        """
        for child in self.child_nodes:
            child.build(field)

    def matches(self, expression):
        """
        Report if the Statement node expression matches the requested
        expression.
        :param expression: string to match against
        :return: true if the expression matches
        """
        return self.gp_node.matches(expression)

    def render(self, out_file):
        """
        Collect the entities that make up the grammar node. A Statement
        is created for each expression as processing descends the
        grammar tree. When the lowest level is reached, all terminals
        are joined and returned as the outcome of the statement. This
        repeats as execution ascends back up the grammar tree, leading
        to a single line of text for gp_node.
        :param out_file: XML output destination
        :return:
        """
        self.open(out_file)

        for child in self.child_nodes:
            child.render(out_file)

        self.close(out_file)


class DiagramNode(Statement):
    """
    Structorizer diagram node
    """

    def open(self, out_file):
        # TODO: make the program name an attribute
        today = date.today().isoformat()

        print('<?xml version="1.0" encoding="UTF-8"?>', file=out_file)
        print('<root xmlns:nsd="https://structorizer.fisch.lu" version="3.30-12" '
              'preRepeat="until " postFor="to" preReturn="return" postForIn="in" preWhile="while " '
              'output="OUTPUT" input="INPUT" preFor="for" preExit="exit" preLeave="leave" ignoreCase="true" '
              'preThrow="throw" preForIn="foreach" stepFor="by" author="sven" created="{}" '
              'changedby="" changed="" origin="GPStruct" '
              'text="{}" comment="" color="{color}" type="program" style="nice">'.format(today,
                                                                                         'PROGRAM',
                                                                                         color=self.color),
              file=out_file)
        print('  <children>', file=out_file)

    def close(self, out_file):
        print('  </children>', file=out_file)
        print('</root>', file=out_file)


class ExitNode(Statement):
    """
    Structorizer Exit node
    """
    color = 'ffff80'

    def __init__(self, gp_node, parent):
        super().__init__(gp_node, parent)

        self.node_text['instruction'] = []

    def open(self, out_file):
        # Instructions contain no other elements so the closing tag is included.
        print('<jump text="{instruction}" comment="" color="{color}" rotated="0" disabled="0">'.format(
            instruction=' '.join(self.node_text['instruction']),
            color=self.color),
            file=out_file)

    def close(self, out_file):
        print('</jump>', file=out_file)

class ForNode(Statement):
    """
    FOR statement outer XML element
    """

    def __init__(self, gp_node, parent):
        super().__init__(gp_node, parent)

        self.node_text['instruction'] = []
        self.node_text['for_control'] = []
        self.node_text['for_from'] = []
        self.node_text['for_to'] = []

    def open(self, out_file):
        # for uses &#60; (less than) to separate the loop variable from the values
        print('<for text="{instruction} {for_control} &#60;- {for_from} {for_to}" comment="" color="{color}">'.format(
            instruction=' '.join(self.node_text['instruction']),
            for_control=' '.join(self.node_text['for_control']),
            for_from=' '.join(self.node_text['for_from']),
            for_to=' '.join(self.node_text['for_to']),
            color=self.color))
        print('  <qFor>')

    def close(self, out_file):
        print('  </qFor>')
        print('</for>')

    def build(self, field):
        """
        Collect the parts that make up the FOR instruction
        :param field:
        :return:
        """
        # A trimmed tree does not have any indication of what is coming
        # for the required parts
        # TODO: support for the optional STEP
        child = self.child_nodes[0]  # FOR terminal
        child.build('instruction')

        child = self.child_nodes[1]  # loop variable
        child.build('for_control')

        child = self.child_nodes[2]  # start value
        child.build('for_from')

        child = self.child_nodes[3]  # end value
        child.build('for_to')

    def render(self, factory, gp_node):
        """
        Find the various parts that make up the FOR statement controls
        and assemble the element text.
        :param factory:
        :param gp_node:
        :return:
        """
        self._prime_generator(gp_node)      # Initialize the GP node generator
        # <FOR> ::= FOR <variable_l_scalar> <FOR_from> <FOR_to> <FOR_operand>

        # Untrimmed tree contains variable_l_scalar, FOR_from, FOR_to and statement_list
        # Trimmed version may only have the final types of the three loop control fields
        # and may not have an explicit statement_list.
        # -> first child after FOR is the loop variable, 2nd is the starting value, 3rd
        # is the end value.

        child = next(self.gp_children)      # FOR terminal
        self.add_text('instruction', child.render(factory, self))

        child = next(self.gp_children)      # loop variable
        self.add_text('for_control', child.render(factory, self))

        child = next(self.gp_children)      # start value
        self.add_text('for_from', child.render(factory, self))

        child = next(self.gp_children)      # end value
        self.add_text('for_to', child.render(factory, self))

        # TODO: handle step

        self.open(out_file)  # Output FOR statement with the current contents of node_text

        self.node_text['instruction'] = [child.render(out_file)]  # Restart with the first statement_list
        super().render(out_file)
        self.close(out_file)

        return ''       # The node text has been printed, so we return an empty string


class ForeverNode(Statement):
    """
    FOREVER statement outer XML element
    """
    def open(self, out_file):
        print('<forever comment="" color="{color}">'.format(color=self.color), file=out_file)
        print('  <qForever>', file=out_file)

    def close(self, out_file):
        print('  </qForever>', file=out_file)
        print('</forever>', file=out_file)


class WhileNode(Statement):
    """
    WHILE statement outer XML element
    """

    def __init__(self, gp_node, parent):
        super().__init__(gp_node, parent)

        self.node_text['instruction'] = []

    def open(self, out_file):
        print('<while text="{}" comment="" color="{color}">'.format(
            ' '.join(self.node_text['instruction']), color=self.color), file=out_file)
        print('  <qWhile>', file=out_file)

    def close(self, out_file):
        print('  </qWhile>', file=out_file)
        print('</while>', file=out_file)

    def build(self, field):
        """
        Collect the terminals that make up the text for the instruction
        :return:
        """
        for child in self.child_nodes:
            if child.matches('<loop_statement_list>'):
                break

            child.build('instruction')


class DatabaseLoop(WhileNode):
    color = '80ff80'        # Green


class AlternativeNode(Statement):
    """
    IF statement outer XML element
    """

    def __init__(self, gp_node, parent):
        super().__init__(gp_node, parent)

        self.node_text['instruction'] = []

    # Problem: logical expression starts at the same level as IF
    def open(self, out_file):
        print('<alternative text="{}" comment="" color="{color}">'.format(
            ' '.join(self.node_text['instruction']), color=self.color))

    def close(self, out_file):
        print('</alternative>')

    def build(self, field):
        """
        Collect the parts that make up the logical expression
        :return:
        """
        # [0] contains the IF terminal, which Structorizer does not need
        for child in self.child_nodes:
            if child.matches('<logical_expression>'):
                break
        # This is (should be...) the logical expression.
        child.build('instruction')

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
        self.node_text['instruction'] = [expression.render(factory, self)]

        # This is (should be...) the logical expression.
        expression = next(self.gp_children)
        self.node_text['instruction'] = [expression.render(factory, self)]   # list for consistency

        self.open()                             # This embeds the expression in the element open statement

        self.node_text['instruction'] = []      # Start over for the qTrue/qFalse branches
        super().render(factory, gp_node)        # Process remaining gp_node children

        self.close()

        return ''       # The node text has been printed so we return an empty string


class AlternativeTrueNode(Statement):
    """
    Alternative statement True branch
    """
    def open(self, out_file):
        print('<qTrue>')

    def close(self, out_file):
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
    def open(self, out_file):
        print('<qFalse>')

    def close(self, out_file):
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

    def __init__(self, gp_node, parent):
        super().__init__(gp_node, parent)

        self.node_text['instruction'] = []

    def open(self, out_file):
        # Instructions contain no other elements so the closing tag is included.
        print('<instruction text="{}" comment="" color="{color}" rotated="0" disabled="0">'
              '</instruction>'.format(' '.join(self.node_text['instruction']), color=self.color))

    def render(self, factory, gp_node):
        super().render(factory, gp_node)
        self.open()

        return ''       # The node text has been printed so we return an empty string


class CallNode(InstructionNode):
    """
    Node for subroutine calls. It is a non-container instruction with
    a distinct rendering.
    """

    def __init__(self, gp_node, parent):
        super().__init__(gp_node, parent)

        self.node_text['instruction'] = []

    def open(self, out_file):
        # Calls contain no other elements so the closing tag is included.
        print('<call text="{}" comment="" color="{color}" rotated="0" disabled="0">'
              '</call>'.format(' '.join(self.node_text['instruction']), color=self.color))


class DatabaseInstruction(InstructionNode):
    color = '80ff80'        # Green


class DiagramTerminal(Statement):
    """
    Diagram equivalent of the grammar side DiagramTerminal
    """
    def build(self, field):
        """
        Pass the contents of the GrammarNode terminal to the parent
        Statement.
        :param field:
        :return:
        """
        self.parent.add_text(field, self.gp_node.render(None, None))
