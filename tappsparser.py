'''
Parser for TAPPS commandline.

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

from ply import yacc

from tappslexer import TAPPSLexer

        
class TAPPSParser(object):
    
    tokens = TAPPSLexer.tokens
    lexer = TAPPSLexer().build()
    
    # precedence = (
        # ('left', 'OR'),
        # ('left', 'AND'),
        # ('left', 'NOT'),
        # ('left', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
        # ('left', 'PLUS', 'MINUS'),
        # ('left', 'TIMES', 'DIVIDE'),
        # )
            
    def p_statement(self, p):
        '''
        statement : set_statement
                  | load_statement
                  | cast_statement
                  | show_statement
                  | describe_statement
                  | shell_statement
                  | new_statement
                  | delete_statement
                  | select_statement
                  | runplugin_statement
        '''
        p[0] = p[1]
    
    def p_set_statement(self, p):
        '''
        set_statement : SET DISPLAYAST ID
                      | SET CWD FOLDER
                      | SET SEPARATOR separators
                      | SET FILLIN fillin_options
                      | SET PARAMETER ID IN ID AS ID
                      | SET PARAMETER DATAFRAME IN ID AS ID
        '''
        if p[2].lower() == 'displayast': p[0] = ('set', 'displayast', p[3])
        if p[2].lower() == 'cwd': p[0] = ('set', 'cwd', p[3])
        if p[2].lower() == 'separator': p[0] = ('set', 'separator', p[3])
        if p[2].lower() == 'fillin': p[0] = ('set', 'fill-in', p[3])
        if p[2].lower() == 'parameter': 
            p[0] = ('set', 'parameter', p[3], p[5], p[7])
    
    def p_fillin_options(self, p):
        '''
        fillin_options : NUMBER
                       | ID
        '''
        p[0] = p[1]
        
    def p_separator(self, p):
        '''
        separators : DELIMITER
                   | COMMA
                   | COLON
                   | SEMICOLON
                   | RIGHTSLASH
                   | BAR
                   | DOT
                   | PLUS
                   | MINUS
                   | TIMES
                   | DIVIDE
                   | GT
                   | LT
        '''
        p[0] = p[1]
        
    def p_load_statement(self, p):
        '''
        load_statement : LOAD CSV FILENAME AS ID
                       | LOAD NOHEADER CSV FILENAME AS ID
        '''
        if p[2].lower() == 'csv': 
            p[0] = ('loadcsv1', p[3], p[5])
        if p[2].lower() == 'noheader' and p[3].lower() == 'csv': 
            p[0] = ('loadcsv2', p[4], p[65])
    
    def p_cast_statement(self, p):
        '''
        cast_statement : CAST id_list IN ID AS datatype
        '''
        p[0] = ('cast', p[6], p[4], p[2])
    
    def p_datatype(self, p):
        '''
        datatype : ALPHA
                 | NONALPHA
                 | FLOAT
                 | REAL
                 | INTEGER
        '''
        p[0] = p[1]
        
    def p_show_statement(self, p):
        '''
        show_statement : SHOW ASTHISTORY
                       | SHOW ENVIRONMENT
                       | SHOW HISTORY
                       | SHOW PLUGIN LIST 
                       | SHOW PLUGIN ID 
                       | SHOW SESSION
                       | SHOW DATAFRAME
                       | SHOW PARAMETER
        '''
        if p[2].lower() == 'asthistory': p[0] = ('show', 'asthistory')
        if p[2].lower() == 'environment': p[0] = ('show', 'environment')
        if p[2].lower() == 'history': p[0] = ('show', 'history')
        if p[2].lower() == 'plugin': 
            if p[3].lower() == 'list': p[0] = ('show', 'pluginlist')
            else: p[0] = ('show', 'plugindata', p[3])
        if p[2].lower() == 'session': p[0] = ('show', 'session')
        if p[2].lower() == 'dataframe': p[0] = ('show', 'dataframe')
        if p[2].lower() == 'parameter': p[0] = ('show', 'parameter')
    
    def p_describe_statement(self, p):
        '''
        describe_statement : DESCRIBE ID
        '''
        p[0] = ('describe', p[2])
        
    def p_shell_statement(self, p):
        '''
        shell_statement : PYTHONSHELL
        '''
        if p[1].lower() == 'pythonshell': p[0] = ('pythonshell',)
        
    def p_new_statement(self, p):
        '''
        new_statement : NEW ID PARAMETER AS ID
                      | NEW ID DATAFRAME FROM ID plocation
        '''
        if p[3].lower() == 'parameter': 
            p[0] = ('newparam', p[2], p[5])
        if p[3].lower() == 'dataframe' and p[4].lower() == 'from': 
            p[0] = ('newdataframe', p[2], p[5], p[6])
    
    def p_delete_statement(self, p):
        '''
        delete_statement : DELETE DATAFRAME ID
                         | DELETE PARAMETER ID
        '''
        if p[2].lower() == 'dataframe': 
            p[0] = ('deldataframe', p[3])
        if p[2].lower() == 'parameter': 
            p[0] = ('delparam', p[3])
        
    def p_plocation(self, p):
        '''
        plocation : RESULTS
                  | DATAFRAME
        '''
        p[0] = p[1]
    
    def p_select_statement(self, p):
        '''
        select_statement : SELECT FROM ID AS ID
                         | SELECT FROM ID AS ID WHERE binop value
                         | SELECT FROM ID AS ID WHERE ID binop value
        '''
        if len(p) == 6:
            p[0] = ('duplicateframe', p[3], p[5])
        if len(p) == 9:
            p[0] = ('greedysearch', p[3], p[5], p[7], p[8])
        if len(p) == 10:
            p[0] = ('idsearch', p[3], p[5], p[7], p[8], p[9])
    
    def p_binop(self, p):
        '''
        binop : DELIMITER
              | GE
              | LE
              | EQ
              | NE
        '''
        p[0] = p[1]
        
    def p_id_list(self, p):
        '''
        id_list : ALL
                | ID
                | id_list DELIMITER ID
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        if len(p) > 2:
            p[0] = p[1] + [p[3]]
        
    def p_value(self, p):
        '''
        value : number_value
              | id_value
        '''
        p[0] = p[1]
        
    def p_number_value(self, p):
        '''
        number_value : NUMBER
        '''
        p[0] = float(p[1])
        
    def p_id_value(self, p):
        '''
        id_value : ID
                 | STRING
        '''
        p[0] = str(p[1])
            
    def p_runplugin_statement(self, p):
        '''
        runplugin_statement : RUNPLUGIN ID
        '''
        p[0] = ('runplugin', p[2])
            
    #def p_error(self, p):
    #    print "Syntax error in input" # TODO: at line %d, pos %d!" % (p.lineno)
    
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, statement, print_ast=False):
        result = self.parser.parse(statement, lexer=self.lexer)
        if print_ast: print "parse result -> ", result
        return result
        
    def test(self):
        while True:
            text = raw_input('TAPPS:> ').strip() 
            if text.lower() in ['exit', 'quit']: return 0
            if text: self.parse(text, True)
        
        
def unittest_parser():
    p = TAPPSParser()
    p.build()
    p.test()
    
if __name__ == '__main__':
    unittest_parser()
              