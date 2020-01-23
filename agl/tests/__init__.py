from unittest import TestLoader, TextTestRunner, TestSuite

from . import test_PARSER, test_strfuncs

modules = [test_PARSER, test_strfuncs]

def test(verbosity=1):
    suite =TestSuite()
    for module in modules:
        suite.addTests(TestLoader().loadTestsFromModule(module))
    return TextTestRunner(verbosity=verbosity).run(suite)