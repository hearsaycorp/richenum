# pylint: disable=E1101

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from richenum import enum
from richenum import EnumConstructionException


Breakfast = enum(
    COFFEE=0,
    OATMEAL=1,
    FRUIT=2)


class SimpleEnumTestSuite(unittest.TestCase):

    def test_members_are_accessible_through_attributes(self):
        self.assertEqual(Breakfast.COFFEE, 0)

    def test_lookup_by_name(self):
        self.assertEqual(Breakfast.get_id_by_label('COFFEE'), 0)

    def test_lookup_by_value(self):
        self.assertEqual(Breakfast.get_label_by_id(0), 'COFFEE')

    def test_can_cast_to_list_of_choices(self):
        self.assertEqual(
            Breakfast.choices,
            [(0, 'COFFEE'), (1, 'OATMEAL'), (2, 'FRUIT')])

    def test_choices_are_ordered_by_value(self):
        Shuffled = enum(FRUIT=2, COFFEE=0, OATMEAL=1)
        self.assertEqual(Shuffled.choices, Breakfast.choices)

    def test_values_can_be_any_hashable_type(self):
        try:
            Confused = enum(INT=0, TUPLE=(1, 2), STR='yup')
            self.assertEqual(Confused.get_id_by_label('TUPLE'), (1, 2))
        except:
            self.fail('Simple enums should accept values of any hashable type.')

        with self.assertRaisesRegexp(EnumConstructionException, 'hashable'):
            Confused = enum(LIST=[1, 2])
