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
    session = e.getPlugins(session['paths']['plugins'], session)
    return session
    
    
def RunPlugin(parameters, session):
    session = e.RunPlugin(parameters, session)
    return session
    
    
def LoadCSV(filepath, series_header=True, separator=',', 
            fill_in=None, newline='\n'):
    session = e.LoadCSV(filepath, series_header, separator, 
                        fill_in, newline)
    return session
    
    
def RunShell(MDF, session):
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
    RunShell(MDF, session)
    sys.exit()
