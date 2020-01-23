import unittest
from agl.strfuncs import lengthnanchors, lengthnhead, lengthntail, \
    lengthnsubstrings


class TestLengthNSubstrings(unittest.TestCase):

    def test_default(self):
        self.assertTupleEqual(lengthnsubstrings('abcd', n=1),
                              ('a', 'b', 'c', 'd'))
        self.assertTupleEqual(lengthnsubstrings('abcd', n=2),
                              ('ab', 'bc', 'cd'))
        self.assertTupleEqual(lengthnsubstrings('abcd', n=3),
                              ('abc', 'bcd'))
        self.assertTupleEqual(lengthnsubstrings('abcd', n=4),
                              ('abcd',))
        self.assertTupleEqual(lengthnsubstrings('abcd', n=5),
                              ())

    def test_readingframe(self):
        self.assertTupleEqual(lengthnsubstrings('abcdefgh', n=2,
                                                readingframe=2),
                              ('abcd', 'cdef', 'efgh'))


class TestLengthNHead(unittest.TestCase):

    def test_default(self):
        self.assertEqual(lengthnhead('abcd', n=1), 'a')
        self.assertEqual(lengthnhead('abcd', n=2), 'ab')
        self.assertEqual(lengthnhead('abcd', n=4), 'abcd')

    def test_readingframe(self):
        self.assertEqual(lengthnhead('abcd', n=1, readingframe=1), 'a')
        self.assertEqual(lengthnhead('abcd', n=1, readingframe=2), 'ab')
        self.assertEqual(lengthnhead('abcd', n=2, readingframe=2), 'abcd')
        self.assertEqual(lengthnhead('abcdef', n=2, readingframe=2), 'abcd')


class TestLengthNTail(unittest.TestCase):

    def test_default(self):
        self.assertEqual(lengthntail('abcd', n=1), 'd')
        self.assertEqual(lengthntail('abcd', n=2), 'cd')
        self.assertEqual(lengthntail('abcd', n=4), 'abcd')

    def test_readingframe(self):
        self.assertEqual(lengthntail('abcd', n=1, readingframe=1), 'd')
        self.assertEqual(lengthntail('abcd', n=1, readingframe=2), 'cd')
        self.assertEqual(lengthntail('abcd', n=2, readingframe=2), 'abcd')
        self.assertEqual(lengthntail('abcdef', n=2, readingframe=2), 'cdef')


class TestLengthNAnchors(unittest.TestCase):

    def test_default(self):
        self.assertTupleEqual(lengthnanchors('abcd', n=1), ('a', 'd'))
        self.assertTupleEqual(lengthnanchors('abcd', n=2), ('ab', 'cd'))
        self.assertTupleEqual(lengthnanchors('abcd', n=3), ('abc', 'bcd'))
        self.assertTupleEqual(lengthnanchors('abcd', n=4), ('abcd', 'abcd'))

    def test_readingframe(self):
        self.assertTupleEqual(lengthnanchors('abcd', n=1, readingframe=1),
                              ('a', 'd'))
        self.assertTupleEqual(lengthnanchors('abcd', n=1, readingframe=2),
                              ('ab', 'cd'))
        self.assertTupleEqual(lengthnanchors('abcdef', n=2, readingframe=2),
                              ('abcd', 'cdef'))







