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

import shell as s
import engine as e

global session
global MDF

import plugins

MDF = MultiDataframe('TAPPS_' + str(datetime.utcnow()))

session = \
{'cwd': os.getcwd(),
 'plugins': {'loadFail': {},
             'loaded': [],
             'exporter': [],
             'importer': [],
             'statistics': [],
             'statistics.hypothesis': [],
             'statistics.model': [],
             'statistics.timeseries': [],
             'unclassified': [],
            },
 'parameters': {
               },
 'MDF': MDF,
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
    sys.path = e.SetPaths(session)
    session = e.GetPlugins(session, os.sep.join([session['cwd'], 'plugins']))
    return session
    
def LoadPlugin(session, plugin_name):
    '''
    Function to perform basic checks and load a plugin into session 
    dictionary to get it ready for use.
    
    The following checks are done:
        1. Able to import plugin module (check for presence of a valid 
        Python module with __init__.py file)
        2. Able to import plugin manifest (check for presence of manifest 
        file: <plugin module>/manifest.py)
        3. Able to import parameters dictionary from 
        <plugin module>/main.py file
        4. Able to import main function, which is the plugin entry 
        function, from <plugin module>/main.py file
        5. Able to import instructions from <plugin module>/main.py file
        6. Check for presence of plugin's name in manifest file
        7. Check for presence of plugin's release (version number) in 
        manifest file
        8. Check for valid category in manifest file
        9. Check for presence of plugin's short description in manifest 
        file
        10. Check for presence of plugin's long description in manifest file
        11. Check for presence of plugin's URL in manifest file
        12. Check for presence of plugin author(s)' contact(s) in manifest 
        file
        13. Check for presence of plugin's license in manifest file
    
    The following changes will be made to session dictionary:
        1. If plugin is successfully loaded, the plugin name will be 
        appended to session['plugins']['loaded']
        2. If plugin is successfully loaded, the plugin name will be 
        appended to session['plugins'][<plugin category>]
        3. If plugin is successfully loaded, details of the plugin will 
        be loaded into session['plugins_<plugin name>'], and 
        session['plugins_<plugin name>']['main'] will contain the function 
        entry point for the plugin
        4. If plugin is NOT successfully loaded (failure in one or more of 
        the above checklist), the checklist for the plugin will be loaded 
        into session['plugins']['loadFail'][<plugin name>]
        
    @param session: dictionary to hold all data within the current session. 
    Please see module documentation for more details.
    @param plugin_name: module name of plugin to load (corresponding to the 
    folder/dictionary which the plugin resides - <current working 
    directory>/plugin/<plugin folder name>)
    @type plugin_name: string
    @return: session dictionary
    '''
    session = e.LoadPlugin(session, plugin_name)
    return session
    
def RunPlugin(session, parameter_name):
    '''
    Function to run/execute a plugin using the parameters (sub-dictionary 
    within session, under 'parameters' key) needed for the plugin and 
    returning the execution results into session dictionary.
    
    The parameters sub-dictionary will need to contain values for the 
    following keys:
        - analysis_name: user-given name for the analytical execution of 
        plugin
        - plugin_name: name of plugin to execute
        - dataframe: a dataframe object to act as data for use by the 
        plugin
    and any other plugin-specific parameters/options.
    
    After execution, analysis results will be returned as value to 
    'results' key in the parameters sub-dictionary.
    
    Hence, session['parameters'][<parameter_name>] will hold the entire 
    parameters sub-dictionary for the current plugin execution and 
    session['parameters'][<parameter_name>]['results'] will hold the 
    plugin output results.
    
    @param session: dictionary to hold all data within the current session. 
    Please see module documentation for more details.
    @param parameter_name: name of parameter dictionary to hold all the 
    parameters needed to execute the plugin. Please see module 
    documentation for more details.
    @return: session dictionary
    '''
    session = e.RunPlugin(session, parameter_name)
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
    
def AttachNewDataFrame(session, dataframe_name):
    '''
    Function to move a new dataframe (in session['new_dataframe'], such 
    as from LoadCSV function) to the main multi data frame object (in 
    session['MDF']. 
    
    MDF will have a new dataframe while session['new_dataframe'] will be 
    set to None.
    
    @param session: dictionary to hold all data within the current session. 
    Please see module documentation for more details.
    @param dataframe_name: new name for the dataframe to attach
    '''
    session = e.AttachNewDataFrame(session, dataframe_name)
    return session
    
def NewPluginParameters(session, plugin_name=''):
    return e.NewPluginParameters(session, plugin_name)
    
def RunShell(session):
    shell = s.Shell(session)
    shell.cmdloop()
    
def RunScript(session, scriptfile):
    shell = s.Shell(session)
    script = open(scriptfile, 'r').readlines()
    script = [x[:-1] for x in script]
    script = [x.strip() for x in script]
    script = [x for x in script 
                  if (x != '') or x.startswith('#')]
    shell.cmdscript(script)
    
def RunNonShell(session, argv):
    if argv[1].lower() == 'script':
        RunScript(session, argv[2])
    
session = startup(session)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        RunShell(session)
        sys.exit()
    if len(sys.argv) == 3:
        RunNonShell(session, sys.argv)
        sys.exit()
    if (len(sys.argv) == 3) or \
        (sys.argv[1] == 'help') or \
        (sys.argv[1] == 'usage'):
        print('')
        print('TAPPS: Technical (Analysis) and Applied Statistics')
        print('')
        print('Copyright (C) 2015, Maurice HT Ling (on behalf of TAPPS Team)')
        print('https://github.com/mauriceling/tapps')
        print('')
        print('Usage: python tapps.py [option] [parameter]')
        print('')
        print('If no option is given (i.e. python tapps.py), TAPPS command')
        print('line shell will be launched for interactive usage.')
        print('')
        print("If option = 'script' (i.e. python tapps.py script <script file>),") 
        print('a script file name must be given. The script file written in')
        print('TAPPS scripting language will be executed.')
