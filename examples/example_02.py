#################################################################
# Example 02: Loading data and running a simple analysis via plugin
#################################################################

@include example_01.py

load csv STI_2015.csv as STI

new summarize parameter as testingA
set parameter analysis_name in testingA as test
set parameter analytical_method in testingA as by_series
set parameter dataframe in testingA as STI

runplugin testingA

new STI_summarize dataframe from testingA results

pythonshell

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
# testingA = NewPluginParameters(session, 'summarize')
# testingA['analysis_name'] = 'test'
# testingA['plugin_name'] = 'template'
# testingA['dataframe'] = session['MDF'].frames['STI']
# testingA['analytical_method'] = 'by_series'
# session['parameters']['testingA'] = testingA
# 
# RunPlugin(session, 'testingA')
# 
# pprint(session)
# pprint(parameters)