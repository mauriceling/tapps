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

# attempt to import readline or pyreadline
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
        
import copads
from copads.dataframe import Series
from copads.dataframe import Dataframe

import commandshell
import startup

global session

session = startup.session
session = startup.startup(session)

def RunPlugin(plugin_name, parameters, session=session):
    plugin_name = 'plugin_' + plugin_name
    results = session[plugin_name]['main'](parameters)
    return results
    
    
def RunShell():
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
    
    
if __name__ == '__main__':
    RunShell()
    sys.exit()