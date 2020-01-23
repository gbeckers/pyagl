# FIXME can we get rid of numpy?
import numpy as np
from .argvalidation import checkpositiveint, checkstring

from .strfuncs import lengthnsubstrings

__all__ = ['commonstart', 'commonstartlength', 'commonstartduration',
           'crosscorrelate', 'crosscorrelationmax', 'sharedlengthnsubstrings',
           'longestsharedsubstrings', 'longestsharedsubstringlength',
           'longestsharedsubstringduration',
           'novellengthnsubstrings', 'samestart', 'occursin',
           'sharedsubstrings', 'issame']

# Notations:
# ---------
# s1, s2, ..., sn : strings
# s1ss, s2ss, ..., snss: sharedsubstrings of s1, s2, ..., sn
# ss1, ss2, ..., ssn : sharedsubstrings


def sharedlengthnsubstrings(s1, s2, n, readingframe=1):
    """
    Finds length-n shared substrings of s1 in s2.

    Parameters
    ----------
    s1 : string
        Token string from which length-n substrings are analyzed
    s2 : string
        Token string within which length-n substrings of s1 are matched
    n : positive int
        Length of the shared substrings that are considered
    readingframe : positive int, default 1
        The number of characters that make up one string token. This will
        often be `1`, so that, e.g. the string "abcd" has 4 tokens. However if
        there are more tokens than can be coded in ascii symbols,
        the larger readingframes are the solution. E.g., if readingframe is 2,
        then "a1a2" has two tokens, namely "a1" and "a2".

    Returns
    -------
    Tuple with hits. Each hit is a two-tuple, containing a substring match and 
    a two-tuple of the positions where the shared  substrings occur in s1 and 
    s2. Note that the positions refer to the token strings, and not python 
    strings. They take into account the reading frame.

    Examples
    --------
    >>> from aglcheck.strcomp import sharedlengthnsubstrings
    >>> sharedlengthnsubstrings('abcdefg', 'cdfgbcd', n=2)
    (('bc', ((1, 4),)), ('cd', ((2, 0), (2, 5))), ('fg', ((5, 2),)))
    >>> sharedlengthnsubstrings('a1a2c1b2b1', 'c1b2b1a1a2', n=2, readingframe=2)
    (('a1a2', ((0, 3),)), ('c1b2', ((2, 0),)), ('b2b1', ((3, 1),)))

    """

    checkpositiveint(readingframe)
    checkstring(s1, readingframe=readingframe)
    checkstring(s2, readingframe=readingframe)
    checkpositiveint(n)
    s1ss = lengthnsubstrings(s1, n=n, readingframe=readingframe)
    matches = []
    for pos, substring in enumerate(s1ss):
        positions = []
        for i in range(0, len(s2), readingframe):
            if substring == s2[i:i + n * readingframe]:
                positions.append((pos, int(i/readingframe)))
        if len(positions) > 0:
            matches.append((substring, tuple(positions)))
    return tuple(matches)


def sharedsubstrings(s1, s2, readingframe=1):
    """
    Finds all possible shared substrings of s1 in s2.

    Parameters
    ----------
    s1 : string
        Token string from which length-n substrings are generated.
    s2 : string
        Token string within which length-n substrings of s1 are matched.
    readingframe : positive int, default 1
        The number of characters that make up one string token. Normally 1,
        so that, e.g. the string "abcd" has 4 tokens. However if there exist
        many tokens, these can be coded with multiple ascii symbols. E.g., if
        readingframe is 2, then "a1a2" has two tokens, namely "a1" and "a2".

    Returns
    -------
    Tuple with hits. Each hit is a two-tuple, containing a substring match and 
    a two-tuple of the positions where the shared  substrings occur in s1 and 
    s2. Note that the positions refer to the token strings, and not python 
    strings. They take into account the reading frame.

    Examples
    --------
    >>> from aglcheck.strcomp import sharedsubstrings
    >>> sharedsubstrings('abcd', 'cdecd')
    ((('c', ((2, 0), (2, 3))), ('d', ((3, 1), (3, 4)))),
     (('cd', ((2, 0), (2, 3))),))
    >>> sharedsubstrings('a1a2', 'a2a3a1a2', readingframe=2)
    ((('a1', ((0, 2),)), ('a2', ((1, 0), (1, 3)))), (('a1a2', ((0, 2),)),))
     
    """

    matches = [sharedlengthnsubstrings(s1, s2, n, readingframe)
               for n in range(1, len(s1) + 1)]
    # remove empty 'matches'
    return tuple(match for match in matches if match)


