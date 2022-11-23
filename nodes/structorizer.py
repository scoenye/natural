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

from nodes import core
from datetime import date


class DiagramNode(core.CompositeNode):
    """
    Structorizer diagram node
    """

    def _render_open(self):
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

    def _render_close(self):
        print('  </children>')
        print('</root>')


class InstructionNode(core.CompositeNode):
    def _render_open(self):
        # Suppress the instruction if it does not contain any terminals
        if self.terminals:
            # Instructions contain no other elements so the closing tag is included.
            print('<instruction text="&#34;{}&#34;" comment="" color="ffffff" rotated="0" disabled="0">'
                  '</instruction>'.format(' '.join(self.terminals)))
