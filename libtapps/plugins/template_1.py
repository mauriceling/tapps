'''!
Plugin: template

Date created: 4th December 2015

Copyright (C) 2015, Maurice HT Ling for TAPPS Development Team.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

# Preamble: Import modules/packages from TAPPS folder
import sys
sys.path.append('../')

import pandas as pd
# ----------------- End of Preamble -----------------

# ---------------------------------------------------
# Start of Plugin Codes
# ---------------------------------------------------

# Name of the plugin / app (mandatory)
name = 'plugin template'

# Version or release number of the plugin / app (mandatory)
release = 1

# A short description of the plugin / app (not mandatory)
shortDescription = \
'''Short Description'''

# Long description of the plugin / app (not mandatory)
longDescription = \
'''Long Description'''

# URL of this project, if any (not mandatory)
projectURL = 'URL to project'

# Person(s) to contact for any help or information regarding this plugin / app
# (not mandatory)
contactDetails = 'Maurice Ling <mauriceling@acm.org>'

# License for this plugin / app (not mandatory)
# If no license is given, it is deemed to be released into public domain 
# for all uses, both academic and industry. 
license = '''General Public Licence version 3

This program is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

instructions = '''
How to fill in parameters dictionary (p):
Standard instructions:
    p['analysis_name'] = <user given name of analysis in string>
    p['narrative'] = <user given description of analysis, if any>
    p['dataframe'] = <Pandas dataframe for analysis>
Instructions specific to this plugin:
    1. p['method'] = <what analysis to be carried out?>
    2. p['method_parameters'] = <dictionary of parameters required for 
    analytical method>
'''

parameters = \
{'plugin_name': 'summarize',
 'analysis_name': None,
 'narrative': None,
 'dataframe': None,
 'method': None,
 'method_parameters': {},
 'results': None
}

def RunPlugIn(parameters):
    '''
    Entry function for the 'summarize' plugin.
    
    @param parameters: set of parameters, including data frame, which are 
    needed for the plugin to execute
    @type parameters: dictionary
    @return: parameters
    @rtype: dictionary
    '''
    # Step 1: Pull out needed items / data from parameters dictionary
    method = parameters['method']
    method_parameters = parameters['method_parameters']
    dataframe = parameters['dataframe']
    results = parameters['results']
    # END Step 1: Pull out needed items / data from parameters dictionary
    
    # Step 2: Perform plugin operations
    if method == "doSomething":
        results = doSomething(method_parameters)
    # END Step 2: Perform plugin operations
    
    # Step 3: Load dataframe and results back into parameters dictionary
    parameters['dataframe'] = dataframe
    parameters['results'] = results
    # END Step 3: Load dataframe and results back into parameters dictionary
    return parameters

def doSomething(mparam):
    """
    Define the actual analysis that needs to be carried out and 
    return the analytical results as a Pandas dataframe"""
    results = []
    results = pd.Dataframe(results)
    return results
