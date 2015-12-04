'''
Manifest file for Plugin: summarize

Date created: 4th December 2015

Copyright (C) 2015, Maurice HT Ling

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

# Name of the plugin / app (mandatory)
name = 'summarize'

# Version or release number of the plugin / app (mandatory)
release = 1

# Category which this plugin / app should belong to (mandatory)
# Allowed categories are:
# 1. exporter
# 2. importer
# 3. statistics
# 4. statistics.hypothesis
# 5. statistics.model
# 6. statistics.timeseries
# 7. unclassified
category = 'statistics'

# A short description of the plugin / app (not mandatory)
shortDescription = '''Generates summary statistics of a dataframe, by 
series or by labels'''

# Long description of the plugin / app (not mandatory)
longDescription = '''List of summary statistics generated: (1) arithmetic 
mean, (2) count, (3) maximum value, (4) median, (5) minimum value, 
(6) standard deviation, (7) summation'''

# URL of this project, if any (not mandatory)
projectURL = 'https://github.com/mauriceling/tapps/tree/master/plugins/summarize_1'

# Person(s) to contact for any help or information regarding this plugin / app
# (not mandatory)
contactDetails = 'Maurice Ling <mauriceling@acm.org>'

# License for this plugin / app (not mandatory)
# If no license is given, it is deemed to be released into public domain 
# for all uses, both academic and industry. 
license = '''General Public Licence version 3

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''