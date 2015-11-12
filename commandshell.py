'''
Standalone command line system for TAPPS.

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

import os, sys, copy, random, traceback
from datetime import datetime
    
import tappslex
import tappsparse

class Shell(object):
    
    def __init__(self):
        self.history = {}
        self.phistory = {}
        self.results = {}
        self.userdata = {}
        self.environment = {'command_count': 0,
                            'cwd': os.getcwd(),
                            'database_connector': None,
                            'database_cursor': None,
                            'database_file': None,
                            'last_command_time': None,
                            'readline_module': None,
                            'starting_time': str(datetime.utcnow()),
                           }
    
    
    def do_copyright(self, option, param, count):
        print()
        print('Copyright 2010-2013, Maurice HT Ling (on behalf of all authors)')
        print()
    
    def do_credits(self, option, param, count):
        print()
        print('''DOSE Project Team
Project architect: Maurice HT Ling (mauriceling@acm.org)
Lead developer: Clarence Castillo''')
        print()
    
        
    def do_help(self, option, param, count):
        '''
List of available commands:
connectdb           copyright           credits          flush
help                license             list             py  
pyshell             quit                save             show

Type help <command> for more help (if any)'''
        if option == '' or option == 'help': print(self.do_help.__doc__)
        elif option == 'connectdb': print(self.do_connectdb.__doc__)
        elif option == 'copyright': self.do_copyright(option, param, count)
        elif option == 'credits': self.do_credits(option, param, count)
        elif option == 'flush': self.do_flush.__doc__
        elif option == 'license': self.do_license(option, param, count)
        elif option == 'list': print(self.do_list.__doc__)
        elif option == 'quit': print(self.do_quit.__doc__)
        elif option == 'py': print(self.do_py.__doc__)
        elif option == 'pyshell': print(self.do_pyshell.__doc__)
        elif option == 'save': print(self.do_save.__doc__)
        elif option == 'show': print(self.do_show.__doc__)
        else:
            txt = option + ' is not a valid command; hence, no help is available.'
            self.results[count] = txt
            print(txt)
    
    def do_license(self, option, param, count):
        print()
        print('''
DOSE License: Unless otherwise specified, all files in dose/copads folder 
will be licensed under Python Software Foundation License version 2.
All other files, including DOSE, will be GNU General Public License version 3.''')
        print()
        
    def do_list(self, option, param, count):
        '''
Command: list <options>
    <options> = {generations | popname | simulations}
Description: Display information about simulations logged in the simulation 
    logging database.
Pre-requisite(s): Requires connection to a simulation logging database 
(using connectdb command)

<options> = datafields <start_time> <table>
    List all logged datafields of a simulation (identified by start_time) 
    from one of the 4 tables (parameters, organisms, world, and miscellaneous) 
    in the simulation logging database. If <table> is not given, generations 
    will be listed from organisms table.
<options> = generations <start_time> <table>
    List all logged generations of a simulation (identified by start_time) 
    from one of the 3 tables (organisms, world, and miscellaneous) in the 
    simulation logging database. If <table> is not given, generations will 
    be listed from organisms table.
<options> = simulations
    List all simulations in the simulation logging database, in the format 
    of [<starting time of simulation>, <simulation name>]
<options> = popname
    List all logged population names of a simulation (identified by 
    start_time) in the simulation logging database.
        '''
        cur = self.environment['database_cursor']
        param = [x.strip() for x in param.split(' ')]
        if len(param) == 1: table = 'organisms'
        else: table = param[1]
        if cur == None:
            error_message = 'Error: no database had been connected'
        if option == '':
            self.no_options_error_message(self.do_list, count)
        elif option == 'datafields':
            print('''Searching for data fields logged in simulation
    start time = %s of 
    simulation logging database file = %s
    table = %s''' % (param[0], self.environment['database_file'], table))
            results = dose.db_list_datafields(cur, param[0], table)
            self.results[count] = results
            for r in results: print(r)
        elif option == 'generations':
            print('''Searching for generations logged in simulation
    start time = %s of 
    simulation logging database file = %s
    table = %s''' % (param[0], self.environment['database_file'], table))
            results = dose.db_list_generations(cur, param[0], table)
            self.results[count] = results
            for r in results: print(r)
        elif option == 'popname': 
            print('''Searching for population names logged in simulation
    start time = %s of 
    simulation logging database file = %s''' % (param[0], self.environment['database_file']))
            results = dose.db_list_population_name(cur, param[0])
            self.results[count] = results
            for r in results: print(r)
        elif option == 'simulations': 
            print('''Searching for simulations logged in simulation logging 
database file = %s''' % (self.environment['database_file']))
            results = dose.db_list_simulations(cur)
            self.results[count] = results
            for r in results: print(r)
        else:
            txt = option + ' is not a valid option. Type help list for more information'
            self.results[count] = txt
            print(txt)
            
    def do_py(self, option, param, count):
        '''
Command: py <python statement>
    <python statement> = any fully formed and complete Python statement in 
                         a single line (not for multi-line statement, such 
                         as loop)
