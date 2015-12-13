'''
TAPPS interpreter: command-line shell and virtual machine.

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
import pickle
from datetime import datetime
from pprint import pprint
    
import copads
from copads.dataframe import Series
from copads.dataframe import Dataframe

import engine as e
from tappsparser import TAPPSParser

class Shell(object):
    '''
    Command-line shell and TAPPS virtual machine.
    '''
    
    def __init__(self, session={}, language='TAPPS'):
        '''
        Constructor method.
        
        @param session: dictionary to hold all data within the current session. 
        Please see module documentation for more details.
        @param language: language to initialize the current shell and virtual 
        machine. Allowable languages are 'TAPPS' (TAPPS DML language).
        @type language: string
        '''
        if language == 'TAPPS':
            self.parser = TAPPSParser()
        self.parser.build()
        self.session = session
        self.history = {}
        self.bytecode = {}
        self.count = 1
        self.environment = {'cwd': os.getcwd(),
                            'display_ast': False,
                            'fill-in': None,
                            'ocwd': os.getcwd(),
                            'separator': ',',
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
        '''
        Prints header, which is displayed at the start of the shell.
        '''
        print('''
TAPPS: Technical (Analysis) and Applied Statistics, Version 0.1
Current time is %s

Type "copyright", "credits" or "license" for more information.
To exit this application, type "quit".
''' % (str(datetime.utcnow())))
        
    def do_copyright(self):
        '''
        Prints copyright statement.
        '''
        print('')
        print('Copyright (C) 2015, Maurice HT Ling (on behalf of TAPPS Team)')
        print('')
        return None
    
    def do_credits(self):
        '''
        Prints list of credits for TAPPS development.
        '''
        print('')
        print('''TAPPS Project Team
