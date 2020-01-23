from . import strfuncs
from . import strcomp
from . import strsetcomp
from . import htmltables
from . import PARSER

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .tests import test