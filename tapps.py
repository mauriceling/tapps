'''
TAPPS: Technical (Analysis) and Applied Statistics.

Date created: 11th November 2015

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