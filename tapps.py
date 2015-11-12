'''
TAPPS: Technical (Analysis) and Applied Statistics.

Date created: 11th November 2015
'''
import copads
from copads.dataframe import Series
from copads.dataframe import Dataframe

import startup

global session

session = startup.session
session = startup.startup(session)

def RunPlugin(plugin_name, parameters, session=session):
    plugin_name = 'plugin_' + plugin_name
    results = session[plugin_name]['main'](parameters)
    return results