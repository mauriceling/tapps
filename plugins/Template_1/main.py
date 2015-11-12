import operator
import copy

def main(dataframe, parameters):
    '''
    Function to perform stepwise Vmax optimization, so that the simulated 
    profile approaches the user-defined required test profile. This function 
    is based on ads.SensitivityAnalysis function in the sense that the most 
    sensitive Vmax will be optimized (vary the Vmax so that the simulated 
    profile approaches the user-defined required test profile) first if there 
    is more than one Vmaxes, lock down the value (Vmax), before optimizing 
    the next most sensitive Vmax.
    
    @param modelname: name of the genetic circuit. This function will 
    look for a corresponding ./temp/<modelname>_parameters.py file, which 
    is the parameter file for the genetic circuit. 
    @type modelname: string
    @param parts: parts definition (see example in g2m module documentation). 
    Default = None.
    @type parts: dictionary
    @param parts_parameters: parts parameters (see example in g2m module
    documentation). Default = None.
    @type parts_parameters: dictionary
    @param variable_names: list of variable/field/attribute names 
    of simresult.
    @param required_test_profile: user-supplied (required) profile of test_probe 
    after optimization process. The optimizer will attempt to reduce the 
    differences between the simulated results and the required_test_profile. 
    This parameter is given as a list of list, that is [[<time>, <required 
    expression value of test-probe]].
    @type required_test_profile: list
    @param test_probe: variable name of the simulation result (must be found 
    in variable_names) for use as test probe. 
    @type test_probe: string
    @param sampling: sampling ratio of simulation results. This is to prevent 
    the results file being too large, especially in sensitivity analysis - 
    3600 seconds at 0.1 second per timestep results in 36000 solutions. 
    Default = 0.01, means 1% or every 100th solution will be taken.
    @type sampling: float
    @param simulator: name of the target simulator or ODE solver to 
    generate simulation code. Default = RK4 (Runge Kutta 4 ODE solver).
    @type simulator: string
    @param start_time: start of time for the simulation. Default = 0.0, 
    or starting from time zero.
    @type start_time: float
    @param timestep: time interval for simulation, which is usually a 
    fraction. Default = 0.1.
    @type timestep: float
    @param end_time: ending time for the simulation. Default = 3600.
    @type end_time: float
    @param with_chassis_ode: flag to signify whether the simulation is to 
    be generated with the use of a cell chassis ODEs, where True represents 
    the use of a cell chassis and False represents not using a cell 
    chassis.
    @type with_chassis_ode: boolean
    @param cell_chassis_ode: name of the cell chassis (the host) to 
    be used. Default = eco_chassis (E. coli)
    @type cell_chassis_ode: string
    @param with_print: flag to signify whether to print out the simulation 
    code in console where True represents to print and False represents 
    not to print.
    @type with_print: boolean
    @return: tuple of (partsparam, variable_names, simresult) where 
        1. partsparam is the parameters dictionary for model generation,
        2. variable_names is a list of variable/field/attribute names for 
        the simulation results,
        3. simresult is a list of list of simulation results and each element 
        (a list) represents the result from a timestep.
    '''    
    modelname = parameters['modelname']
    if 'parts' in parameters: 
        parts = parameters['parts']
    else: 
        parts = None
    if 'partsparam' in parameters: 
        parts_parameters = parameters['partsparam']
    else: 
        parts_parameters = None
    variable_names = parameters['variable_names'] 
    required_test_profile = parameters['required_test_profile']
    test_probe = parameters['test_probe']
    if 'sampling' in parameters:
        sampling = parameters['sampling']
    else:
        sampling = 0.01
    if 'simulator' in parameters:
        simulator = parameters['simulator']
    else:
        simulator = 'RK4'
    if 'start_time' in parameters:
        start_time = parameters['start_time']
    else:
        start_time = 0.0
    if 'timestep' in parameters:
        timestep = parameters['timestep']
    else:
        timestep = 0.1
    if 'end_time' in parameters:
        end_time = parameters['end_time']
    else:
        end_time = 3600
    if 'with_chassis_ode' in parameters:
        with_chassis_ode = parameters['with_chassis_ode']
    else:
        with_chassis_ode = False
    if 'cell_chassis_module' in parameters:
        cell_chassis_ode = parameters['cell_chassis_module']
    else: 
        cell_chassis_module = 'eco_chassis'
    if 'with_print' in parameters:
        with_print = parameters['with_print']
    else:
        with_print = False
    
    p = copy.deepcopy(parameters)
    p['sensitivityFile'] = 'temp/temp.csv'
    p['sensitivity_parameters'] = ['all.initial_condition',
                        'all.association_constant',
                        'all.dissociation_constant',
                        'all.peptide_degradation_rate',
                        'all.relative_rbs_strength',
                        'all.hill',
                        'all.km',
                        'all.v0',
                        'all.vmax']
    p['variations'] = [0.6, 1.4]
    
    maxDifference = 10000  #the maximum value could be modified

	#below code use to generate the first time simulation result
    parameters = ads.GenerateAndSimulate(parameters)
                                          
    projected_variables = ['time', test_probe] # the projected_variables is used to select the first row of the data
    # rresult = ads.SimulationResultPicker(variable_names,
                                         # variable_names, simresult) 
    sensitivity_results = ads.SensitivityAnalysis(p)
    (sensitive_parameters, 
     probe_data) = ads.GetSensitiveParameters(sensitivity_results, 
                                              variable_names, 
                                              test_probe)
                                              
   
    
    return  (sensitive_parameters, probe_data, sensitivity_results)