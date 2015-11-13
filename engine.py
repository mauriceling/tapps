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

import copads
from copads.dataframe import Series
from copads.dataframe import Dataframe
from copads.dataframe import MultiDataframe


plugin_categories = ['template']

def LoadPlugin(session, plugin):
    '''
    Function to perform basic checks and load a plugin into session 
    dictionary to get it ready for use.
    
    The following checks are done:
        1. Able to import plugin module (check for presence of a valid 
        Python module with __init__.py file)
        2. Able to import plugin manifest (check for presence of manifest 
        file: <plugin module>/manifest.py)
        3. Able to import main function, which is the plugin entry 
        function, from <plugin module>/main.py file
        4. Check for presence of plugin's name in manifest file
        5. Check for presence of plugin's release (version number) in 
        manifest file
        6. Check for valid category in manifest file
        7. Check for presence of plugin's short description in manifest 
        file
        8. Check for presence of plugin's long description in manifest file
        9. Check for presence of plugin's URL in manifest file
        10. Check for presence of plugin author(s)' contact(s) in manifest 
        file
        11. Check for presence of plugin's license in manifest file
    
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
    @param plugin: module name of plugin to load (corresponding to the 
    folder/dictionary which the plugin resides - <current working 
    directory>/plugin/<plugin folder name>)
    @type plugin: string
    @return: session dictionary
    '''
    checks = ['ImportError:Plugin',
              'ImportError:Manifest',
              'ImportError:MainFunction',
              'ManifestError:NoName',
              'ManifestError:NoRelease',
              'ManifestError:InvalidCategory',
              'ManifestError:NoShortDescription',
              'ManifestError:NoLongDescription',
              'ManifestError:NoURL',
              'ManifestError:NoContact',
              'ManifestError:NoLicense']
    try: 
        exec('from plugins import %s' % plugin)
        checks[0] = 'Passed'
    except: pass
    try: 
        exec('from plugins.%s import %s' % (plugin, 'manifest'))
        checks[1] = 'Passed'
    except: pass
    try: 
        exec('from plugins.%s.main import %s' % (plugin, 'main'))
        checks[2] = 'Passed'
    except: pass
    try: 
        plugin_name = manifest.name
        if plugin_name != '':
            checks[3] = 'Passed'
    except: pass
    try:
        release = manifest.release
        checks[4] = 'Passed'
    except: pass
    try:
        category = manifest.category
        if category in plugin_categories:
            checks[5] = 'Passed'
    except: pass
    try:
        sDesc = manifest.shortDescription
        checks[6] = 'Passed'
    except: pass
    try:
        lDesc = manifest.longDescription
        checks[7] = 'Passed'
    except: pass
    try:
        URL = manifest.projectURL
        checks[8] = 'Passed'
    except: pass
    try:
        contact = manifest.contactDetails
        checks[9] = 'Passed'
    except: pass
    try:
        license = manifest.license
        checks[10] = 'Passed'
    except: pass
    pass_rate = float(len([x for x in checks if x == 'Passed'])) / float(len(checks))
    if pass_rate < 1.0:
        session['plugins']['loadFail'][plugin] = checks
    else:
        session['plugins']['loaded'].append(plugin_name)
        session['plugins'][category].append(plugin_name)
        session['plugin_' + plugin_name] = {'main': main,
                                            'release': release,
                                            'sdesc': sDesc,
                                            'ldesc': lDesc,
                                            'URL': URL,
                                            'contact': contact,
                                            'license': license}
    return session


def GetPlugins(session, path):
    '''
    Function to discover available plugins and load each of the plugins 
    (using engine.LoadPlugin function to each plugin) into session 
    dictionary and get the plugins ready for use. Each plugin resides 
    within its own folder in the plugin directory/folder; hence, the 
    plugins discovery process is to list down the directory/folder names 
    within the plugin directory/folder.
    
    As this function calls engine.LoadPlugin function repeatedly to each 
    plugin, the following changes will be made to session dictionary:
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
    @param path: full path to plugin directory/folder. Default = <current 
    working directory>/plugins
    @type path: string
    @return: session dictionary
    '''
    plugin_directories = [x for x in os.walk(path)][0][1]
    for plugin in plugin_directories:
        session = LoadPlugin(session, plugin)
    for category in plugin_categories:
        plugin_list = session['plugins'][category]
        plugin_list = list(set(plugin_list))
        session['plugins'][category] = plugin_list
    return session
    
    
def RunPlugin(session, session):
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
    plugin_name = 'plugin_' + parameters['plugin_name']
    results = session[plugin_name]['main'](parameters)
    parameters['results'] = results
    analysis_name = parameters['analysis_name']
    session['analyses'][analysis_name] = parameters
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
    dataframe = DataFrame(filepath)
    dataframe.addCSV(filepath, series_header, separator, fill_in, newline)
    session['new_dataframe'] = dataframe
    return session
    