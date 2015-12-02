'''
Index of Data Files for TAPPS

Date created: 1st December 2015

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

data_index = {
'ASX200': {'files': ['ASX200_2015.csv'],
           'url': 'http://finance.yahoo.com/q/hp?s=^AXJO+Historical+Prices',
           'description':'''S&P/ASX 200 Index. Australia.'''},
'HSI': {'files': ['HSI_2015.csv'],
         'url': 'http://finance.yahoo.com/q/hp?s=^HSI+Historical+Prices',
         'description':'''Hang Seng Index. Hong Kong.'''},
'N225': {'files': ['N225_2015.csv'],
         'url': 'http://finance.yahoo.com/q/hp?s=^HSI+Historical+Prices',
         'description':'''Nikkei 225 Stock Index. Japan.'''},
'S&P500': {'files': ['SP500_2015.csv'],
           'url': 'http://finance.yahoo.com/q/hp?s=^GSPC+Historical+Prices',
           'description':'''Standard and Poors 500 Index. USA.'''},
'STI': {'files': ['STI_2015.csv'],
        'url': 'http://finance.yahoo.com/q/hp?s=^STI+Historical+Prices'
        'description':'''Singapore Straits Times Industrial Index. 
        Index of 30 highest market capitalized companies in Singapore 
        Stocks Exchange.'''}
}
