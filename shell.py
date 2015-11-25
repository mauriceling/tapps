'''
TAPPS commandline shell.

Date created: 25th November 2015

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

import os
import sys
import copy
import random
import traceback
from datetime import datetime
from pprint import pprint
    
import engine as e
from tappsparser import TAPPSParser

class Shell(object):
    
    def __init__(self):
        self.parser = TAPPSParser()
        self.parser.build()
        self.history = {}
        self.bytecode = {}
        self.environment = {'cwd': os.getcwd(),
                            'display_ast': True,
                           }
    
    def formatExceptionInfo(self, maxTBlevel=10):
        '''
        Method to gather information about an exception raised. It is used
        to readout the exception messages and type of exception. This method
        takes a parameter, maxTBlevel, which is set to 10, which defines the
        maximum level of tracebacks to recall.
        
        This method is obtained from http://www.linuxjournal.com/
        article.php?sid=5821
        '''
        cla, exc, trbk = sys.exc_info()
        excName = cla.__name__
        try: excArgs = exc.__dict__["args"]
        except KeyError: excArgs = "<no args>"
        excTb = traceback.format_tb(trbk, maxTBlevel)
        return (excName, excArgs, excTb)
        
    def header(self):
        print('''
Technical (Analysis) and Applied Statistics, Version 0.1
Current time is %s

Type "copyright", "credits" or "license" for more information.
To exit this application, type "quit".
''' % (str(datetime.utcnow())))
        
    def do_copyright(self):
        print('')
        print('Copyright (C) 2015, Maurice HT Ling (on behalf of TAPPS Team)')
        print('')
        return None
    
    def do_credits(self):
        print('')
        print('''TAPPS Project Team
Project architect: Maurice HT Ling (mauriceling@acm.org)''')
        print('')
        return None
        
    def do_license(self):
        print('')
        license = open('LICENSE', 'r').readlines()
        license = [x[:-1] for x in license]
        for line in license: print(line)
        print('')
        return None

    def show_environment(self):
        environment = self.environment.keys()
        environment.sort()
        print('')
        print('Environment Variables:')
        for e in environment:
            print('  %s = %s' %(str(e), self.environment[str(e)]))
        print('')
        return None
        
    def show_history(self):
        line_number = self.history.keys()
        line_number.sort()
        print('')
        for i in line_number:
            print('Command #%s : %s' % (str(i), self.history[str(i)]))
        print('')
        return None
        
    def intercept_processor(self, statement):
        if statement == 'copyright': return self.do_copyright()
        if statement == 'credits': return self.do_credits()
        if statement == 'exit': return 'exit'
        if statement == 'license': return self.do_license()
        if statement == 'quit': return 'exit'
        if statement == 'show environment': return self.show_environment()
        if statement == 'show history': return self.show_history()
        
    def do_xxx(self, operand):
        pass
    
    def command_processor(self, operator, operand):
        if operator == 'xxx': self.do_xxx(operand)
        
    def cmdloop(self):
        self.header()
        count = 1
        while True:
            try:
                statement = raw_input('TAPPS: %s> ' % str(count)).strip() 
                self.history[str(count)] = statement
                if statement.lower() in ['copyright', 
                                         'credits', 
                                         'exit', 
                                         'license',
                                         'quit',
                                         'show environment',
                                         'show history']:
                     state = self.intercept_processor(statement)
                     if state == 'exit': return 0
                else:
                    bytecode = self.parser.parse(statement, True)
                    self.bytecode[str(count)] = bytecode
                    operator = bytecode[0]
                    if len(bytecode) == 1: 
                        operand = []
                    else: 
                        operand = bytecode[1:]
                    self.command_processor(operator, operand)
                count = count + 1
            except:
                error_message = list(self.formatExceptionInfo())
                for line in error_message:
                    if (type(line) == list):
                        for l in line: 
                            print(l)
            
       
    
if __name__ == '__main__':    
    shell = Shell()
    shell.cmdloop()
    