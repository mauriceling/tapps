import os
import sys
from pprint import pprint

from tapps import *

session = LoadCSV(session, 
                  os.sep.join([session['cwd'], 'data', 
                               'STI_20151111_19871228.csv']))
session = AttachNewDataFrame(session, 'STI')

parameters = NewPluginParameters(session, 'template')

parameters['analysis_name'] = 'test'
parameters['plugin_name'] = 'template'
parameters['dataframe'] = session['MDF'].frames['STI']
parameters['analytical_method'] = 'summation'

session['parameters']['testingA'] = parameters

RunPlugin(session, 'testingA')

pprint(session)

pprint(parameters)

'''
SET CWD /Users/mauriceling/Dropbox/MyProjects/tapps/data
SET SEPARATOR ,
SET FILLIN None

LOAD CSV STI_20151111_19871228.csv as STI

NEW template PARAMETERS AS testingA
'''