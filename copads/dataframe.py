'''
A generic series and data frame to hold data and analysis
Date created: 24th September 2012
Licence: Python Software Foundation License version 2
'''
import string
import random

from copadsexceptions import FunctionParameterValueError

class Series(object):
    '''
    A data series is essentially a labeled list or vector. Each item in 
    the list/vector is given a label for identification and retrieval. 
    Hence, the number of labels and the number of data elements must be 
    equal.
    
    In itself, a data series can be viewed as a column of data in a data 
    table where the name of the series corresponds to the field name; such 
    as::
    
        <Label>    Height
        Tom        165
        Ellis      191
        Richard    172
        Melvin     175
    '''
    def __init__(self, name=''):
        '''
        Constructor. Initialize data series with a name.
        
        @param name: Name of this data series. Default is empty name.
        @type name: string
        '''
        self.name = str(name)
        self.data = []
        self.label = []
        self.analyses = {}
        
    def addData(self, data, label=[]):
        '''
        Method to add data into the data series. If provided, the number 
        of elements in data and label have to be the same. However, the 
        labels need not be unique (duplicated labels are allowed) but this 
        is highly undesirable as it can cause issues which requires unique 
        labels.
        
        @param data: list of data values.
        @type data: list
        @param label: list of labels for the data values. If not given, 
        a sequential number will be given as label but this does not ensure 
        uniqueness in label names across the entire series.
        @type label: list
        '''
        if len(label) == 0:
            label = range(len(data))
        if len(data) != len(label):
            raise FunctionParameterValueError()
        for i in range(len(data)):
            self.data.append(data[i])
            self.label.append(label[i])
        
    def changeDatum(self, new_value, label):
        '''
        Method to change the data value of a label. If the label is not 
        found within the data series, nothing will be changed.
        
        @param new_value: the new value for the label.
        @param label: the label name for the data value to be changed.
        '''
        try: 
            index = self.label.index(label)
            self.data[index] = new_value
        except ValueError: pass
        
    def changeLabel(self, new_label, original_label):
        '''
        Method to change the name of an existing label. If the existing 
        (original) label is not found within the data series, nothing will 
        be changed.
        
        @param new_label: the new name for the label.
        @param original_label: the existing (original) label name to be 
        changed.
        '''
        try:
            index = self.label.index(original_label)
            self.label[index] = new_label
        except ValueError: pass
      
    def getDatum(self, label):
        '''
        Method to get data value for a given label. If the label is not 
        found within the data series, None will be returned.
        
        @param label: the label name for the data value to retrieve.
        @return: data value tagged to the label (if found), or None (if the 
        label is not found).
        '''
        try:
            index = self.label.index(label)
            return self.data[index]
        except ValueError: return None
        
    def getLabels(self, datum):
        '''
        Method to get label name(s) for a given data value.
        
        @param datum: the data value to retrieve its corresponding label.
        @return: [None] if data value is not found; list of one or more 
        label names if the data value is found.
        @rtype: list
        '''
        labels = [self.label[index] 
                  for index in range(len(self.data)) 
                     if self.data[index] == datum]
        if len(labels) == 0: return [None]
        if len(labels) > 0: return labels
        
    
