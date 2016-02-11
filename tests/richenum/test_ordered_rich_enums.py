# -*- coding: utf-8 -*-

# pylint: disable=E1101

import copy
from six import PY3
try:
    import unittest2 as unittest
except ImportError:
    import unittest
if PY3:
    unicode = str  # for flake8, mainly

from richenum import EnumConstructionException  # noqa
from richenum import EnumLookupError  # noqa
from richenum import OrderedRichEnum  # noqa
from richenum import OrderedRichEnumValue  # noqa
from richenum import RichEnumValue  # noqa


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
        self.assertEqual(Breakfast.from_index(0), coffee)
        # Should work if enum isn't zero-indexed.
        self.assertEqual(SadBreakfast.from_index(1), oatmeal)

        with self.assertRaises(EnumLookupError):
            SadBreakfast.from_index(7)

    def test_construction_preserves_indices(self):
        self.assertEqual(SadBreakfast.OATMEAL.index, 1)
        self.assertEqual(Breakfast.OATMEAL.index, 1)

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

    def test_less_than_other_types(self):
        # RichEnumValues are always < values of other types
        self.assertLess(Breakfast.COFFEE, Breakfast.COFFEE.canonical_name)
        self.assertLess(Breakfast.COFFEE, Breakfast.COFFEE.index)
        self.assertLess(Breakfast.COFFEE, {'foo': 'bar'})

        # ...even if the other type is also descended from OrderedRichEnumValue
        other_coffee = OrderedRichEnumValue(0, 'coffee', 'Coffee')
        self.assertLess(Breakfast.COFFEE, other_coffee)

    def test_not_equal_to_other_types(self):
        self.assertNotEqual(Breakfast.COFFEE, None)
        # RichEnumValues are always != values of other types
        self.assertNotEqual(Breakfast.COFFEE, Breakfast.COFFEE.canonical_name)
        self.assertNotEqual(Breakfast.COFFEE, Breakfast.COFFEE.index)
        self.assertNotEqual(Breakfast.COFFEE, {'foo': 'bar'})

        # ...even if the other type is also descended from OrderedRichEnumValue
        other_coffee = OrderedRichEnumValue(0, 'coffee', 'coffee')
        self.assertNotEqual(Breakfast.COFFEE, other_coffee)

    def test_compares_by_index(self):
        self.assertLess(Breakfast.COFFEE, Breakfast.OATMEAL)

    def test_equality_by_index_and_type(self):
        # Tests equality of canonical names, not identity
        coffee_copy = copy.deepcopy(Breakfast.COFFEE)
        self.assertFalse(coffee_copy is Breakfast.COFFEE)
        self.assertEqual(Breakfast.COFFEE, coffee_copy)

    def test_unicode_handling(self):
        poop_oatmeal = BreakfastEnumValue(3, u'oatmeal💩', u'Oatmeal💩')
        self.assertRegexpMatches(
            repr(poop_oatmeal),
            r"<BreakfastEnumValue #3: oatmeal..? \('Oatmeal..?'\)>",
        )
        self.assertEqual(str(poop_oatmeal), "Oatmeal💩")
        if not PY3:
            self.assertEqual(unicode(poop_oatmeal), u"Oatmeal💩")
