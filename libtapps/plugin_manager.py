'''!
Plugin Manager for TAPPS.

Date created: 24th February 2019

Copyright (C) 2019, Maurice HT Ling for TAPPS Development Team.

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

def ImportPlugin(session, pluginName):
    '''!
    Function to import a plugin.

    @param session Dictionary: TAPPS session dictionary.
    @param pluginName String: Name of plugin to import.
    @return: Updated TAPPS session dictionary.
    '''
    pluginPath = [session['cwd'], 'libtapps', 'plugins', 
                  pluginName + '.py']
    pluginPath = os.sep.join(pluginPath)
    try:
        print('Loading plugin from ' + pluginPath)
        pluginDir, pluginFile = os.path.split(pluginPath)
        pluginName, pluginExt = os.path.splitext(pluginFile)
        originalCWD = session['cwd']
        os.chdir(pluginDir)
        pluginObj = __import__(pluginName)
        pluginObj.__file__ = pluginPath
        session['plugins'][pluginName] = pluginObj
        os.chdir(originalCWD)
    except:
        raise ImportError('Unable to import ' + pluginPath)
    return session
