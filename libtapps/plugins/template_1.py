'''!
Plugin: summarize

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
# ----------------- End of Preamble -----------------

# ---------------------------------------------------
# Start of Plugin Codes
# ---------------------------------------------------

# Name of the plugin / app (mandatory)
name = 'plugin template'

# Version or release number of the plugin / app (mandatory)
release = 1

# Category which this plugin / app should belong to (mandatory)
# Allowed categories are:
# 1. exporter
# 2. importer
# 3. statistics
# 4. statistics.hypothesis
# 5. statistics.model
# 6. statistics.timeseries
# 7. unclassified
category = 'statistics'

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
    p['dataframe'] = <input dataframe object from session['MDF'].frames>
Instructions specific to this plugin:
    1. p['analytical_method'] takes in either 'by_series' 
    (summarize by series) or 'by_labels' (summarize by labels).
'''

parameters = \
{'plugin_name': 'summarize',
 'analysis_name': None,
 'analytical_method': None,
 'dataframe': None,
 'results': None,
 'narrative': None,
}

def main(parameters):
    '''
    Entry function for the 'summarize' plugin.
    
    @param parameters: set of parameters, including data frame, which are 
    needed for the plugin to execute
    @type parameters: dictionary
    @return: parameters
    @rtype: dictionary
    '''
    # Step 1: Pull out needed items / data from parameters dictionary
    method = parameters['analytical_method']
    dataframe = parameters['dataframe']
    results = parameters['results']
    # END Step 1: Pull out needed items / data from parameters dictionary
    
    # Step 2: Perform plugin operations
    if method == 'by_series' or method == None:
        (statistics, labels) = summarize_series(dataframe)
        results.addData(statistics, labels)
    if method == 'by_labels':
        (data, series) = summarize_labels(dataframe)
        results.data = data
        results.label = data.keys()
        results.series_names = series
    # END Step 2: Perform plugin operations
    
    # Step 3: Load dataframe and results back into parameters dictionary
    parameters['dataframe'] = dataframe
    parameters['results'] = results
    # END Step 3: Load dataframe and results back into parameters dictionary
    return parameters

def summarize_series(dataframe):
    '''
    Function to statistical summaries of each series in the dataframe.
    '''
    labels = dataframe.data.keys()
    series = dataframe.series_names
    statistics = {'summation': [],
                  'arithmetic_mean': [],
                  'standard_deviation': [],
                  'maximum': [],
                  'minimum': [],
                  'median': [],
                  'count': []}
    for index in range(len(series)):
        sdata = [float(dataframe.data[label][index]) for label in labels]
        # 1. summation
        statistics['summation'].append(sum(sdata))
        # 2. arithmetic mean
        arithmetic_mean = float(sum(sdata)) / len(sdata)
        statistics['arithmetic_mean'].append(arithmetic_mean)
        # 3. median
        index = int(len(sdata) / 2)
        statistics['median'].append(sdata[index])
        # 4. maximum
        sdata.sort()
        statistics['maximum'].append(sdata[-1])
        # 5. minimum
        statistics['minimum'].append(sdata[0])
        # 6. count
        statistics['count'].append(len(sdata))
        # 7. standard deviation
        if len(sdata) < 30:
            s = float(sum([(x-arithmetic_mean)**2 
                            for x in sdata])) / (len(sdata) - 1)
        else:
            s = float(sum([(x-arithmetic_mean)**2 
                            for x in sdata])) / len(sdata)
        statistics['standard_deviation'].append((s**0.5))
    return (statistics, series)
 
def summarize_labels(dataframe):
    '''
    Function to statistical summaries of each label in the dataframe.
    '''
    labels = dataframe.data.keys()
    series = ['arithmetic_mean',
              'count',
              'maximum',
              'median',
              'minimum',
              'standard_deviation',
              'summation']
    data = {}
    for label in dataframe.data.keys():
        sdata = [float(x) for x in dataframe.data[label]]
        temp = ['arithmetic_mean',
                'count',
                'maximum',
                'median',
                'minimum',
                'standard_deviation',
                'summation']
        # 1. arithmetic mean
        temp[0] = float(sum(sdata)) / len(sdata)
        # 2. count
        temp[1] = len(sdata)
        # 3. maximum
        sdata.sort()
        temp[2] = sdata[-1]
        # 4. median
        index = int(len(sdata) / 2)
        temp[3] = sdata[index]
        # 5. minimum
        temp[4] = sdata[0]
        # 6. standard deviation
        if (len(sdata) < 30) and (len(sdata) > 1):
            s = float(sum([(x-temp[0])**2 
                           for x in sdata])) / (len(sdata) - 1)
        elif len(sdata) == 1:
            s = 'NA'
        else:
            s = float(sum([(x-temp[0])**2 
                           for x in sdata])) / len(sdata)
        temp[5] = s ** 0.5
        # 7: summation
        temp[6] = sum(sdata)
        data[label] = [x for x in temp]
    return (data, series)