Project architect: Maurice HT Ling (mauriceling@acm.org)''')
        print('')
        return None
        
    def do_license(self):
        '''
        Prints license statement.
        '''
        print('')
        license = open('LICENSE', 'r').readlines()
        license = [x[:-1] for x in license]
        for line in license: print(line)
        print('')
        return None
        
    def intercept_processor(self, statement):
        '''
        Method to intercept non-bytecode statements and channel to the 
        appropriate handlers.
        
        @param statement: command-line statement
        @type statement: string
        '''
        if statement == 'copyright': return self.do_copyright()
        if statement == 'credits': return self.do_credits()
        if statement == 'exit': return 'exit'
        if statement == 'license': return self.do_license()
        if statement == 'quit': return 'exit'
        
    def error_message(self, code, msg):
        '''
        Generic error code/message printer to display error/warning messages.
        
        @param code: error/warning code to display
        @type code: string
        @param msg: error/warning message to display
        @type msg: string
        '''
        print('%s: %s' % (str(code), str(msg)))
        
    def do_set(self, operand):
        '''
        Method to set options in environment or within plugin parameters set.
        
        Operand = [<object to show>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        op = operand[0].lower()
        if op == 'displayast':
            if operand[1].lower() in ['t', 'true']:
                self.environment['display_ast'] = True
            if operand[1].lower() in ['f', 'false']:
                self.environment['display_ast'] = False
        if op == 'cwd':
            self.environment['cwd'] = operand[1]
            self.session['cwd'] = operand[1]
        if op == 'ocwd':
            self.environment['cwd'] = self.environment['ocwd']
            self.session['cwd'] = self.environment['ocwd']
        if op == 'rcwd':
            cwd = os.sep.join([self.environment['cwd'], operand[1]])
            self.environment['cwd'] = cwd
            self.session['cwd'] = cwd
        if op == 'separator':
            self.environment['separator'] = operand[1]
        if op == 'fill-in':
            if (type(operand[1]) == type('str')) and \
                (operand[1].lower() == 'none'): 
                self.environment['fill-in'] = None
            elif (type(operand[1]) == type('str')) and \
                (operand[1].lower() != 'none'):
                self.environment['fill-in'] = str(operand[1])
            elif type(operand[1]) == type(1):
                self.environment['fill-in'] = int(operand[1])
            elif type(operand[1]) == type(1.1):
                self.environment['fill-in'] = float(operand[1])
        if op == 'parameter' and operand[1] != 'dataframe':
            param_name = operand[1]
            paramD_name = operand[2]
            data = operand[3]
            if paramD_name in self.session['parameters']:
                self.session['parameters'][paramD_name][param_name] = data
        if op == 'parameter' and operand[1] == 'dataframe':
            paramD_name = operand[2]
            df_name = operand[3]
            if paramD_name in self.session['parameters']:
                if df_name in self.session['MDF'].frames:
                    data = self.session['MDF'].frames[df_name]
                    self.session['parameters'][paramD_name]['dataframe'] = data
        return None
    
    def show_environment(self):
        '''
        Method to show environmental parameters.
        
        Operand = []
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        environment = self.environment.keys()
        environment.sort()
        print('')
        print('Environment Variables:')
        for e in environment:
            print('  %s = %s' %(str(e), self.environment[str(e)]))
        print('')
        return None
    
    def show_asthistory(self):
        '''
        Method to show abstract syntax tree(s) (the bytecode tree(s)) for all 
        executed commands.
        
        Operand = []
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        line_number = self.bytecode.keys()
        line_number.sort()
        print('')
        for i in line_number:
            print('Command #%s : %s' % (str(i), self.bytecode[str(i)]))
        print('')
        return None
        
    def show_history(self):
        '''
        Method to show all executed commands.
        
        Operand = []
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        line_number = self.history.keys()
        line_number.sort()
        print('')
        for i in line_number:
            print('Command #%s : %s' % (str(i), self.history[str(i)]))
        print('')
        return None
    
    def show_pluginlist(self):
        '''
        Method to show summarized list of plugin(s).
        
        Operand = []
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        names = self.session['plugins']['loaded']
        print('')
        print('Loaded Plugins (n = %s): ' % str(len(names)))
        for n in names: 
            print('  %s ; Release = %s' % 
                (str(n), 
                 self.session['plugin_' + n]['release']))
        print('')
        for c in e.plugin_categories:
            numplugin = len(self.session['plugins'][c])
            print('Plugin Category: %s (n = %s)' % (str(c), str(numplugin)))
            listing = ' ; '.join(self.session['plugins'][c])
            print('    %s' % listing)
            print('')
        return None
        
    def show_plugindata(self, operand):
        '''
        Method to show detailed information about a plugin.
        
        Operand = [<plugin name>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        if len(operand) == 2:
            pname = operand[1]
            parameters = self.session['plugin_' + pname]['parameters']
            instructions = self.session['plugin_' + pname]['instructions']
            release = self.session['plugin_' + pname]['release']
            sdesc= self.session['plugin_' + pname]['sdesc']
            ldesc= self.session['plugin_' + pname]['ldesc']
            url = self.session['plugin_' + pname]['URL']
            contact = self.session['plugin_' + pname]['contact']
            license = self.session['plugin_' + pname]['license']
            print('')
            print('Plugin Name: %s; Release = %s' % (str(pname), str(release)))
            print('  Short Description: %s' % str(sdesc))
            print('  Long Description: %s' % str(ldesc))
            print('  URL: %s' % str(url))
            print('  Contact: %s' % str(contact))
            print('  License: %s' % str(license))
            print('  Instructions: %s' % str(instructions))
            print('  Parameter Dictionary:')
            pprint(parameters)
        else:
            return None
        
    def show_session(self):
        '''
        Method to show all session attributes.
        
        Operand = []
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        print('')
        print('Session Attributes:')
        pprint(self.session)
        print('')
        return None
        
    def show_dataframe(self):
        '''
        Method to show data frame(s).
        
        Operand = []
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        dataframes = self.session['MDF'].frames
        print('')
        print('Current Dataframe(s) (n = %s):' % str(len(dataframes)))
        print('')
        for df_name in dataframes.keys():
            series_names = ','.join(dataframes[df_name].series_names)
            print('  Dataframe Name: %s' % str(df_name))
            print('  Series Names: %s' % str(series_names))
            print('  Number of Series: %s' \
                  % str(len(dataframes[df_name].series_names)))
            print('  Number of Labels (data rows): %s' \
                  % str(len(dataframes[df_name].data)))
            print('')
        print('')
        return None
        
    def show_parameter(self):
        '''
        Method to show all plugin parameter(s) set(s).
        
        Operand = []
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        pname = self.session['parameters'].keys()
        print('')
        print('Current Parameter(s) (n = %s):' % str(len(pname)))
        print('')
        for n in pname:
            param = self.session['parameters'][n]
            print('  Parameter Name: %s' % str(n))
            print('    Analysis Name: %s' % str(param['analysis_name']))
            print('    Plugin Name: %s' % str(param['plugin_name']))
            print('    Analytical Method: %s' % str(param['analytical_method']))
            print('    Input Dataframe: %s' % str(param['dataframe']))
            print('    Narrative: %s' % str(param[ 'narrative']))
            print('')
        print('')
        return None
        
    def do_show(self, operand):
        '''
        Method to show attributes or settings.
        
        Operand = [<object to show>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        op = operand[0].lower()
        if op == 'asthistory': return self.show_asthistory()
        if op == 'history': return self.show_history()
        if op == 'environment': return self.show_environment()
        if op == 'pluginlist': return self.show_pluginlist()
        if op == 'plugindata': return self.show_plugindata(operand)
        if op == 'session': return self.show_session()
        if op == 'dataframe': return self.show_dataframe()
        if op == 'parameter': return self.show_parameter()
        return None
    
    def do_loadcsv(self, operand, version):
        '''
        Method to load CSV file and attach the data frame.
        
        Operand = [<CSV file name>, <data frame name>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        @param version: loading version. Version == 1, CSV with headers. 
        Version == 2, CSV without headers.
        '''
        filename = operand[0]
        filepath = os.sep.join([self.environment['cwd'], filename])
        df_name = operand[1]
        if version == 1:
            self.session = e.LoadCSV(self.session, filepath, True, 
                                     self.environment['separator'], 
                                     self.environment['fill-in'], '\n')
            self.session = e.AttachNewDataFrame(self.session, df_name)
        if version == 2:
            self.session = e.LoadCSV(self.session, filepath, False, 
                                     self.environment['separator'], 
                                     self.environment['fill-in'], '\n')
            self.session = e.AttachNewDataFrame(self.session, df_name)
        return None
    
    def do_pythonshell(self, operand):
        '''
        Method to launch a Python shell.
        
        Operand = []
        
        The following are executed:
        C{import code
        from pprint import pprint
        from tapps import *
        import engine as tapps_engine
        session = self.session
        environment = self.environment
        dataframes = self.session['MDF'].frames
        code.interact(local=vars())}
                
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        exec('''import code; \
                from pprint import pprint; \
                from tapps import *; \
                import engine as tapps_engine; \
                session = self.session; \
                environment = self.environment; \
                dataframes = self.session['MDF'].frames; \
                print(""); \
                print("You had spawned a Python interpreter (sub-shell) in TAPPS"); \
                print("Please use Ctrl-D to exit from this sub-shell"); \
                print(""); \
                code.interact(local=vars())''')
        return None
        
    def do_newdataframe(self, operand):
        '''
        Method to attach a data frame (input data frame or results data frame) 
        from plugin parameter(s) set.
        
        Operand = [<name of attached data frame>, <parameter set name>, 
        <parameter: 'dataframe' or 'results'>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        new_df_name = operand[0]
        paramD_name = operand[1]
        df_in_paramD = operand[2]
        if paramD_name in self.session['parameters']:
            if df_in_paramD in self.session['parameters'][paramD_name]:
                df = copy.deepcopy(self.session['parameters'][paramD_name][df_in_paramD])
                df.name = new_df_name
                self.session['MDF'].addDataframe(df, False)
            else:
                code = 'Error/001'
                message = 'Dataframe name, %s, is not found in Parameters %s' \
                          % (df_in_paramD, paramD_name)
                self.error_message(code, message)
        else:
            code = 'Error/002'
            message = 'Parameters name, %s, is not found' % (paramD_name)
            self.error_message(code, message)
        return None
        
    def do_newparam(self, operand):
        '''
        Method to create a new plugin parameter(s) set.
        
        Operand = [<plugin name>, <name for plugin parameter(s) set>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        plugin_name = operand[0]
        parameter_name = operand[1]
        parameters = e.NewPluginParameters(self.session, plugin_name)
        self.session['parameters'][parameter_name] = parameters
        return None
        
    def do_runplugin(self, operand):
        '''
        Method to execute a plugin using a plugin parameter(s) set.
        
        Operand = [<name of plugin parameter(s) set>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        paramD_name = operand[0]
        if paramD_name in self.session['parameters']:
            e.RunPlugin(self.session, paramD_name)
        else:
            code = 'Error/003'
            message = 'Parameters name, %s, is not found' % (paramD_name)
            self.error_message(code, message)
        return None
    
    def do_greedysearch(operand):
        '''
        Method to select data from a data frame into another data frame, where 
        a data element in any series, identified by the same data label, holds 
        true for the selection criterion.
        
        This method uses dataframe.Dataframe.extractValue() method.
        
        Operand = [<data frame name>, <new data frame name>, <binary 
        comparator>, <search value>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        df_name = operand[0]
        ndf_name = operand[1]
        binop = operand[2]
        value = operand[3]
        if binop not in ['=', '!=', '>', '>=', '<', '<=']: binop = '*'
        if df_name in self.session['MDF'].frames:
            df = self.session['MDF'].frames[df_name]
            ndf = df.extractValue(binop, value, ndf_name)
            self.session['MDF'].addDataframe(ndf, False)
        else:
            ndf = Dataframe(ndf_name)
            self.session['MDF'].addDataframe(ndf, False)
            code = 'Warning/004'
            message = 'Dataframe name, %s, is not found. An empty dataframe is added.' \
                      % (df_name)
            self.error_message(code, message)
        return None
        
    def do_idsearch(self, operand):
        '''
        Method to select data from a data frame into another data frame, where 
        a data element in a specific series, holds true for the selection 
        criterion.
        
        This method uses dataframe.Dataframe.extractSeriesValue() method.
        
        Operand = [<data frame name>, <new data frame name>, <series name>, 
        <binary comparator>, <search value>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        df_name = operand[0]
        ndf_name = operand[1]
        series_name = operand[2]
        binop = operand[3]
        value = operand[4]
        if binop not in ['=', '!=', '>', '>=', '<', '<=']: binop = '*'
        if df_name in self.session['MDF'].frames:
            df = self.session['MDF'].frames[df_name]
            ndf = df.extractSeriesValue(series_name, binop, value, ndf_name)
            self.session['MDF'].addDataframe(ndf, False)
        else:
            ndf = Dataframe(ndf_name)
            self.session['MDF'].addDataframe(ndf, False)
            code = 'Warning/005'
            message = 'Dataframe name, %s, is not found. An empty dataframe is added.' \
                      % (df_name)
            self.error_message(code, message)
        return None
    
    def do_cast(self, operand):
        '''
        Method to type cast one or more series in a data frame.
        
        Operand = [<data type to cast into>, <data frame name>, 
        [<series names>]]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        if operand[0] == 'alpha': datatype = 'string'
        if operand[0] == 'nonalpha': datatype = 'float'
        if operand[0] == 'float': datatype = 'float'
        if operand[0] == 'real': datatype = 'float'
        if operand[0] == 'integer': datatype = 'integer'
        df_name = operand[1]
        series_names = operand[2]
        if df_name not in self.session['MDF'].frames: 
            code = 'Error/006'
            message = 'Dataframe name, %s, is not found' % (df_name)
            self.error_message(code, message)
            return None
        df = self.session['MDF'].frames[df_name]
        if series_names[0] == 'all':
            df.cast(datatype, 'error_replace', 'all')
        else:
            error_sn = [s for s in series_names if s not in df.series_names]
            if len(error_sn) > 0:
                code = 'Warning/013'
                message = 'The following series name(s) are not found and not casted: %s' \
                          % (' ,'.join(error_sn))
                self.error_message(code, message)
            series_names = [s for s in series_names if s in df.series_names]
            for s in series_names:
                df.cast(datatype, 'error_replace', s)
        return None
    
    def do_duplicateframe(self, operand):
        '''
        Method to replicate/duplicate a data frame using deepcopy.
        
        Operand = [<name of data frame to duplicate>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        df_name = operand[0]
        ndf_name = operand[1]
        if df_name in self.session['MDF'].frames:
            df = self.session['MDF'].frames[df_name]
            ndf = df.extractValue('*', '', ndf_name)
            self.session['MDF'].addDataframe(ndf, False)
        else:
            ndf = Dataframe(ndf_name)
            self.session['MDF'].addDataframe(ndf, False)
            code = 'Warning/007'
            message = 'Dataframe name, %s, is not found. An empty dataframe is added.' \
                      % (df_name)
            self.error_message(code, message)
        return None
        
    def do_deldataframe(self, operand):
        '''
        Method to delete/remove a data frame.
        
        Operand = [<name of data frame to delete>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        if operand[0] in self.session['MDF'].frames:
            del self.session['MDF'].frames[operand[0]]
        else:
            code = 'Warning/008'
            message = 'Dataframe name, %s, is not found. No dataframe deleted' \
                      % (operand[0])
            self.error_message(code, message)
        return None
        
    def do_delparam(self, operand):
        '''
        Method to delete/remove a plugin parameter(s) set.
        
        Operand = [<plugin parameter(s) set to delete>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        if operand[0] in self.session['parameters']:
            param = self.session['parameters']
            del param[operand[0]]
        else:
            code = 'Warning/009'
            message = 'Parameter, %s, is not found. No parameters deleted' \
                      % (operand[0])
            self.error_message(code, message)
        return None
    
    def do_describe(self, operand):
        '''
        Method to describe a data frame.
        
        Operand = [<data frame name>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        if operand[0] not in self.session['MDF'].frames: 
            code = 'Error/010'
            message = 'Dataframe name, %s, is not found' % (operand[0])
            self.error_message(code, message)
            return None
        else: 
            df = self.session['MDF'].frames[operand[0]]
        print('')
        print('Describing Dataframe - %s' % df.name)
        print('')
        series_names = ','.join(df.series_names)
        print('  Series Names: %s' % str(series_names))
        print('  Number of Series: %s' % str(len(df.series_names)))
        print('  Number of Labels (data rows): %s' % str(len(df.data)))
        print('')
        for sn in df.series_names:
            index = df.series_names.index(sn)
            sdata = [df.data[label][index] for label in df.data.keys()]
            sdata.sort()
            dtypes = {'string': 0, 'integer': 0, 'float': 0, 'unknown': 0}
            for d in sdata:
                if type(d) == type('str'): 
                    dtypes['string'] = dtypes['string'] + 1
                elif type(d) == type(1): 
                    dtypes['integer'] = dtypes['integer'] + 1
                elif type(d) == type(1.0): 
                    dtypes['float'] = dtypes['float'] + 1
                else:
                    dtypes['unknown'] = dtypes['unknown'] + 1
            print('  Series Name - %s' % str(sn))
            print('  Minimum value in %s: %s' % (str(sn), str(sdata[0])))
            print('  Maximum value in %s: %s' % (str(sn), str(sdata[-1])))
            print('  Number of string data type values: %s' \
                  % str(dtypes['string']))
            print('  Number of integer data type values: %s' \
                  % str(dtypes['integer']))
            print('  Number of float data type values: %s' \
                  % str(dtypes['float']))
            print('  Number of unknown data type values: %s' \
                  % str(dtypes['unknown']))
            print('')
        return None
        
    def do_savesession(self, operand):
        '''
        Method to save/serialize the current session into a file.
        
        Operand = [<file name to be serialized into>]
        
        This method used pickle protocol version 0 to serialize.
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        filename = os.sep.join([self.environment['cwd'], operand[0]])
        f = open(filename, 'wb')
        data = [self.session,
                self.history,
                self.bytecode,
                self.count,
                self.environment]
        pickle.dump(data, f, 0)
        return None
        
    def do_loadsession(self, operand):
        '''
        Method to load a previously saved/serialized session from external 
        file.
        
        Operand = [<session serialized file>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        filename = os.sep.join([self.environment['cwd'], operand[0]])
        f = open(filename, 'rb')
        data = pickle.load(f)
        self.session = data[0]
        self.history = data[1]
        self.bytecode = data[2]
        self.count = data[3]
        self.environment = data[4]
        return None
        
    def do_mergeseries(self, operand):
        '''
        Method to merge one or more series from the source data frame into 
        destination data frame.
        
        Operand = [<data frame name>, [<series names>], <source data frame>, 
        <destination data frame>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        series_names = operand[0]
        source_df = operand[1]
        destination_df = operand[2]
        if source_df not in self.session['MDF'].frames:
            code = 'Error/011'
            message = 'Dataframe name (source), %s, is not found' % (source_df)
            self.error_message(code, message)
            return None
        else:
            sdf = self.session['MDF'].frames[source_df]
        if destination_df not in self.session['MDF'].frames: 
            code = 'Error/012'
            message = 'Dataframe name (destination), %s, is not found' % (destination_df)
            self.error_message(code, message)
            return None
        else:
            ddf = self.session['MDF'].frames[destination_df]
        if series_names[0].lower() == 'all':
            series_names = [s for s in sdf.series_names]
        error_sn = [s for s in series_names if s not in sdf.series_names]
        if len(error_sn) > 0:
            code = 'Error/014'
            message = 'The following series name(s), %s, are not found in %s' \
                      % (' ,'.join(error_sn), source_df)
            self.error_message(code, message)
        series_names = [s for s in series_names if s in sdf.series_names]
        for sn in series_names:
            if sn in ddf.series_names:
                code = 'Warning/015'
                message = 'Series name, %s, is found in destination dataframe and is not merged' \
                          % (' ,'.join(error_sn))
                self.error_message(code, message)
            else:
                s = sdf.toSeries(sn)
                ddf.addSeries(s, None)
        return None
    
    def do_mergelabels1(self, operand):
        '''
        Method to append data from source data frame into destination data 
        frame, without replacement. Existing data within the destination data 
        frame will not be replaced with data from source data frame.
        
        Operand = [<data frame name>, <source data frame>, <destination data 
        frame>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        source_df = operand[0]
        destination_df = operand[1]
        if source_df not in self.session['MDF'].frames:
            code = 'Error/016'
            message = 'Dataframe name (source), %s, is not found' % (source_df)
            self.error_message(code, message)
            return None
        else:
            sdf = self.session['MDF'].frames[source_df]
        if destination_df not in self.session['MDF'].frames: 
            code = 'Error/017'
            message = 'Dataframe name (destination), %s, is not found' % (destination_df)
            self.error_message(code, message)
            return None
        else:
            ddf = self.session['MDF'].frames[destination_df]
        if sdf.series_names != ddf.series_names:
            code = 'Error/020'
            message = 'Destination series name(s), %s, do not match source series name(s), %s' \
                      % (str(ddf.series_names), str(sdf.series_names))
            self.error_message(code, message)
            return None
        ddf_labels = ddf.data.keys()
        keylist = [k for k in sdf.data.keys() if k not in ddf_labels]
        for label in keylist:
            ddf.data[label] = [x for x in sdf.data[label]]
        ddf.label = ddf.data.keys()
        return None
    
    def do_mergelabels2(self, operand):
        '''
        Method to append data from source data frame into destination data 
        frame, with replacement. Existing data within the destination data 
        frame will be replaced with data from source data frame, if the labels 
        in the destination data frame is found in the source data frame.
        
        Operand = [<data frame name>, <source data frame>, <destination data 
        frame>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        source_df = operand[0]
        destination_df = operand[1]
        if source_df not in self.session['MDF'].frames:
            code = 'Error/018'
            message = 'Dataframe name (source), %s, is not found' % (source_df)
            self.error_message(code, message)
            return None
        else:
            sdf = self.session['MDF'].frames[source_df]
        if destination_df not in self.session['MDF'].frames: 
            code = 'Error/019'
            message = 'Dataframe name (destination), %s, is not found' % (destination_df)
            self.error_message(code, message)
            return None
        else:
            ddf = self.session['MDF'].frames[destination_df]
        if sdf.series_names != ddf.series_names:
            code = 'Error/021'
            message = 'Destination series name(s), %s, do not match source series name(s), %s' \
                      % (str(ddf.series_names), str(sdf.series_names))
            self.error_message(code, message)
            return None
        for label in sdf.data.keys():
            ddf.data[label] = [x for x in sdf.data[label]]
        ddf.label = ddf.data.keys()
        return None
        
    def do_renameseries(self, operand):
        '''
        Method to rename series name within a specific data frame.
        
        Operand = [<data frame name>, <original series name>, <new series name>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        old_name = operand[1]
        new_name = operand[2]
        if operand[0] not in self.session['MDF'].frames:
            code = 'Error/022'
            message = 'Dataframe name, %s, is not found' % (operand[0])
            self.error_message(code, message)
            return None
        else:
            df = self.session['MDF'].frames[operand[0]]
        try:
            index = df.series_names.index(old_name)
            df.series_names[index] = new_name
        except ValueError:
            code = 'Error/024'
            message = 'Series name, %s, is not found' % (old_name)
            self.error_message(code, message)
        return None
        
    def do_renamelabels(self, operand):
        '''
        Method to rename label name within a specific data frame.
        
        Operand = [<data frame name>, <original label name>, <new label name>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        old_name = operand[1]
        new_name = operand[2]
        if operand[0] not in self.session['MDF'].frames:
            code = 'Error/023'
            message = 'Dataframe name, %s, is not found' % (operand[0])
            self.error_message(code, message)
            return None
        else:
            df = self.session['MDF'].frames[operand[0]]
        if old_name not in df.data.keys():
            code = 'Error/025'
            message = 'Label name, %s, is not found' % (old_name)
            self.error_message(code, message)
            return None
        index = df.label.index(old_name)
        df.label[index] = new_name
        data = [x for x in df.data[old_name]]
        df.data[new_name] = data
        del df.data[old_name]
        return None
    
    def do_savecsv(self, operand):
        '''
        Method to save a data frame into a CSV file.
        
        Operand = [<data frame name>, <CSV file name>]
        
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        if operand[0] not in self.session['MDF'].frames:
            code = 'Error/026'
            message = 'Dataframe name, %s, is not found' % (operand[0])
            self.error_message(code, message)
            return None
        else:
            df = self.session['MDF'].frames[operand[0]]
        filename = operand[1]
        filepath = os.sep.join([self.environment['cwd'], filename])
        csvfile = open(filepath, 'w')
        sep = self.environment['separator']
        header = sep.join([''] + [str(x) for x in df.series_names])
        csvfile.write(header + '\n')
        for label in df.data.keys():
            row = [str(label)] + [str(item) for item in df.data[label]]
            row = sep.join(row)
            csvfile.write(row + '\n')
        csvfile.close()
        return None
        
    def command_processor(self, operator, operand):
        '''
        Method to channel bytecodes operand(s), if any, into the respective 
        bytecode processors.
        
        @param operator: bytecode operator
        @type operator: string
        @param operand: bytecode operand(s), if any
        @type operand: list
        '''
        if operator == 'cast': self.do_cast(operand)
        if operator == 'deldataframe': self.do_deldataframe(operand)
        if operator == 'delparam': self.do_delparam(operand)
        if operator == 'describe': self.do_describe(operand)
        if operator == 'duplicateframe': self.do_duplicateframe(operand)
        if operator == 'greedysearch': self.do_greedysearch(operand)
        if operator == 'idsearch': self.do_idsearch(operand)
        if operator == 'loadcsv1': self.do_loadcsv(operand, 1)
        if operator == 'loadcsv2': self.do_loadcsv(operand, 2)
        if operator == 'loadsession': self.do_loadsession(operand)
        if operator == 'mergelabels1': self.do_mergelabels1(operand)
        if operator == 'mergelabels2': self.do_mergelabels2(operand)
        if operator == 'mergeseries': self.do_mergeseries(operand)
        if operator == 'newdataframe': self.do_newdataframe(operand)
        if operator == 'newparam': self.do_newparam(operand)
        if operator == 'pythonshell': self.do_pythonshell(operand)
        if operator == 'renameseries': self.do_renameseries(operand)
        if operator == 'renamelabels': self.do_renamelabels(operand)
        if operator == 'runplugin': self.do_runplugin(operand)
        if operator == 'savecsv': self.do_savecsv(operand)
        if operator == 'savesession': self.do_savesession(operand)
        if operator == 'set': self.do_set(operand)
        if operator == 'show': self.do_show(operand)
    
    def interpret(self, statement):
        '''
        Method to process an input statement by either sending it to Shell.
        intercept_processor(), for non-bytecodes statements, or Shell.
        command_processor(), for bytecodes statements after lexing and parsing 
        the input statement into bytecodes.
        
        Bytecodes are returned by the corresponding language's lexer and parser 
        in the form of a tuple, (<bytecode operator>, <bytecode operands>+), 
        which is then split into operator (the byte operator) and a list of 
        operands (the bytecode operands), if any.
        
        @param statement: command-line statement
        @type statement: string
        '''
        try:
            self.history[str(self.count)] = statement
            if statement.lower() in ['copyright', 'copyright;',
                                     'credits', 'credits;',
                                     'exit', 'exit;',
                                     'license', 'license;',
                                     'quit', 'quit;',
                                    ]:
                 state = self.intercept_processor(statement)
                 if state == 'exit': return 'exit'
            else:
                bytecode = self.parser.parse(statement, 
                                             self.environment['display_ast'])
                self.bytecode[str(self.count)] = bytecode
                operator = bytecode[0]
                if len(bytecode) == 1: 
                    operand = []
                else: 
                    operand = bytecode[1:]
                self.command_processor(operator, operand)
            self.count = self.count + 1
        except:
            error_message = list(self.formatExceptionInfo())
            for line in error_message:
                if (type(line) == list):
                    for l in line: 
                        print(l)
        
    def cmdloop(self):
        '''
        Command-line loop executor. This runs the shell like a command-line 
        interpreter and calls Shell.interpret() method to process the statement/
        command from the command-line.
        
        @return: session dictionary
        '''
        self.header()
        while True:
            statement = raw_input('TAPPS: %s> ' % str(self.count)).strip() 
            if statement == 'exit': return 0
            self.interpret(statement)
        return self.session
        
    def cmdscript(self, script):
        '''
        Script executor. This method is used to execute a script file that is 
        passed into TAPPS and calls Shell.interpret() method to process the 
        ordered list of commands in script.
        
        @param script: ordered list of commands in script to execute.
        @return: session dictionary
        '''
        for statement in script:
            statement = statement.strip()
            print('Command #%s: %s' % (str(self.count), statement))
            if statement == 'exit': return 0
            self.interpret(statement)
        return self.session
            
       
if __name__ == '__main__':
    from tapps import session
    shell = Shell(session)
    shell.cmdloop()
