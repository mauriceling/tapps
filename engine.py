'''
Execution Engine for TAPPS.

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

import os
import sys
import copy
import re
import importlib

import copads
from copads.dataframe import Series
from copads.dataframe import Dataframe
from copads.dataframe import MultiDataframe


parameters = \
{'analysis_name': None,
 'plugin_name': None,
 'analytical_method': None,
 'dataframe': None,
 'results': Dataframe(),
}

plugin_categories = ['importer',
                     'exporter',
                     'statistics',
                     'statistics.hypothesis',
                     'statistics.model',
                     'statistics.timeseries',
                     'unclassified']

def SetPaths(session):
    sys.path.append(os.sep.join([session['cwd'], 'plugins']))
    sys.path.append(os.sep.join([session['cwd'], 'copads']))
    return sys.path

def LoadPlugin(session, plugin):
    '''
    Function to perform basic checks and load a plugin into session 
    dictionary to get it ready for use.
    
    The following checks are done:
        1. Presence of callable main function in plugin
        2. Presence of Parameters dictionary
        3. Presence of instructions
        4. Presence of plugin name
        5. Presence of release number
        6. Presence of acceptable category
        7. Presence of short description
        8. Presence of long description
        9. Presence of URL
        10. Presence of contact details
        11. Presence of license
    
    The following changes will be made to session dictionary:
        1. If plugin is successfully loaded, the plugin name will be 
        appended to session['plugins']['loaded']
        2. If plugin is successfully loaded, the plugin name will be 
        appended to session['plugins'][<plugin category>]
        3. If plugin is successfully loaded, details of the plugin 
        will be loaded into session['plugins_<plugin name>'], and 
        session['plugins_<plugin name>']['main'] will contain the 
        function entry point for the plugin
        4. If plugin is NOT successfully loaded (failure in one or 
        more of the above checklist), the checklist for the plugin 
        will be loaded into session['plugins']['loadFail'][<plugin 
        name>]
        
    @param session: dictionary to hold all data within the current session. 
    Please see module documentation for more details.
    @param plugin: module name of plugin to load (corresponding to the 
    folder/dictionary which the plugin resides - <current working 
    directory>/plugin/<plugin folder name>)
    @type plugin: string
    @return: session dictionary
    '''
    checks = ['MainFunctionError',
              'ParametersError',
              'InstructionsError',
              'NameError',
              'ReleaseError',
              'CategoryError',
              'ShortDescriptionError',
              'LongDescriptionError',
              'URLError',
              'ContactError',
              'LicenseError']
    # Check 1: Presence of callable main function in plugin
    try:
        if callable(plugin.main):
            main = plugin.main
            checks[0] = 'Passed'
        else:
            print('MainFunctionError - main not callable')
    except:
        print('MainFunctionError - general exception')
    # Check 2: Presence of Parameters dictionary
    try:
        if type(plugin.parameters) == type({}):
            parameters = plugin.parameters
            checks[1] = 'Passed'
        else:
            print('ParametersError - parameters type is not dictionary')
    except:
        print('ParametersError - general exception')
    # Check 3: Presence of instructions
    try:
        instructions = plugin.instructions
        checks[2] = 'Passed'
    except: print('InstructionsError')
    # Check 4: Presence of plugin name
    try:
        plugin_name = plugin.name
        checks[3] = 'Passed'
    except: print('NameError')
    # Check 5: Presence of release number
    try:
        release = plugin.release
        checks[4] = 'Passed'
    except: print('ReleaseError')
    # Check 6: Presence of acceptable category
    try:
        category = plugin.category
        if category in plugin_categories:
            checks[5] = 'Passed'
        else:
            print('CategoryError - Invalid category')
    except: print('CategoryError - general exception')
    # Check 7: Presence of short description
    try:
        sDesc = plugin.shortDescription
        checks[6] = 'Passed'
    except: print('ShortDescriptionError')
    # Check 8: Presence of long description
    try:
        lDesc = plugin.longDescription
        checks[7] = 'Passed'
    except: print('LongDescriptionError')
    # Check 9: Presence of URL
    try:
        URL = plugin.projectURL
        checks[8] = 'Passed'
    except: print('URLError')
    # Check 10: Presence of contact details
    try:
        contact = plugin.contactDetails
        checks[9] = 'Passed'
    except: print('ContactError')
    # Check 11: Presence of license
    try:
        license = plugin.license
        checks[10] = 'Passed'
    except: print('LicenseError')
    # Tabulate passes
    pass_rate = float(len([x for x in checks if x == 'Passed'])) / float(len(checks))
    if pass_rate < 1.0:
        session['plugins']['loadFail'][plugin] = checks
    else:
        plugin_name = plugin_name.lower()
        parameters['results'] = Dataframe()
        session['plugins']['loaded'].append(plugin_name)
        session['plugins'][category].append(plugin_name)
        session['plugin_' + plugin_name] = {'main': main,
                                            'parameters': parameters,
                                            'instructions': instructions,
                                            'release': release,
                                            'sdesc': sDesc,
                                            'ldesc': lDesc,
                                            'URL': URL,
                                            'contact': contact,
                                            'license': license}
    return session
    
def GetPlugins(session, pluginpath='plugins'):
    '''
    Function to discover available plugins and load each of the 
    plugins (using engine.LoadPlugin function to each plugin) into 
    session dictionary and get the plugins ready for use. Each plugin is a Python script file (with or without its own folder) in the 
    plugin directory/folder; hence, the plugins discovery process is 
    to list down the directory/folder names within the plugin directory
    /folder.
    
    As this function calls engine.LoadPlugin function repeatedly to 
    each plugin, the following changes will be made to session 
    dictionary:
        1. If plugin is successfully loaded, the plugin name will be 
        appended to session['plugins']['loaded']
        2. If plugin is successfully loaded, the plugin name will be 
        appended to session['plugins'][<plugin category>]
        3. If plugin is successfully loaded, details of the plugin 
        will be loaded into session['plugins_<plugin name>'], and 
        session['plugins_<plugin name>']['main'] will contain the 
        function entry point for the plugin
        4. If plugin is NOT successfully loaded (failure in one or 
        more of the above checklist), the checklist for the 
        plugin will be loaded into 
        session['plugins']['loadFail'][<plugin name>]
        
    @param session: dictionary to hold all data within the current 
    session. Please see module documentation for more details.
    @param path: path to plugin directory/folder. Default = plugins
    @type path: string
    @return: session dictionary
    '''
    pluginpath = str(pluginpath)
    pysearchre = re.compile('.py$', re.IGNORECASE)
    pluginfiles = filter(pysearchre.search,
                        os.listdir(os.path.join(os.path.dirname(__file__), pluginpath)))
    form_module = lambda fp: '.' + os.path.splitext(fp)[0]
    pluginlist = [x for x in map(form_module, pluginfiles)]
    pluginlist = [x for x in pluginlist 
                  if not (x.startswith('.__') or 
                      x.startswith('.wikipage_generator') or
                      x.startswith('.template'))]
    # import parent module / namespace
    importlib.import_module('plugins')
    for plugin in pluginlist:
        print('Loading plugin: %s' % str(plugin[1:]))
        imported_plugin = importlib.import_module(plugin, 
            package="plugins")
        session = LoadPlugin(session, imported_plugin)
    for category in plugin_categories:
        plugin_list = session['plugins'][category]
        plugin_list = list(set(plugin_list))
        session['plugins'][category] = plugin_list
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
    plugin_name = 'plugin_' + \
                  session['parameters'][parameter_name]['plugin_name']
    parameters = session[plugin_name]['main'](session['parameters'][parameter_name])
    session['parameters'][parameter_name] = parameters
    return session
    
def LoadCSV(session, filepath, series_header, separator, fill_in, newline):
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
    that header is included in the CSV file. 
    @param separator: item separator within the CSV file.
    @param fill_in: value to fill into missing values during process. 
    This is required as the number of data elements across each label 
    must be the same. Hence, filling in of missing values can occur 
    when (1) the newly added data series consists of new labels which 
    are not found in the current data frame (this will require filling 
    in of missing values in the current data frame), or (2) the current 
    data frame consists of labels that are not found in the newly 
    added data series (this will require filling in of missing values 
    to the newly added data series).
    @param newline: character to denote new line or line feed in the 
    CSV file.
    '''
    dataframe = Dataframe(filepath)
    dataframe.addCSV(filepath, series_header, separator, fill_in, newline)
    session['new_dataframe'] = dataframe
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
    session['new_dataframe'].name = dataframe_name
    session['MDF'].addDataframe(session['new_dataframe'], False)
    session['new_dataframe'] = None
    return session
    
def NewPluginParameters(session, plugin_name=''):
    '''
    Function to duplicate parameters dictionary of a specific plugin.
    
    @param session: dictionary to hold all data within the current session. 
    Please see module documentation for more details.
    @param plugin_name: name of plugin to get new parameters for.
    @type plugin_name: string
    @return: plugin parameters dictionary
    '''
    if plugin_name == '':
        return copy.deepcopy(parameters)
    else:
        plugin_name = 'plugin_' + plugin_name
        return copy.deepcopy(session[plugin_name]['parameters'])
    