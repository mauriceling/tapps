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

def loadPlugin(plugin, session):
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
    
    @param plugin: module name of plugin to load (corresponding to the 
    folder/dictionary which the plugin resides - <current working 
    directory>/plugin/<plugin folder name>)
    @type plugin: string
    @param session: dictionary to hold all data within the current session. 
    Please see module documentation for more details.
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
        session['plugins']['loaded'] = plugin_name
        session['plugins'][category].append(plugin_name)
        session['plugin_' + plugin_name] = {'main': main,
                                            'release': release,
                                            'sdesc': sDesc,
                                            'ldesc': lDesc,
                                            'URL': URL,
                                            'contact': contact,
                                            'license': license}
    return session


def getPlugins(path, session):
    '''
    Function to discover available plugins and load each of the plugins 
    into session dictionary and get the plugins ready for use. Each plugin 
    resides within its own folder in the plugin directory/folder; hence, 
    the plugins discovery process is to list down the directory/folder 
    names within the plugin directory/folder.
    
    @param path: full path to plugin directory/folder. Default = <current 
    working directory>/plugins
    @type path: string
    @param session: dictionary to hold all data within the current session. 
    Please see module documentation for more details.
    @return: session dictionary
    '''
    plugin_directories = [x for x in os.walk(path)][0][1]
    for plugin in plugin_directories:
        session = loadPlugin(plugin, session)
    for category in plugin_categories:
        plugin_list = session['plugins'][category]
        plugin_list = list(set(plugin_list))
        session['plugins'][category] = plugin_list
    return session
    
    
def RunPlugin(parameters, session):
    plugin_name = 'plugin_' + parameters['plugin_name']
    results = session[plugin_name]['main'](parameters)
    parameters['results'] = results
    analysis_name = parameters['analysis_name']
    session['analyses'][analysis_name] = parameters
    return session
    
 
def LoadCSV(filepath, series_header, separator, fill_in, newline):
    dataframe = DataFrame(filepath)
    dataframe.addCSV(filepath, series_header, separator, fill_in, newline)
    session['new_dataframe'] = dataframe
    return session
    