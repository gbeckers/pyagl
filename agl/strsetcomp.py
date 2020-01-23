import inspect
import pandas as pd
from . import strcomp

__all__ = ['availableanalysisfunctions', 'crosscorrelationmax',
           'sharedlengthnsubstringcount', 'longestsharedsubstringlength',
           'longestsharedsubstringduration', 'novellengthnsubstringcount',
           'commonstartduration', 'commonstartlength', 'issubstring', 'issame',
           'samestart', 'levenshtein', 'levenshtein']


class ComparisonMatrix(object):

    def __init__(self, resultsdict, dataaccessfunc, stringdata, comparison,
                 name, title=None):

        self.resultsdict = resultsdict
        self.dataaccessfunc = dataaccessfunc
        self.stringdata = stringdata
        self.comparison = comparison
        self.name = name
        self.title = title
        self.xstringlabels = stringdata[comparison[0]].labels()
        self.ystringlabels = stringdata[comparison[1]].labels()

    def __str__(self):
        return '<ComparisonMatrix>'

    __repr__ = __str__

    def get_matrix(self):

        matrix = []
        for xl in self.xstringlabels:
            cols = []
            for yl in self.ystringlabels:
                result = self.dataaccessfunc(self.resultsdict[xl][yl])
                cols.append(result)
            matrix.append(cols)
        return matrix

    def get_pandasdataframe(self, name=None):
        if name is None:
            name = self.name
        indextuples = []
        values = []
        c0 = self.comparison[0]
        c1 = self.comparison[1]
        values = {'cat1': [], 'cat2': [], 'str1': [], 'str2': [], name: []}
        for l0 in self.xstringlabels:
            for l1 in self.ystringlabels:
                values['cat1'].append(c0)
                values['cat2'].append(c1)
                values['str1'].append(l0)
                values['str2'].append(l1)
                values[name].append(self.dataaccessfunc(self.resultsdict[l0][l1]))
        colnames = ('cat1', 'cat2', 'str1', 'str2', name)
        #index = pd.DataFrame(indextuples, colnames=names)
        return pd.DataFrame(values, columns=colnames)


def _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                            title=None, comparison=('All', 'All')):
    """
    Private function that takes string data sets, applies an analysis function
    to each string from the first set in `comparison` with each string from 
    the second set in `comparison`. The sets should be defined in `stringdata`.

    The analysisf must take two strings as the first two arguments and 
    readingframe as the third.

    The dataaccessf can be used to further process the results of the
    analysisf before the result is returned. E.g. count the number of items
    returned by analysisf.

    Parameters
    ----------
    stringdata
    analysisf : a function
        The function compares two strings and returns an outcome. It must take 
        two strings as the first two arguments and readingframe as the third.
    dataaccessfunc : a function
    title
    comparison

    Returns
    -------
    A ComparisonMatrix instance that can be used for further analyses or 
    visualization.

    """
    callingfname = inspect.stack()[1][3]
    stringcategory0 = stringdata[comparison[0]]
    stringcategory1 = stringdata[comparison[1]]
    rf = stringdata.readingframe
    results = {}
    for s0label,s0 in stringcategory0.items():
        results[s0label] = {}
        for s1label,s1 in stringcategory1.items():
            results[s0label][s1label] = analysisf(s0, s1, readingframe=rf)
    return ComparisonMatrix(resultsdict=results,
                            dataaccessfunc=dataaccessfunc,
                            stringdata=stringdata,
                            comparison=comparison,
                            name=callingfname,
                            title=title)


def longestsharedsubstringlength(stringdata, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        items = strcomp.longestsharedsubstrings(s1, s2,
                                              readingframe=readingframe)
        if items:
            return int(len(items[0][0]) / readingframe)
        else:
            return 0

    def dataaccessfunc(count):
        return count

    title = 'Length longest shared substring'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def longestsharedsubstringduration(stringdata, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        return strcomp.longestsharedsubstringduration(s1, s2,
                                                  tokendurations=stringdata.tokendurations,
                                                  isiduration=stringdata.isiduration,
                                                  readingframe=readingframe)

    def dataaccessfunc(duration):
        return duration

    title = 'Duration longest shared substring'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def crosscorrelationmax(stringdata, comparison=('All', 'All')):
    analysisf = strcomp.crosscorrelationmax

    def dataaccessfunc(m): return m

    title = 'Maximum crosscorrelation'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def sharedlengthnsubstringcount(stringdata, n, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        return strcomp.sharedlengthnsubstrings(s1, s2, n, readingframe)

    def dataaccessfunc(item):
        if item != ():
            return sum([len(c[1]) for c in item])
        else:
            return 0

    title = 'Number of {}-length shared substrings'.format(n)
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def novellengthnsubstringcount(stringdata, n, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        return strcomp.novellengthnsubstrings(s2, s1, n, readingframe)

    def dataaccessfunc(item):
        if item != ():
            return len(item)
        else:
            return 0

    title = 'Number of novel {}-length substrings'.format(n)
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def commonstartlength(stringdata, comparison=('All', 'All')):
    analysisf = strcomp.commonstartlength

    def dataaccessfunc(item): return item

    title = "Length of shared start substring"
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def commonstartduration(stringdata, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        return strcomp.commonstartduration(s1, s2,
                                       tokendurations=stringdata.tokendurations,
                                       isiduration=stringdata.isiduration,
                                       readingframe=readingframe)

    def dataaccessfunc(duration): return duration

    title = 'Duration of shared start substring'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def issame(stringdata, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe): return s1 == s2

    def dataaccessfunc(item): return item

    title = 'Identical strings'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def issubstring(stringdata, comparison=('All', 'All')):
    analysisf = strcomp.issubstring

    def dataaccessfunc(item): return item

    title = 'Is substring'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def samestart(stringdata, n, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        return strcomp.samestart(s1, s2, n, readingframe)

    def dataaccessfunc(item): return item

    title = 'Has same {}-length substring start'.format(n)
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title, comparison=comparison)


def levenshtein(stringdata, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        return strcomp.levenshtein(s1, s2, readingframe)

    def dataaccessfunc(item): return item

    title = 'Levenshtein distance'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title, comparison=comparison)



availableanalysisfunctions = {
    'crosscorrelationmax': crosscorrelationmax,
    'sharedlengthnsubstringcount': sharedlengthnsubstringcount,
    'longestsharedsubstringlength': longestsharedsubstringlength,
    'longestsharedsubstringduration': longestsharedsubstringduration,
    'novellengthnsubstringcount': novellengthnsubstringcount,
    'commonstartduration': commonstartduration,
    'commonstartlength': commonstartlength,
    'issubstring': issubstring,
    'issame': issame,
    'samestart': samestart,
    'levenshtein': levenshtein
}
