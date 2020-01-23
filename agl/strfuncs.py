from functools import lru_cache

__all__ = ['lengthnsubstrings', 'substrings', 'lengthnhead',
           'lengthntail', 'lengthnanchors', 'heads', 'tails', 'anchors']


def lengthnsubstrings(s, n, readingframe=1):
    """
    Returns a tuple of consecutive length-n substrings of s.

    Parameters
    ----------
    s : string
        Token string from which length-n substrings are generated, or an
        iterable of them.
    n : positive int
        Length of the shared substrings that are considered
    readingframe : positive int, default 1
        The number of characters that make up one string token. Normally 1,
        so that, e.g. the string "abcd" has 4 tokens. However if there exist
        many tokens, these can be coded with multiple ascii symbols. E.g., if
        readingframe is 2, then "a1a2" has two tokens, namely "a1" and "a2".

    Returns
    -------
    Tuple with substrings

    Examples
    --------
    >>> from agl.strfuncs import lengthnsubstrings
    >>> lengthnsubstrings('abcdefghi', n=4)
    ('abcd', 'bcde', 'cdef', 'defg', 'efgh', 'fghi')
    >>> lengthnsubstrings('a1a2a3c1b3b2b1', n=4, readingframe=2)
    ('a1a2a3c1', 'a2a3c1b3', 'a3c1b3b2', 'c1b3b2b1')

    """
    #separate function so that we can memoize and still have docstring
    @lru_cache(maxsize=512)
    def _lengthnsubstrings(s, n, readingframe=1):
        # how many length-n substrings exist in in s?
        nss = int(len(s) / readingframe) - n + 1
        nglyphs = n * readingframe
        return tuple(s[i:i + nglyphs] for i in range(0, nss * readingframe,
                                               readingframe))

    return _lengthnsubstrings(s=s, n=n, readingframe=readingframe)


def substrings(s, minlength=1, maxlength=None, readingframe=1):
    """
    Returns a tuple of all consecutive substrings of s.

    Note that this includes the full string itself.

    Parameters
    ----------
    s : string
        Token string from which length-n substrings are generated, or an
        iterable of them.
    minlength : positive int
        Minimum length of the shared substrings that are considered
    maxlength : positive int
        Maximum length of the shared substrings that are considered
    readingframe :  positive int, default 1
        The number of characters that make up one string token. Normally 1,
        so that, e.g. the string "abcd" has 4 tokens. However if there exist
        many tokens, these can be coded with multiple ascii symbols. E.g., if
        readingframe is 2, then "a1a2" has two tokens, namely "a1" and "a2".

    Returns
    -------
    Tuple with substrings

    Examples
    --------
    >>> from agl.strfuncs import substrings
    >>> substrings('cdef')
    ('c', 'd', 'e', 'f', 'cd', 'de', 'ef', 'cde', 'def', 'cdef')
    >>> substrings('cdef', readingframe=2)
    ('cd', 'ef', 'cdef')

    """

    @lru_cache(maxsize=512)
    def _substrings(s, minlength=1, maxlength=None, readingframe=1):
        if maxlength is None:
            maxlength = int(len(s) / readingframe)
        ss = []
        for n in range(minlength, maxlength + 1):
            ss.extend(lengthnsubstrings(s, n=n, readingframe=readingframe))
        return tuple(ss)
    return _substrings(s=s, minlength=minlength, maxlength=maxlength,
                       readingframe=readingframe)

# FIXME functions next need doc
def lengthnhead(s, n, readingframe=1):
    return s[:n*readingframe]

def lengthntail(s, n, readingframe=1):
    return s[-n*readingframe:]

def lengthnanchors(s, n, readingframe=1):
    return tuple((lengthnhead(s, n, readingframe=readingframe),
                  lengthntail(s, n, readingframe=readingframe)))

# FIXME functions next need doc and tests
def heads(s, minlength=1, maxlength=None, readingframe=1):
    if maxlength is None:
        maxlength = int(len(s) / readingframe)
    return tuple(lengthnhead(s, n=n, readingframe=readingframe)
                     for n in range(minlength, maxlength + 1))

def tails(s, minlength=1, maxlength=None, readingframe=1):
    if maxlength is None:
        maxlength = int(len(s) / readingframe)
    return tuple(lengthntail(s, n=n, readingframe=readingframe)
                     for n in range(minlength, maxlength + 1))

def anchors(s, minlength=1, maxlength=None, readingframe=1):
    if maxlength is None:
        maxlength = int(len(s) / readingframe)
    return tuple(lengthnhead(s, n=n, readingframe=readingframe)
                                for n in range(minlength, maxlength + 1)) + \
           tuple(lengthntail(s, n=n, readingframe=readingframe)
                                for n in range(minlength, maxlength + 1))
