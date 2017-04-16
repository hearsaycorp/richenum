import unittest

from . import OrderedRichEnum, OrderedRichEnumValue, RichEnum, RichEnumValue, EnumConstructionException
from .richenum import _OrderedRichEnumMetaclass


class RichEnumTestSuite(unittest.TestCase):

    def setUp(self):

        class TestEnumValue(RichEnumValue):
            def __init__(self, custom, *args):
                super(TestEnumValue, self).__init__(*args)
                self.custom = custom
        self.p1 = TestEnumValue('other1', 'test1', 'Test 1')
        self.p2 = TestEnumValue('other2', 'test2', 'Test 2')

        class TestRichEnum(RichEnum):
            TEST1 = self.p1
            TEST2 = self.p2

        self.rich_enum = TestRichEnum

    def test_len(self):
        # Check the length
        self.assertEqual(len(self.rich_enum), 2)

    def test_attr(self):
        # ensure the data is accessible via attributes
        self.assertEqual(self.rich_enum.TEST1, self.p1)
        self.assertEqual(self.rich_enum.TEST2, self.p2)

        with self.assertRaises(AttributeError):
            self.rich_enum.ATTR3

    def test_membership(self):
        self.assertTrue(self.p1 in self.rich_enum)
        self.assertFalse(RichEnumValue('test3', 'Test 3') in self.rich_enum)
        self.assertFalse('Test 3' in self.rich_enum)

    def test_iteration(self):
        # test iteration
        self.assertEqual([e for e in self.rich_enum], [self.p1, self.p2])

    def test_rich_enum_reverse_lookup(self):
        self.assertEqual(self.rich_enum.lookup("canonical_name", "test1"), self.p1)
        self.assertEqual(self.rich_enum.lookup("canonical_name", "test2"), self.p2)

    def test_choices(self):
        self.assertEqual(self.rich_enum.choices(), [('test1', 'Test 1'), ('test2', 'Test 2')])
        self.assertEqual(self.rich_enum.choices(value_field='custom', display_field='canonical_name'),
                         [('other1', 'test1'), ('other2', 'test2')])


class OrderedRichEnumTestSuite(unittest.TestCase):
    class IntRichEnumValue(OrderedRichEnumValue):
        def __init__(self, index, value):
            self.value = value
            super(OrderedRichEnumTestSuite.IntRichEnumValue, self).__init__(index, "name", "Name")

    def custom_setup(self, zero_indexed=True, kwargs=None):
        """
        Can be called again at the start of a test to override the arguments passed in by the standard setUp() method
        """
        if kwargs is None:
            kwargs = {}

        self.start_index = 0
        if not zero_indexed:
            self.start_index = 1

        self.p1 = OrderedRichEnumTestSuite.IntRichEnumValue(self.start_index, "v1")
        self.p2 = OrderedRichEnumTestSuite.IntRichEnumValue(self.start_index + 1, "v2")
        self.assertNotIn("ATTR1", kwargs)
        self.assertNotIn("ATTR2", kwargs)

        kwargs["ATTR1"] = self.p1
        kwargs["ATTR2"] = self.p2

        self.rich_enum = _OrderedRichEnumMetaclass("TestRichEnum", (OrderedRichEnum, ), kwargs)

    def setUp(self):
        self.custom_setup()

    def _test_index(self, zero_indexed):
        self.custom_setup(zero_indexed)
        # ensure the data is accessible via indices
        self.assertEqual(self.rich_enum[self.start_index], self.p1)
        self.assertEqual(self.rich_enum[self.start_index + 1], self.p2)
        self.assertEqual(self.rich_enum[-1], self.p2)

        # ensure that non-existent indices raise an exception
        with self.assertRaises(IndexError):
            self.rich_enum[self.start_index + 2]

    def test_index(self):
        self._test_index(True)
        self._test_index(False)

    def _test_slice(self, zero_indexed):
        self.custom_setup(zero_indexed)
        # ensure the data is accessible via slices
        self.assertEqual(self.rich_enum[self.start_index:self.start_index + 2], (self.p1, self.p2))
        self.assertEqual(self.rich_enum[:], (self.p1, self.p2))
        self.assertEqual(self.rich_enum[::2], (self.p1,))
        # Note: slices won't raise any errors

    def test_slice(self):
        self._test_slice(True)
        self._test_slice(False)

    #######################################################################
    # Tests that don't need custom_setup()
    #######################################################################

    def _test_rich_enum_value_indices(self, start_index):
        p1 = OrderedRichEnumTestSuite.IntRichEnumValue(start_index, "v1")
        p2 = OrderedRichEnumTestSuite.IntRichEnumValue(start_index + 1, "v2")

        class TestRichEnum(OrderedRichEnum):
            ATTR1 = p1
            ATTR2 = p2

        # Ensure that the RichEnumValue index was not changed
        self.assertEquals(p1.index, start_index)
        self.assertEquals(p2.index, start_index + 1)

    def test_rich_enum_value_indices(self):
        self._test_rich_enum_value_indices(1)
        self._test_rich_enum_value_indices(1000)

    def test_rich_enum_value_invalid_indices(self):
       # Test negative index
        self.assertRaisesRegexp(EnumConstructionException, "Index cannot be a negative number", OrderedRichEnumTestSuite.IntRichEnumValue, -1, "v1")

        # Test missing indices
        with self.assertRaisesRegexp(EnumConstructionException, "Expected indices to be sequential starting from: 1. Missing indices: set\(\[2\]\). Extra indices: set\(\[3\]\)"):
            class TestRichEnum(OrderedRichEnum):
                ATTR1 = OrderedRichEnumTestSuite.IntRichEnumValue(1, "v1")
                ATTR2 = OrderedRichEnumTestSuite.IntRichEnumValue(3, "v2")
