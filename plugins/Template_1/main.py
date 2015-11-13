'''
Template / Boiler plates for writing a TAPPS plugin.
'''

def main(parameters):
    '''
    Entry function for the plugin.
    
    @param parameters: set of parameters, including data frame, which are 
    needed for the plugin to execute
    @type parameters: dictionary
    @return: session
    @rtype: dictionary
    '''
    # Step 1: Pull out needed items / data from parameters dictionary
    method = parameters['analytical_method']
    dataframe = parameters['dataframe']
    results = parameters['results']
    # END Step 1: Pull out needed items / data from parameters dictionary
    
    # Step 2: Perform plugin operations
    if method == 'label_summation':
        (summation, labels) = label_summation(dataframe)
        results.addData({'summation': summation}, 
                        labels)
    # END Step 2: Perform plugin operations
    
    # Step 3: Load dataframe and results back into parameters dictionary
    parameters['dataframe'] = dataframe
    parameters['results'] = results
    # END Step 3: Load dataframe and results back into parameters dictionary
    return parameters
    
def label_summation(dataframe):
    labels = dataframe.data.keys()
    summation = [sum([float(item) 
                      for item in dataframe.data[label]]) 
                 for label in labels]
    return (summation, labels)
    