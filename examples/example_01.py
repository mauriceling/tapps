# import os
# import sys
# from pprint import pprint
# 
# from tapps import *
# 
# session = LoadCSV(session, os.sep.join([session['cwd'], 'data', 
                    # 'STI_20151111_19871228.csv']))
# session = AttachNewDataFrame(session, 'STI')
# 
# parameters = NewPluginParameters(session, 'template')
# parameters['analysis_name'] = 'test'
# parameters['plugin_name'] = 'template'
# parameters['dataframe'] = session['MDF'].frames['STI']
# parameters['analytical_method'] = 'summation'
# session['parameters']['testingA'] = parameters
# 
# RunPlugin(session, 'testingA')
# 
# pprint(session)
# pprint(parameters)

show plugin list
show plugin template
show session
show environment

set cwd /Users/mauriceling/Dropbox/MyProjects/tapps/data
set separator ,
set fillin None
show environment

load csv STI_20151111_19871228.csv as STI

new template parameters as testingA
set parameter analysis_name in testingA as test
set parameter analytical_method in testingA as summation
set parameter dataframe in testingA as STI

runplugin testingA

new STI_summation dataframe from testingA results

pythonshell