Description: Execute an arbitrary single-lined Python statement
Pre-requisite(s): None
        '''
        exec(arg)
        
    def do_pyshell(self, option, param, count):
        '''
Command: pyshell
Description: Launch a full Python interactive interpreter and exposes 
    current DOSE command shell as 'self' object. The 3 main dictionaries in 
    current DOSE command shell are exposed at top level - 
    (1) environment (from self.environment - a dictionary that holds all 
    environmental variables), 
    (2) results (from self.results - a dictionary that results from each 
    command in the current session if any), and 
    (3) userdata (from self.userdata - a dictionary that holds any user 
    defined data). 
    This command provides full functionality to the user, which is similar 
    to using DOSE as a library. Hence, please read DOSE command shell 
    documentation and use with care.
    To exit from the interactive interpreter, use Crtl-D.
Pre-requisite(s): None
        '''
        exec('''import code; \
                import dose; \
                environment = self.environment; \
                userdata = self.userdata;\
                results = self.results;\
                code.interact(local=vars())''')
        
    def do_quit(self, option, param, count):
        '''
Command: quit
Description: Terminate this application
Pre-requisite(s): None'''
        print()
        print('''Are you going off?? -:(
Please contact Maurice Ling (mauriceling@acm.org) if you need any help.
Goodbye! Have a nice day and hope to see you again soon!

%s

Current time is %s''' % (quotation(), str(datetime.utcnow())))
        print()
        
    def do_save(self, option, param, count):
        '''
Command: save <options> <file name>
    <options> = {history | workspace}
    <file name> = File name for output. The file will be in current working
                  directory
Description: To save history or data into a text file
Pre-requisite(s): None

<options> = history
    Writes out history of the current session into <file name>
<options> = workspace
    Writes out the entire workspace (history, data, environment) of the 
    current session into <file name>'''
        if option == '':
            self.no_options_error_message(self.do_save, count)
        if param == '': 
            param = 'saved.' + str(self.environment['starting_time']) + '.txt'
        outfile = open(os.sep.join([str(self.environment['cwd']), param]), 'a')
        if option == 'history':
            outfile.write('Date time stamp of current session: ' + \
                         str(self.environment['starting_time']) + os.linesep)
            keys = [int(x) for x in list(self.history.keys())]
            keys.sort()
            for k in [str(x) for x in keys]:
                txt = ' | '.join(['Command', k, str(self.history[k])])
                outfile.write(txt + os.linesep)
            outfile.write('===================================' + os.linesep)
            outfile.close()
        elif option == 'workspace':
            outfile.write('Date time stamp of current session: ' + \
                         str(self.environment['starting_time']) + os.linesep)
            # writing out environment
            for k in list(self.environment.keys()):
                txt = ['Environment', str(k), str(self.environment[k])]
                txt = ' | '.join(txt)
                outfile.write(txt + os.linesep)
            # prepare to write out commands and data
            historykeys = list(self.history.keys())
            keys = [x for x in list(self.results.keys()) 
                    if x not in historykeys]
            keys = keys + historykeys
            keys = [int(x) for x in keys]
            keys.sort()
            for k in [str(x) for x in keys]:
                # writing out commands
                txt = ' | '.join(['Command', k, str(self.history[k])])
                outfile.write(txt + os.linesep)
                # writing out data (self.results) if any
                try:
                    txt = ' | '.join(['Data', str(k), str(self.results[k])])
                    outfile.write(txt + os.linesep)
                except: pass
            outfile.write('===================================' + os.linesep)
            outfile.close()
        else:
            txt = option + ' is not a valid option. Type help save for more information'
            self.results[count] = txt
            print(txt)
            
                
    def command_handler(self, operator, operands):
        count = str(count)
        if cmd == 'xxx': self.do_xxx(operands)
    
    
    def cmdloop(self):
        statement = ''
        count = 1
        while True:
            try:
                statement = raw_input("TAPPS:%s > " % str(count))
                statement = str(statement.strip())
                self.history[str(count)] = statement
                pstatement = tappsparse.parse(statement)
                self.phistory[str(count)] = pstatement
                operator = pstatement[0]
                if len(pstatment) == 1: operands = []
                else: operands = pstatment[1:]
                self.environment['last_command_time'] = str(datetime.utcnow())
                self.environment['command_count'] = count
                self.command_handler(operator, operands)
                count = count + 1
            except:
                error_message = list(self.formatExceptionInfo())
                self.results[str(count)] = error_message
                for line in error_message:
                    if (type(line) == list):
                        for l in line: print(l)
                    print(line)
                
                
    def completer(self, text, state):
        options = [x for x in self.commands 
                   if x.startswith(text)]
        try: return options[state]
        except IndexError: return None
    
    
    def header(self):
        print('''
Technical (Analysis) and Applied Statistics, Version 0.1
Current time is %s

Type "help", "copyright", "credits" or "license" for more information.
To exit this application, type "quit".
''' % (self.environment['starting_time']))
    
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