class Dataframe(object):
    '''
    A data frame is an encapsulation of one or more data series and its 
    associated analyses. Hence, a data frame can be formed using one or 
    more data series where data elements across series are linked up by 
    their respective labels. As a result, a data frame can be viewed as 
    a table or spreadsheet. 
    
    For example, a data frame of ::
    
        <Label>    Height   Weight
        Tom        165      62
        Ellis      191      85
        Richard    172      68
        Melvin     175      67
        
    can be formed using 2 data series - Height, and Weight; where each 
    data series has 'Tom', 'Ellis', 'Richard', and 'Melvin' as labels.
    '''
    def __init__(self, name=''):
        '''
        Constructor. Initialize data frame with a name.
        
        @param name: Name of this data frame. Default is empty name.
        @type name: string
        '''
        self.name = str(name)
        self.series_names = []
        self.data = {}
        self.label = []
        self.analyses = {}
    
    def _generateRandomName(self):
        '''
        Private method to generate a 8-character upper case name to be used 
        as series names.
        
        @return: generated name.
        @rtype: string
        '''
        name = ''.join([random.choice(string.ascii_uppercase) 
                        for i in range(8)])
        while name in self.series_name:
            name = ''.join([random.choice(string.ascii_uppercase) 
                            for i in range(8)])
        return name
        
    def addSeries(self, series, fill_in=None):
        '''
        Method to add a data series into the data frame.
        
        @param series: data series (dataframe.Series object) for addition.
        @param fill_in: value to fill into missing values during process. 
        This is required as the number of data elements across each label 
        must be the same. Hence, filling in of missing values can occur 
        when (1) the newly added data series consists of new labels which 
        are not found in the current data frame (this will require filling 
        in of missing values in the current data frame), or (2) the current 
        data frame consists of labels that are not found in the newly 
        added data series (this will require filling in of missing values 
        to the newly added data series). Default = None.
        '''
        if series.name == '':
            series.name = self._generateRandomName()
        df_label = self.data.keys()
        for i in range(len(series.data)):
            if series.label[i] not in df_label:
                temp = [fill_in] * len(self.series_names)
                temp.append(series.data[i])
                self.data[series.label[i]] = temp
            else:
                temp = self.data[series.label[i]]
                temp.append(series.data[i])
                self.data[series.label[i]] = temp
        self.series_names.append(series.name)
        self.label = self.data.keys()
        for k in self.label:
            if len(self.data[k]) < len(self.series_names):
                temp = self.data[k]
                temp.append(fill_in)
                self.data[k] = temp
                
    def addData(self, dataset, labels, fill_in=None):
        '''
        Method to add new data into the current data frame. For example, 
        
        >>> df = d.Dataframe('frame1')
        >>> dataset = {'seriesA': [10, 11, 12, 13, 14],
                       'seriesB': [20, 21, 22, 23, 24],
                       'seriesC': [30, 31, 32, 33, 34],
                       'seriesD': [40, 41, 42, 43, 44]}
        >>> label = ['A', 'B', 'C', 'D', 'E']
        >>> df.addData(dataset, label)
        
        will result in::
        
                seriesA  seriesB  seriesC  seriesD
            A   10       20       30       40
            B   11       21       31       41
            C   12       22       32       42
            D   13       23       33       43
            E   14       24       34       44
        
        @param dataset: set of data to add. This is formatted as a 
        dictionary where the key is the series name and the value is a list 
        of data values of the same number of elements as labels.
        @type dataset: dictionary
        @param labels: list of labels for the data values. If not given, 
        a sequential number will be given as label but this does not ensure 
        uniqueness in label names across the entire series.
        @type label: list
        @param fill_in: value to fill into missing values during process. 
        This is required as the number of data elements across each label 
        must be the same. Hence, filling in of missing values can occur 
        when (1) the newly added data series consists of new labels which 
        are not found in the current data frame (this will require filling 
        in of missing values in the current data frame), or (2) the current 
        data frame consists of labels that are not found in the newly 
        added data series (this will require filling in of missing values 
        to the newly added data series). Default = None.
        '''
        series_names = dataset.keys()
        series_names.sort()
        for series_name in series_names:
            s = Series(str(series_name))
            s.addData(dataset[series_name], labels)
            self.addSeries(s, fill_in)
            
    def addCSV(self, filepath, series_header=True, separator=',', 
               fill_in=None, newline='\n'):
        '''
        Method to add data from comma-delimited file (CSV) into current 
        data frame.
        
        @param filepath: path to CSV file.
        @type filepath: string
        @param series_header: boolean flag to denote whether the first row 
        in the CSV file contains the data header. It is highly recommended 
        that header is included in the CSV file. Default = True (header is 
        included)
        @param separator: item separator within the CSV file. Default = ','
        @param fill_in: value to fill into missing values during process. 
        This is required as the number of data elements across each label 
        must be the same. Hence, filling in of missing values can occur 
        when (1) the newly added data series consists of new labels which 
        are not found in the current data frame (this will require filling 
        in of missing values in the current data frame), or (2) the current 
        data frame consists of labels that are not found in the newly 
        added data series (this will require filling in of missing values 
        to the newly added data series). Default = None.
        @param newline: character to denote new line or line feed in the 
        CSV file. Default = '\n'
        '''
        data = open(filepath, 'r').readlines()
        data = [x[:(-1)*len(newline)] for x in data]
        data = [[item.strip() 
                 for item in x.split(separator)] 
                for x in data]
        if series_header:
            series = data[0][1:]
            data = data[1:]
        labels = [x[0] for x in data]
        data = [x[1:] for x in data]
        data = zip(*data)
        for i in range(len(series)):
            s = Series(series[i])
            s.addData(data[i], labels)
            self.addSeries(s, fill_in)
            
    def changeDatum(self, new_value, series, label):
        '''
        Method to change the data value of a series and label. If the 
        series or label is not found within the data series, nothing will 
        be changed.
        
        @param new_value: the new value for the label.
        @param series: the series name for the data value to be changed.
        @param label: the label name for the data value to be changed.
        '''
        try: 
            s = self.series_names.index(series)
            self.data[label][s] = new_value
        except ValueError: pass
        except KeyError: pass
        
    def changeSeriesName(self, new_name, original_name):
        '''
        Method to change the name of an existing series. If the existing 
        (original) series name is not found within the data series, nothing 
        will be changed.
        
        @param new_name: the new name for the series.
        @param original_name: the existing (original) series name to be 
        changed.
        '''
        try:
            index = self.series_names.index(original_name)
            self.series_names[index] = new_name
        except ValueError: pass
  
    def changeLabel(self, new_label, original_label):
        '''
        Method to change the name of an existing label. If the existing 
        (original) label is not found within the data series, nothing will 
        be changed.
        
        @param new_label: the new name for the label.
        @param original_label: the existing (original) label name to be 
        changed.
        '''
        try:
            data = [x for x in self.data[original_label]]
            self.data[new_label] = data
            del self.data[original_label]
        except KeyError: pass
        try:
            index = self.label.index(original_label)
            self.label[index] = new_label
        except ValueError: pass
        
    def getDatum(self, series, label):
        '''
        Method to get data value for a given series and label names. If the 
        series name or label name is not found within the data series, None 
        will be returned.
        
        @param series: the series name for the data value to retrieve.
        @param label: the label name for the data value to retrieve.
        @return: data value tagged to the series and label (if found), or 
        None (if the series or label is not found).
        '''
        try:
            s = self.series_names.index(series)
            return self.data[label][s]
        except ValueError: return None
        except KeyError: return None
        
    def getLabels(self, datum):
        '''
        Method to get label name(s) for a given data value. However, this 
        method does not return the series name from which the data value 
        is/are found.
        
        @param datum: the data value to retrieve its corresponding label.
        @return: [None] if data value is not found; list of one or more 
        label names if the data value is found.
        @rtype: list
        '''
        labels = [label
                  for label in self.data.keys()
                     for series in range(len(self.data[label]))
                         if self.data[label][series] == datum]
        if len(labels) == 0: return [None]
        if len(labels) > 0: return labels
        
    def getSeries(self, datum):
        '''
        Method to get series name(s) for a given data value. However, this 
        method does not return the label name from which the data value 
        is/are found.
        
        @param datum: the data value to retrieve its corresponding series.
        @return: [None] if data value is not found; list of one or more 
        series names if the data value is found.
        @rtype: list
        '''
        series = [self.series_names[series]
                  for label in self.data.keys()
                     for series in range(len(self.data[label]))
                         if self.data[label][series] == datum]
        if len(series) == 0: return [None]
        if len(series) > 0: return series
        
    def getSeriesLabels(self, datum):
        '''
        Method to get series name(s) and label name(s) for a given data 
        value. This method returns the a list of coodinates tuples, 
        (series name, label name) in which the given data value is found.
        
        @param datum: the data value to retrieve its corresponding 
        coordinates.
        @return: [(None, None)] if data value is not found; list of one or 
        more coordinates if the data value is found.
        @rtype: list
        '''
        coordinates = [(self.series_names[series], label)
                       for label in self.data.keys()
                           for series in range(len(self.data[label]))
                               if self.data[label][series] == datum]
        if len(coordinates) == 0:  return [(None, None)]
        else: return list(set(coordinates))
        
        
