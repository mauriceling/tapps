import startup

global session

session = startup.session
session = startup.startup(session)

def RunPlugin(plugin_name, parameters, session=session):
    results = session['plugin_' + plugin_name]['main'](dataframe, parameters)
    return results