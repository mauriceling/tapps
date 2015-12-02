#################################################################
# Example 02: Loading data and running a simple analysis via plugin
#################################################################

@include example_01.py

load csv STI_2015.csv as STI

new template parameter as testingA
set parameter analysis_name in testingA as test
set parameter analytical_method in testingA as summation
set parameter dataframe in testingA as STI

runplugin testingA

new STI_summation dataframe from testingA results

# The Python equivalent of the above will be:
# import os
# import sys
# from pprint import pprint
# 
# from tapps import *
# 
# session = LoadCSV(session, os.sep.join([session['cwd'], 'data', 
                    # 'STI_2015.csv']))
# session = AttachNewDataFrame(session, 'STI')
# 
# testingA = NewPluginParameters(session, 'template')
# testingA['analysis_name'] = 'test'
# testingA['plugin_name'] = 'template'
# testingA['dataframe'] = session['MDF'].frames['STI']
# testingA['analytical_method'] = 'summation'
# session['parameters']['testingA'] = testingA
# 
# RunPlugin(session, 'testingA')
# 
# pprint(session)
# pprint(parameters)