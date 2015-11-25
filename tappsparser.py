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
    
    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'NOT'),
        ('left', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        )
            
    def p_statement(self, p):
        '''
        statement : set_statement
                  | load_statement
                  | show_statement
                  | insert_statement
                  | select_statement
        '''
        p[0] = p[1]
    
    def p_set_statement(self, p):
        '''
        set_statement : SET DISPLAYAST ID SEMICOLON
                      | SET DISPLAYAST ID
        '''
        if p[2].lower() == 'displayast':
            p[0] = ('set', 'displayast', p[3])
            
    def p_load_statement(self, p):
        '''
        load_statement : LOAD CSV FILENAME AS ID SEMICOLON
                       | LOAD CSV FILENAME AS ID
        '''
        if p[2].lower() == 'csv':
            p[0] = ('loadcsv', p[3], p[5])
            
    def p_show_statement(self, p):
        '''
        show_statement : SHOW ID SEMICOLON
                       | SHOW ID
        '''
        if p[2].lower() == 'history': p[0] = ('show', 'history')
        if p[2].lower() == 'environment': p[0] = ('show', 'environment')
        
    def p_insert_statement(self, p):
        # TODO: support extension: insert into X (a,b,c) VALUES (a1,b1,c1), (a2,b2,c2), ...
        '''
        insert_statement : INSERT ID LPAREN id_list RPAREN VALUES LPAREN expr_list RPAREN
                         | INSERT INTO ID LPAREN id_list RPAREN VALUES LPAREN expr_list RPAREN 
        '''
        if p[2].lower() == "into":
            p[0] = ('insert', p[3], p[5], p[9])
        else:
            p[0] = ('insert', p[2], p[4], p[8])

    def p_select_statement(self, p):
        '''
        select_statement : SELECT select_columns FROM ID opt_where_clause opt_orderby_clause
        '''
        p[0] = ('select', p[2], p[4], p[5], p[6])
        
    def p_select_columns(self, p):
        '''
        select_columns : TIMES
                       | id_list
        '''
        p[0] = p[1]
        
    def p_opt_where_clause(self, p):
        '''
        opt_where_clause : WHERE search_condition
                         |
        '''
        if len(p) == 1:
            p[0] = None
        else:
            p[0] = p[2]
            
    def p_search_condition(self, p):
        '''
        search_condition : search_condition OR search_condition
                         | search_condition AND search_condition
                         | NOT search_condition
                         | LPAREN search_condition RPAREN
                         | predicate
        '''
        lenp = len(p)
        if lenp == 4:
            if p[1] == '(':
                p[0] = p[2]
            else:
                p[0] = (p[2], p[1], p[3])
        elif lenp == 3:
            p[0] = (p[1], p[2])
        else:
            p[0] = p[1]
            
    # TODO: there are other predicates...see sql2.y            
    def p_predicate(self, p):
        '''
        predicate : comparison_predicate
        '''
        p[0] = p[1]
        
    def p_comparison_predicate(self, p):
        '''
        comparison_predicate : scalar_exp EQ scalar_exp
                             | scalar_exp NE scalar_exp
                             | scalar_exp LT scalar_exp
                             | scalar_exp LE scalar_exp
                             | scalar_exp GT scalar_exp
                             | scalar_exp GE scalar_exp
        '''
        p[0] = (p[2], p[1], p[3])
        
    # TODO: unify this with old expr rules
    def p_scalar_exp(self, p):
        '''
        scalar_exp : scalar_exp PLUS scalar_exp
                   | scalar_exp MINUS scalar_exp
                   | scalar_exp TIMES scalar_exp
                   | scalar_exp DIVIDE scalar_exp
                   | atom
                   | LPAREN scalar_exp RPAREN
        '''
        lenp = len(p)
        if lenp == 4:
            if p[1] == "(":
                p[0] = p[2]
            else:
                p[0] = (p[2], p[1], p[3])
        elif lenp == 2:
            p[0] = p[1]
        else:
            raise AssertionError()
        
    def p_atom(self, p):
        '''
        atom : NUMBER
             | ID
             | STRING
        '''
        p[0] = p[1]
            
    # TODO: more advanced order by including multiple columns, asc/desc            
    def p_opt_orderby_clause(self, p):
        '''
        opt_orderby_clause : ORDER BY ID
                           |
        '''
        if len(p) == 1:
            p[0] = None
        else:
            p[0] = p[3]
            
    #def p_conditional_expr(self, p):
    #    '''
    #    conditional_expr : relational_expr
    #                     | conditional_expr AND conditional_expr
    #                     | conditional_expr OR conditional_expr
    #    '''
    #    if len(p) == 2:
    #        p[0] = [p[1]]
    #    else:
    #        p[0] = (p[2], p[1], p[3])
            
    #def p_relational_expr(self, p):
    #    '''
    #    relational_expr : expr LT expr
    #                    | expr LE expr
    #                    | expr GT expr
    #                    | expr GE expr
    #                    | expr EQ expr
    #    '''
    #    p[0] = (p[2], p[1], p[3])
        
    def p_id_list(self, p):
        '''
        id_list : ID
                | id_list COMMA ID
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_expr_list(self, p):
        '''
        expr_list : expr
                  | expr_list COMMA expr
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_expr(self, p):
        '''
        expr : expr PLUS term
             | expr MINUS term
             | term
             | ID
             | STRING
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('binop', p[2], p[1], p[3])
            
    def p_term(self, p):
        '''
        term : term TIMES factor
             | term DIVIDE factor
             | factor
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('binop', p[2], p[1], p[3])

    def p_factor(self, p):
        '''
        factor : NUMBER
               | LPAREN expr RPAREN
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2] 
    
    def p_error(self, p):
        print "Syntax error in input" # TODO: at line %d, pos %d!" % (p.lineno)
    
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
    
if __name__ == "__main__":    
    #unittest_lexer()
    unittest_parser()
    
                