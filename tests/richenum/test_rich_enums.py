# -*- coding: utf-8 -*-
import copy
import unittest2 as unittest

from richenum import EnumConstructionException
from richenum import EnumLookupError
from richenum import RichEnum
from richenum import RichEnumValue


class VegetableEnumValue(RichEnumValue):
    def __init__(self, flavor, *args):  # pylint: disable=E1002
        super(VegetableEnumValue, self).__init__(*args)
        self.flavor = flavor


okra = VegetableEnumValue('gross', 'okra', 'Okra')
broccoli = VegetableEnumValue('delicious', 'broccoli', 'Broccoli')


class Vegetable(RichEnum):
    OKRA = okra
    BROCCOLI = broccoli


class RichEnumTestSuite(unittest.TestCase):

    def test_length_is_num_members(self):
        self.assertEqual(len(Vegetable), 2)

    def test_members_are_accessible_through_attributes(self):
        self.assertEqual(Vegetable.OKRA, okra)
        self.assertEqual(Vegetable.BROCCOLI, broccoli)

        with self.assertRaises(AttributeError):
            Vegetable.PARSNIP  # pylint: disable=E1101

    def test_membership(self):
        self.assertTrue(Vegetable.OKRA in Vegetable)

        # Doesn't work with canonical or display names.
        self.assertFalse('okra' in Vegetable)
        self.assertFalse('Okra' in Vegetable)

        parsnip = VegetableEnumValue('yum', 'parsnip', 'Parsnip')
        self.assertFalse(parsnip in Vegetable)

    def test_enums_iterate_through_members(self):
        members = tuple(e for e in Vegetable)
        self.assertEqual(members, (Vegetable.OKRA, Vegetable.BROCCOLI))

    def test_lookup_by_canonical_name(self):
        self.assertEqual(Vegetable.from_canonical('okra'), Vegetable.OKRA)  # pylint: disable=E1101
        with self.assertRaises(EnumLookupError):
            Vegetable.from_canonical('parsnip')  # pylint: disable=E1101

    def test_lookup_by_display_name(self):
        self.assertEqual(Vegetable.from_display('Okra'), Vegetable.OKRA)  # pylint: disable=E1101
        with self.assertRaises(EnumLookupError):
            Vegetable.from_display('Parsnip')  # pylint: disable=E1101

    def test_generic_lookup(self):
        self.assertEqual(Vegetable.lookup('canonical_name', 'okra'), Vegetable.OKRA)  # pylint: disable=E1101
        self.assertEqual(Vegetable.lookup('flavor', 'gross'), Vegetable.OKRA)  # pylint: disable=E1101
        with self.assertRaises(EnumLookupError):
            Vegetable.lookup('flavor', 'yum')  # pylint: disable=E1101

    def test_choices(self):
        self.assertEqual(
            Vegetable.choices(),  # pylint: disable=E1101
            [('okra', 'Okra'), ('broccoli', 'Broccoli')])
        self.assertEqual(
            Vegetable.choices(value_field='flavor', display_field='canonical_name'),  # pylint: disable=E1101
            [('gross', 'okra'), ('delicious', 'broccoli')])

    def test_public_members_must_be_enum_values(self):
        with self.assertRaisesRegexp(EnumConstructionException, 'Invalid attribute'):
            class Medley(RichEnum):
                OKRA = okra
                PARSNIP = 'parsnip'

    def test_public_members_must_be_same_concrete_type(self):
        with self.assertRaisesRegexp(EnumConstructionException, 'Differing member types'):
            class Medley(RichEnum):
                OKRA = okra
                PARSNIP = RichEnumValue('carrot', 'Carrot')

    def test_private_members_can_be_anything(self):
        try:
            class Medley(RichEnum):
                OKRA = okra
                # Should ignore underscore-prefixed attrs.
                _PARSNIP = 'parsnip'
                # Should also ignore lowercase attrs.
                parsnip = 'parsnip'
        except EnumConstructionException:
            self.fail('RichEnum should allow private attributes of any type.')

    def test_less_than_other_types(self):
        # RichEnumValues are always < values of other types
        self.assertLess(Vegetable.OKRA, Vegetable.OKRA.canonical_name)
        self.assertLess(Vegetable.OKRA, 11)
        self.assertLess(Vegetable.OKRA, {'foo': 'bar'})

        # ...even if the other type is also descended from RichEnumValue
        other_okra = RichEnumValue('okra', 'Okra')
        self.assertLess(Vegetable.OKRA, other_okra)

    def test_not_equal_to_other_types(self):
        self.assertNotEqual(Vegetable.OKRA, None)
        # RichEnumValues are always != values of other types
        self.assertNotEqual(Vegetable.OKRA, Vegetable.OKRA.canonical_name)
        self.assertNotEqual(Vegetable.OKRA, 11)
        self.assertNotEqual(Vegetable.OKRA, {'foo': 'bar'})

        # ...even if the other type is also descended from RichEnumValue
        other_okra = RichEnumValue('okra', 'Okra')
        self.assertNotEqual(Vegetable.OKRA, other_okra)

    def test_compares_by_canonical_name(self):
        # 'broccoli' < 'okra'
        self.assertLess(Vegetable.BROCCOLI, Vegetable.OKRA)

    def test_equality_by_canonical_name_and_type(self):
        # Tests equality of canonical names, not identity
        okra_copy = copy.deepcopy(Vegetable.OKRA)
        self.assertFalse(okra_copy is Vegetable.OKRA)
        self.assertEqual(Vegetable.OKRA, okra_copy)

    def test_unicode_handling(self):
        poop_okra = VegetableEnumValue('gross', 'okra💩', u'Okra💩')
        self.assertEqual(repr(poop_okra), "<VegetableEnumValue: okra? ('Okra?')>")
        self.assertEqual(str(poop_okra), "Okra💩")
        self.assertEqual(unicode(poop_okra), u"Okra💩")
