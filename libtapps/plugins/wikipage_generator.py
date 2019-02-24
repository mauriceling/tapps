'''!
Generates Wiki page for plugin using plugin's manifest data.

Date created: 4th December 2015

Copyright (C) 2015, Maurice HT Ling for TAPPS Development Team.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys

text = '''**Download URL:** %s

**Category:** %s

**Latest release number:** %s

**Description:** %s

%s

**Contact Details:** %s

**Licence:** %s
'''

if __name__ == '__main__':
    plugin_name = sys.argv[1]
    outfile = sys.argv[1] + '.txt'
    exec('import %s' % plugin_name)
    exec('from %s import manifest as manifest' % plugin_name)
    name = str(manifest.name)
    release = str(manifest.release)
    category = str(manifest.category)
    shortDescription = str(manifest.shortDescription)
    longDescription = str(manifest.longDescription)
    projectURL = str(manifest.projectURL)
    'https://github.com/mauriceling/tapps/tree/master/plugins/summarize_1'
    contactDetails = str(manifest.contactDetails)
    license = str(manifest.license)
    if projectURL.startswith('https://github.com/mauriceling/tapps'):
       projectURL = 'This plugin is already included in TAPPS base system'
    text = text % (projectURL,
                   category,
                   release,
                   shortDescription,
                   longDescription,
                   contactDetails,
                   license)
    f = open(outfile, 'w')
    f.write(text)
    f.close()
    