class MultiDataframe(object):
    '''
    A multidata frame is a container of one or more data frames. This 
    allows for processing across more than one data frames.
    '''

    def __init__(self, name=''):
        '''
        Constructor. Initialize multidata frame with a name.
        
        @param name: Name of this data frame. Default is empty name.
        @type name: string
        '''
        self.name = str(name)
        self.frames = {}
        self.frame_names = []
        self.analyses = {}
        
    def addDataframe(self, dataframe, replace=False):
        '''
        Method to add a data frame. It is highly encouraged that all 
        data frames to be added have their own identifying names. In event 
        whereby the data frame does not have a name, a randomly generated 
        8-character name will be assigned.
        
        This method allows for replacement of existing data frame when 
        'replace' flag is set to True. In event where 'replace' flag is 
        False (do not replace existing data frame, if present) and there 
        is an existing data frame with the same name, a randomly generated 
        8-character name will be appended to the name of the data frame to 
        be added.
        '''
        df_name = dataframe.name
        used_names = self.frames.keys()
        if (not replace) and (df_name in used_names):
            while df_name in used_names:
                df_name = df_name + '_' + \
                          ''.join([random.choice(string.ascii_uppercase) 
                                for i in range(8)])
            dataframe.name = df_name
        if df_name == '':
            name = ''.join([random.choice(string.ascii_uppercase) 
                            for i in range(8)])
            while name in used_names:
                name = ''.join([random.choice(string.ascii_uppercase) 
                                for i in range(8)])
            dataframe.name = name
        self.frames[dataframe.name] = dataframe
        self.frame_names.append(dataframe.name)