def longestsharedsubstrings(s1, s2, readingframe=1):
    """
    Finds longest shared substrings of s1 in s2. If there are multiple
    matches, return every match.

    Parameters
    ----------
    s1 : string
        Token string from which length-n substrings are generated.
    s2 : string
        Token string within which length-n substrings of s1 are matched.
    readingframe : positive int, default 1
        The number of characters that make up one string token. Normally 1,
        so that, e.g. the string "abcd" has 4 tokens. However if there exist
        many tokens, these can be coded with multiple ascii symbols. E.g., if
        readingframe is 2, then "a1a2" has two tokens, namely "a1" and "a2".

    Returns
    -------
    Tuple with hits. Each hit is a two-tuple, containing a substring match and 
    a two-tuple of the positions where the shared  substrings occur in s1 and 
    s2. Note that the positions refer to the token strings, and not python 
    strings. They take into account the reading frame.

    Examples
    --------
    >>> from aglcheck.strcomp import longestsharedsubstrings
    >>> longestsharedsubstrings('acd', 'cdacdeacd')
    (('acd', ((0, 2), (0, 6))),)
    >>> longestsharedsubstrings('acde', 'cdbcdeacd')
    (('acd', ((0, 6),)), ('cde', ((1, 3),)))
    >>> longestsharedsubstrings('a1a2', 'a2a3a1a2a1', readingframe=2)
    (('a1a2', ((0, 2),)),)
    
    """
    for n in range(len(s1)//readingframe, 0, -1):
        matches = sharedlengthnsubstrings(s1, s2, n, readingframe)
        if matches:
            return matches
    return ()


def longestsharedsubstringlength(s1, s2, readingframe=1):
    """
    Finds the length of the longest shared substrings of s1 in s2.

    Parameters
    ----------
    s1 : string
        Token string from which length-n substrings are generated.
    s2 : string
        Token string within which length-n substrings of s1 are matched.
    readingframe : positive int, default 1
        The number of characters that make up one string token. Normally 1,
        so that, e.g. the string "abcd" has 4 tokens. However if there exist
        many tokens, these can be coded with multiple ascii symbols. E.g., if
        readingframe is 2, then "a1a2" has two tokens, namely "a1" and "a2".

    Returns
    -------
    int
        Length of longest shared substring

    Examples
    --------
    >>> from aglcheck.strcomp import longestsharedsubstrings
    >>> longestsharedsubstrings('acd', 'cdacdeacd')
    3
    >>> longestsharedsubstrings('acde', 'cdbcdeacd')
    3
    >>> longestsharedsubstrings('a1a2', 'a2a3a1a2a1', readingframe=2)
    2

    """
    items = longestsharedsubstrings(s1=s1, s2=s2, readingframe=readingframe)
    if items:
        return int(len(items[0][0]) / readingframe)
    else:
        return 0


def longestsharedsubstringduration(s1, s2, tokendurations, isiduration,
                                   readingframe=1):
    """
        Finds longest shared substrings of s1 in s2, and calculates their 
        duration.

        Parameters
        ----------
        s1 : string
            Token string from which length-n substrings are generated.
        s2 : string
            Token string within which length-n substrings of s1 are matched.
        tokendurations: dict
            A dictionary in which every token occurring in s1 and s2 is a key
            that maps to its duration.
        isiduration: float
            The duration of silence between tokens. Assumed to be fixed.
        readingframe : positive int, default 1
            The number of characters that make up one string token. Normally 1,
            so that, e.g. the string "abcd" has 4 tokens. However if there exist
            many tokens, these can be coded with multiple ascii symbols. E.g., if
            readingframe is 2, then "a1a2" has two tokens, namely "a1" and "a2".

        Returns
        -------
        float: duration of the longest shared substring.

        Examples
        --------
        >>> from aglcheck.strcomp import longestsharedsubstringduration
        >>> longestsharedsubstringduration('abc', 'aab', {'a': 1., 'b': 2.}, .2)
        3.2
        
    """
    durations = [0.]
    for s, positions in longestsharedsubstrings(s1=s1, s2=s2,
                                                readingframe=readingframe):
        elements = [s[i:i + readingframe] for i in
                    range(0, len(s), readingframe)]
        sounddur = sum([tokendurations[el] for el in elements])
        durations.append(sounddur + (len(elements) - 1) * isiduration)
    return float(np.max(durations))


def novellengthnsubstrings(s1, s2, n, readingframe=1):
    """
    Finds length-n shared substrings of s1 that are absent in s2.

    Parameters
    ----------
    s1 : string
        Token string from which length-n substrings are generated.
    s2 : string
        Token string within which length-n substrings of s1 are matched
    n : positive int
        Length of the shared substrings that are considered
    readingframe : positive int, default 1
        The number of characters that make up one string token. Normally 1,
        so that, e.g. the string "abcd" has 4 tokens. However if there exist
        many tokens, these can be coded with multiple ascii symbols. E.g., if
        readingframe is 2, then "a1a2" has two tokens, namely "a1" and "a2".

    Returns
    -------
    Tuple with hits. Each hit is a two-tuple, containing a substring match and 
    a nuber of the positions where the novel substrings occur in s1. Note 
    that the positions refer to the token strings, and not python strings. 
    They take into account the reading frame.

    Examples
    --------
    >>> from aglcheck.strcomp import novellengthnsubstrings
    >>> novellengthnsubstrings('abcdef', 'adcdeg', n=2)
    (('ab', 0), ('bc', 1), ('ef', 4))
    >>> novellengthnsubstrings('abcdefgh', 'abcdeggh', n=2, readingframe=2)
    (('cdef', 1), ('efgh', 2))
    
    """

    checkpositiveint(readingframe)
    checkstring(s1, readingframe=readingframe)
    checkstring(s2, readingframe=readingframe)
    checkpositiveint(n)
    # which length-n substrings exist in in s1?
    s1ss = lengthnsubstrings(s1, n=n, readingframe=readingframe)
    s2ss = set(lengthnsubstrings(s2, n=n, readingframe=readingframe))
    return tuple((ss, pos) for pos, ss in enumerate(s1ss) if ss not in s2ss)



def commonstart(s1, s2, readingframe=1):
    """
    Returns the substring that s1 and s2 share from the beginning.

    Parameters
    ----------
    s1 : string
        Token string
    s2 : string
        Token string
   readingframe : positive int, default 1
        The number of characters that make up one string token. Normally 1,
        so that, e.g. the string "abcd" has 4 tokens. However if there exist
        many tokens, these can be coded with multiple ascii symbols. E.g., if
        readingframe is 2, then "a1a2" has two tokens, namely "a1" and "a2".

    Returns
    -------
    string: Token string that s1 and s2 share from the beginning.
    
    Examples
    --------
    >>> from aglcheck.strcomp import commonstart
    >>> commonstart('abcde', 'abcef')
    'abc'
    >>> commonstart('abcdef', 'abcefg', readingframe=2)
    'ab'
    
    """
    # check if parameters make sense
    checkstring(s1, readingframe=readingframe)
    checkstring(s2, readingframe=readingframe)
    checkpositiveint(readingframe)

    i = sum([s2.startswith(s1[:i]) for i in
             range(readingframe, len(s1) + 1, readingframe)])
    return s1[:i * readingframe]


def commonstartlength(s1, s2, readingframe=1):
    """
    Counts the length of the substring that both s1 and s2 start with.

    """
    return len(commonstart(s1=s1, s2=s2,
                           readingframe=readingframe)) // readingframe


def commonstartduration(s1, s2, tokendurations, isiduration, readingframe=1):
    s = commonstart(s1=s1, s2=s2, readingframe=readingframe)
    elements = [s[i:i + readingframe] for i in range(0, len(s), readingframe)]
    sounddur = np.sum([tokendurations[el] for el in elements])
    if len(elements) > 0:
        return sounddur + (len(elements) - 1) * isiduration
    else:
        return 0.


def crosscorrelate(s1, s2, readingframe=1, full=True):
    checkstring(s1, readingframe=readingframe)
    checkstring(s2, readingframe=readingframe)
    checkpositiveint(readingframe)
    if readingframe > 1:
        s1 = [s1[i:i + readingframe] for i in range(0, len(s1), readingframe)]
        s2 = [s2[i:i + readingframe] for i in range(0, len(s2), readingframe)]
    sa1 = np.array(list(s1))
    sa2 = np.zeros(2 * len(s1) + len(s2) - 2, dtype=sa1.dtype)
    sa2[sa1.size - 1:sa1.size + len(s2) - 1] = list(s2)
    nsteps = len(sa2) - len(sa1)
    ccp = [(sa1 == sa2[i:i + sa1.size]) for i in range(nsteps + 1)]
    ccs = [[item if isequal else '' for (isequal, item) in zip(cc, sa1)] for cc
           in ccp]
    ccf = np.array([(sa1 == sa2[i:i + sa1.size]).sum()
                    for i in range(nsteps + 1)])

    if full:
        return ccf, ccs
    else:
        return ccf[sa1.size - 1:-(sa1.size - 1)], \
               ccs[sa1.size - 1:-(sa1.size - 1)]


def crosscorrelationmax(s1, s2, readingframe=1, full=True):
    cc = crosscorrelate(s1=s1, s2=s2, readingframe=readingframe, full=full)
    return max(cc[0])


def issubstring(s1, s2, readingframe=1):
    """Is s1 a substring of s2"""
    checkstring(s1, readingframe=readingframe)
    checkstring(s2, readingframe=readingframe)
    return s2.count(s1) > 0


def issame(s1, s2, readingframe=1):
    """Is s1 identical to s2"""
    checkstring(s1, readingframe=readingframe)
    checkstring(s2, readingframe=readingframe)
    return s1==s2


def occursin(s1, s2, readingframe=1):
    n = len(s1)
    result = sharedlengthnsubstrings(s1, s2, n=n, readingframe=readingframe)
    if result:
        return result[0] # only one match is possible
    else:
        return result # empty tuple


def startswith(s1, s2, readingframe=1):
    checkstring(s1, readingframe=readingframe)
    checkstring(s2, readingframe=readingframe)
    return s1.startswith(s2)


def samestart(s1, s2, n, readingframe=1):
    checkstring(s1, readingframe=readingframe)
    checkstring(s2, readingframe=readingframe)
    return s1[:n * readingframe] == s2[:n * readingframe]


def levenshtein(s1, s2, readingframe=1):
    """
    Code adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation
    /Strings/Levenshtein_distance#Python

    """
    checkstring(s1, readingframe=readingframe)
    checkstring(s2, readingframe=readingframe)
    checkpositiveint(readingframe)
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    if readingframe > 1:
        s1 = [s1[i:i + readingframe] for i in range(0, len(s1), readingframe)]
        s2 = [s2[i:i + readingframe] for i in range(0, len(s2), readingframe)]
    previous_row = range(0, len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]
