'''
Parser and AST builder for TAPPS commandline.

Date created: 12th November 2015

Copyright (C) 2015, Maurice HT Ling

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from ply import lex

class TAPPSLexer(object):

    reserved = {'as': 'AS',
                'asthistory': 'ASTHISTORY',
                'csv': 'CSV',
                'displayast': 'DISPLAYAST',
                'environment': 'ENVIRONMENT',
                'history': 'HISTORY',
                'list': 'LIST',
                'load': 'LOAD',
                'plugin': 'PLUGIN',
                'set': 'SET',
                'show': 'SHOW',
       # 'insert' : 'INSERT', 
       # 'into'   : 'INTO',
       # 'select' : 'SELECT',
       # 'from'   : 'FROM',
       # 'where'  : 'WHERE',
       # 'order'  : 'ORDER',
       # 'by'     : 'BY',
       # 'values' : 'VALUES',
       # 'and'    : 'AND',
       # 'or'     : 'OR',
       # 'not'    : 'NOT',
                } 
              
    tokens = ['NUMBER',
              'FOLDER',
              'FILENAME',
              'ID', 
              'STRING',
              'COMMA', 
              'SEMICOLON',
              # 'PLUS', 
              # 'MINUS',
              # 'TIMES',      
              # 'DIVIDE',
              # 'LPAREN',     
              # 'RPAREN',
              # 'GT', 
              # 'GE',
              # 'LT',
              # 'LE',
              # 'EQ',
              # 'NE', 
              ] + list(reserved.values())
    
    def t_NUMBER(self, t):
        # TODO: see http://docs.python.org/reference/lexical_analysis.html
        # for what Python accepts, then use eval
        r'\d+'
        t.value = int(t.value)    
        return t
        
    def t_FOLDER(self, t):
        r'([A-Za-z]:(/[A-Za-z0-9]+)*)|((/[A-Za-z0-9]+)+)'
        return t
        
    def t_FILENAME(self, t):
        r'[A-Za-z0-9_\-]+(\.[A-Za-z0-9_\-]+)+'
        return t
        
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = TAPPSLexer.reserved.get(t.value,'ID')    # Check for reserved words
        # redis is case sensitive in hash keys but we want the sql to be case insensitive,
        # so we lowercase identifiers 
        t.value = t.value.lower()
        return t
    
    def t_STRING(self, t):
        # TODO: unicode...
        # Note: this regex is from pyparsing, 
        # see http://stackoverflow.com/questions/2143235/how-to-write-a-regular-expression-to-match-a-string-literal-where-the-escape-is
        # TODO: may be better to refer to http://docs.python.org/reference/lexical_analysis.html 
        '(?:"(?:[^"\\n\\r\\\\]|(?:"")|(?:\\\\x[0-9a-fA-F]+)|(?:\\\\.))*")|(?:\'(?:[^\'\\n\\r\\\\]|(?:\'\')|(?:\\\\x[0-9a-fA-F]+)|(?:\\\\.))*\')'
        t.value = eval(t.value) 
        #t.value[1:-1]
        return t
        
    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno = t.lexer.lineno + len(t.value)
    
    t_ignore  = ' \t'
    
    # Regular expression rules for simple tokens
    t_COMMA = r'\,'
    t_SEMICOLON = r';'
    # t_PLUS = r'\+'
    # t_MINUS = r'-'
    # t_TIMES = r'\*'
    # t_DIVIDE = r'/'
    # t_LPAREN = r'\('
    # t_RPAREN = r'\)'
    # t_GT = r'>'
    # t_GE = r'>='
    # t_LT = r'<'
    # t_LE = r'<='
    # t_EQ = r'='
    # t_NE = r'!='
    
    def t_error(self, t):
        raise TypeError("Unknown text '%s'" % (t.value,))

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    def test(self):
        while True:
            text = raw_input('TAPPSLex:> ').strip()
            if text.lower() in ['exit', 'quit']:
                break
            self.lexer.input(text)
            while True:
                tok = self.lexer.token()
                if not tok: 
                    break
                print tok
                
def unittest_lexer():
    l = TAPPSLexer()
    l.build()
    l.test()

if __name__ == "__main__":    
    unittest_lexer()