'''
TAPPS: Technical (Analysis) and Applied Statistics.

Date created: 11th November 2015

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
from datetime import datetime

import copads
from copads.dataframe import Series
from copads.dataframe import Dataframe
from copads.dataframe import MultiDataframe

import commandshell
import engine as e

global session
global MDF


MDF = MultiDataframe('TAPPS_' + str(datetime.utcnow()))

import plugins

session = \
{'paths': {'cwd': os.getcwd(),
           'data': os.sep.join([os.getcwd(), 'data']),
           'plugins': os.sep.join([os.getcwd(), 'plugins']),
          },
 'plugins': {'loadFail': {},
             'loaded': [],
             'template': [],
            },
 'analyses': {
             },
}

parameters = \
{'analysis_name': None,
 'plugin_name': None,
 'dataframe': None,
 'results': None,
}

def startup(session):
    '''
    Main function to execute all startup routines, which includes the 
    following:
        1. Get a list of available plugins and load each of them.
    
    @param session: dictionary to hold all data within the current session. 
    Please see module documentation for more details.
    @return: session dictionary
    '''
    session = e.GetPlugins(session, session['paths']['plugins'])
    return session
    
    
def RunPlugin(session, parameters):
    '''
    Function to run/execute a plugin using the parameters needed for the 
    plugin and returning the execution results into session dictionary.
    
    The parameters dictionary will need to contain values for the following 
    keys:
        - analysis_name: user-given name for the analytical execution of 
        plugin
        - plugin_name: name of plugin to execute
        - dataframe: a dataframe object to act as data for use by the 
        plugin
    and any other plugin-specific parameters/options.
    
    After execution, analysis results will be returned as value to 
    'results' key in the parameters dictionary, and the entire parameters 
    dictionary will be loaded into 'analysis' sub-dictionary within the 
    session dictionary using the analysis_name as key.
    
    Hence, session['analyses'][<analysis_name>] will hold the parameters 
    dictionary.
    
    @param session: dictionary to hold all data within the current session. 
    Please see module documentation for more details.
    @param parameters: dictionary to hold all the parameters needed to 
    execute the plugin. Please see module documentation for more details.
    @return: session dictionary
    '''
    session = e.RunPlugin(session, parameters)
    return session
    
    
def LoadCSV(session, filepath, series_header=True, separator=',', 
            fill_in=None, newline='\n'):
    '''
    Function to load a comma-delimited (CSV) file as a data frame.
    
    The data frame will have the filepath as name, and will be loaded into 
    session dictionary under 'new_dataframe' key.
    
    @param session: dictionary to hold all data within the current session. 
    Please see module documentation for more details.
    @param filepath: path to CSV file.
    @type filepath: string
    @param series_header: boolean flag to denote whether the first row 
    in the CSV file contains the data header. It is highly recommended 
    that header is included in the CSV file. Default = True (header is 
    included)
    @param separator: item separator within the CSV file. Default = ','
    @param fill_in: value to fill into missing values during process. 
    This is required as the number of data elements across each label 
    must be the same. Hence, filling in of missing values can occur 
    when (1) the newly added data series consists of new labels which 
    are not found in the current data frame (this will require filling 
    in of missing values in the current data frame), or (2) the current 
    data frame consists of labels that are not found in the newly 
    added data series (this will require filling in of missing values 
    to the newly added data series). Default = None.
    @param newline: character to denote new line or line feed in the 
    CSV file. Default = '\n'
    '''
    session = e.LoadCSV(session, filepath, series_header, separator, 
                        fill_in, newline)
    return session
    
    
def RunShell(session, MDF):
    try:
        import readline
        readline_import = True
        pyreadline_import = False
    except ImportError:
        readline_import = False
        try:
            import pyreadline as readline
            pyreadline_import = True
        except ImportError:
            readline_import = False
            pyreadline_import = False
    shell = commandshell.Shell()
    shell.header()
    if readline_import:
        shell.environment['readline_module'] = 'readline'
    elif pyreadline_import:
        shell.environment['readline_module'] = 'pyreadline'
    else:
        shell.environment['readline_module'] = None
    if readline_import or pyreadline_import:
        readline.set_completer(shell.completer)   # enables autocompletion
        readline.parse_and_bind("tab: complete")
    shell.cmdloop()
    
    
session = startup(session)


if __name__ == '__main__':
    RunShell(session, MDF)
    sys.exit()
