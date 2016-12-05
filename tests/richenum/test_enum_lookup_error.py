try:
    import unittest2 as unittest
except ImportError:
    import unittest

from richenum import EnumLookupError  # noqa


class EnumLookupErrorTestSuite(unittest.TestCase):
    def test_enumlookuperror_is_lookuperror(self):
        self.assertTrue(issubclass(EnumLookupError, LookupError))
