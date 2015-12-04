'''
Plugin: template 

Template / Boiler plates for writing a TAPPS plugin.

Note that the plugin name have to be entirely in small caps.
'''

instructions = '''
Provides user readable instructions on what the operations of the current 
plugin, how to fill-in the parameters dictionary, and what options are 
required/allowed by the plugin.

How to fill in parameters dictionary (p):
Standard instructions:
    p['analysis_name'] = <user given name of analysis in string>
    p['narrative'] = <user given description of analysis, if any>
    p['dataframe'] = <input dataframe object from session['MDF'].frames>
Instructions specific to this plugin:
    etc etc
'''

parameters = \
{'plugin_name': 'template',
 'analysis_name': None,
 'analytical_method': None,
 'dataframe': None,
 'results': None,
 'narrative': None,
}

def main(parameters):
    '''
    Entry function for the plugin. This sample plugin will sum up the 
    values in each data series within the data frame.
    
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
    if method == 'summation':
        (summation, labels) = series_summation(dataframe)
        results.addData({'summation': summation}, 
                        labels)
    # END Step 2: Perform plugin operations
    
    # Step 3: Load dataframe and results back into parameters dictionary
    parameters['dataframe'] = dataframe
    parameters['results'] = results
    # END Step 3: Load dataframe and results back into parameters dictionary
    return parameters
    
def series_summation(dataframe):
    '''
    Function to perform summation of each series in the dataframe.
    '''
    labels = dataframe.data.keys()
    series = dataframe.series_names
    summation = []
    for index in range(len(series)):
        sdata = [float(dataframe.data[label][index]) for label in labels]
        summation.append(sum(sdata))
    return (summation, series)
    