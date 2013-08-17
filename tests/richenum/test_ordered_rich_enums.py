import unittest2 as unittest

from richenum import EnumConstructionException
from richenum import EnumLookupError
from richenum import OrderedRichEnum
from richenum import OrderedRichEnumValue
from richenum import RichEnumValue


class BreakfastEnumValue(OrderedRichEnumValue):
    pass


coffee = BreakfastEnumValue(0, 'coffee', 'Coffee')
oatmeal = BreakfastEnumValue(1, 'oatmeal', 'Oatmeal')
fruit = BreakfastEnumValue(2, 'fruit', 'Fruit')


class Breakfast(OrderedRichEnum):
    COFFEE = coffee
    # Deliberately not ordered by index.
    FRUIT = fruit
    OATMEAL = oatmeal


class SadBreakfast(OrderedRichEnum):
    OATMEAL = oatmeal


class OrderedRichEnumTestSuite(unittest.TestCase):

    def test_lookup_by_index(self):
        self.assertEqual(Breakfast.from_index(0), coffee)  # pylint: disable=E1101
        # Should work if enum isn't zero-indexed.
        self.assertEqual(SadBreakfast.from_index(1), oatmeal)  # pylint: disable=E1101

        with self.assertRaises(EnumLookupError):
            SadBreakfast.from_index(7)  # pylint: disable=E1101

    def test_construction_preserves_indices(self):
        self.assertEqual(SadBreakfast.OATMEAL.index, 1)  # pylint: disable=E1101
        self.assertEqual(Breakfast.OATMEAL.index, 1)  # pylint: disable=E1101

    def test_cannot_have_duplicate_indices(self):
        with self.assertRaisesRegexp(EnumConstructionException, 'Index already defined'):
            class DuplicateBreakast(OrderedRichEnum):
                COFFEE = coffee
                TEA = BreakfastEnumValue(0, 'tea', 'Tea')

    def test_cannot_have_negative_indices(self):
        msg = 'Index cannot be a negative number'
        with self.assertRaisesRegexp(EnumConstructionException, msg):
            class NegativeBreakfast(OrderedRichEnum):
                BACON = BreakfastEnumValue(-1, 'bacon', 'Bacon')

    def test_members_are_sorted_by_index(self):
        self.assertEqual(
            tuple(e for e in Breakfast),
            (coffee, oatmeal, fruit))

    def test_membership(self):
        self.assertTrue(Breakfast.COFFEE in Breakfast)
        self.assertTrue(coffee in Breakfast)
        self.assertFalse('coffee' in Breakfast)
        self.assertFalse('Coffee' in Breakfast)
        self.assertFalse(0 in Breakfast)

    def test_public_members_must_be_ordered(self):
        # Can't mix OrderedRichEnumValues and RichEnumValues.
        with self.assertRaisesRegexp(EnumConstructionException, 'Invalid attribute'):
            class MixedBreakfast(OrderedRichEnum):
                COFFEE = coffee
                TEA = RichEnumValue('tea', 'Tea')
