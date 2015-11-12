import os
import sys

import plugins

session = \
{'paths': {'cwd': os.getcwd(),
           'plugins': os.sep.join([os.getcwd(), 'plugins']),
          },
 'plugins': {'loadFail': {},
             'loaded': [],
             'template': [],
            },
 'analyses': {
             },
}

plugin_categories = ['template']

def loadPlugin(plugin, session=session):
    checks = ['ImportError:Plugin',
              'ImportError:Manifest',
              'ImportError:MainFunction',
              'ManifestError:NoName',
              'ManifestError:NoRelease',
              'ManifestError:InvalidCategory',
              'ManifestError:NoShortDescription',
              'ManifestError:NoLongDescription',
              'ManifestError:NoURL',
              'ManifestError:NoContact',
              'ManifestError:NoLicense']
    try: 
        exec('from plugins import %s' % plugin)
        checks[0] = 'Passed'
    except: pass
    try: 
        exec('from plugins.%s import %s' % (plugin, 'manifest'))
        checks[1] = 'Passed'
    except: pass
    try: 
        exec('from plugins.%s.main import %s' % (plugin, 'main'))
        checks[2] = 'Passed'
    except: pass
    try: 
        plugin_name = manifest.name
        if plugin_name != '':
            checks[3] = 'Passed'
    except: pass
    try:
        release = manifest.release
        checks[4] = 'Passed'
    except: pass
    try:
        category = manifest.category
        if category in plugin_categories:
            checks[5] = 'Passed'
    except: pass
    try:
        sDesc = manifest.shortDescription
        checks[6] = 'Passed'
    except: pass
    try:
        lDesc = manifest.longDescription
        checks[7] = 'Passed'
    except: pass
    try:
        URL = manifest.projectURL
        checks[8] = 'Passed'
    except: pass
    try:
        contact = manifest.contactDetails
        checks[9] = 'Passed'
    except: pass
    try:
        license = manifest.license
        checks[10] = 'Passed'
    except: pass
    pass_rate = float(len([x for x in checks if x == 'Passed'])) / float(len(checks))
    if pass_rate < 1.0:
        session['plugins']['loadFail'][plugin] = checks
    else:
        session['plugins']['loaded'] = plugin_name
        session['plugins'][category].append(plugin_name)
        session['plugin_' + plugin_name] = {'main': main,
                                            'release': release,
                                            'sdesc': sDesc,
                                            'ldesc': lDesc,
                                            'URL': URL,
                                            'contact': contact,
                                            'license': license}
    return (session, checks)


def getPlugins(path=session['paths']['plugins'], session=session):
    plugin_directories = [x for x in os.walk(path)][0][1]
    for plugin in plugin_directories:
        (session, checks) = loadPlugin(plugin, session)
    for category in plugin_categories:
        plugin_list = session['plugins'][category]
        plugin_list = list(set(plugin_list))
        session['plugins'][category] = plugin_list
    return session
            

def startup(session=session):
    getPlugins(session['paths']['plugins'], session)
    return session