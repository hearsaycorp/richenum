# -*- coding: utf-8 -*-
# pylint: disable=E1101

import copy
import re
import unittest
import pytest
import six
if six.PY3:
    unicode = str  # for flake8, mainly

from richenum import EnumConstructionException  # noqa
from richenum import EnumLookupError  # noqa
from richenum import RichEnum  # noqa
from richenum import RichEnumValue  # noqa


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
            Vegetable.PARSNIP

    def test_membership(self):
        self.assertTrue(Vegetable.OKRA in Vegetable)

        # Doesn't work with canonical or display names.
        self.assertFalse('okra' in Vegetable)
        self.assertFalse('Okra' in Vegetable)

        parsnip = VegetableEnumValue('yum', 'parsnip', 'Parsnip')
        self.assertFalse(parsnip in Vegetable)

    def test_enums_iterate_through_members(self):
        members = set(e for e in Vegetable)
        self.assertEqual(members, set((Vegetable.OKRA, Vegetable.BROCCOLI)))

    def test_lookup_by_canonical_name(self):
        self.assertEqual(Vegetable.from_canonical('okra'), Vegetable.OKRA)
        with self.assertRaises(EnumLookupError):
            Vegetable.from_canonical('parsnip')

    def test_lookup_by_display_name(self):
        self.assertEqual(Vegetable.from_display('Okra'), Vegetable.OKRA)
        with self.assertRaises(EnumLookupError):
            Vegetable.from_display('Parsnip')

    def test_generic_lookup(self):
        self.assertEqual(Vegetable.lookup('canonical_name', 'okra'), Vegetable.OKRA)
        self.assertEqual(Vegetable.lookup('flavor', 'gross'), Vegetable.OKRA)
        with self.assertRaises(EnumLookupError):
            Vegetable.lookup('flavor', 'yum')

    def test_choices(self):
        self.assertEqual(
            set(x for x in Vegetable.choices()),
            set((('okra', 'Okra'), ('broccoli', 'Broccoli'))),
        )

        self.assertEqual(
            set(x for x in Vegetable.choices(value_field='flavor', display_field='canonical_name')),
            set((('gross', 'okra'), ('delicious', 'broccoli'))),
        )

    def test_public_members_must_be_enum_values(self):
        with pytest.raises(EnumConstructionException, match=r"Invalid attribute"):
            class Medley(RichEnum):
                OKRA = okra
                PARSNIP = 'parsnip'

    def test_public_members_must_be_same_concrete_type(self):
        with pytest.raises(EnumConstructionException, match=r"Differing member types"):
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
        poop_okra = VegetableEnumValue('gross', u'okra💩', u'Okra💩')
        exp = re.compile(r"<VegetableEnumValue: okra..? \('Okra..?'\)>")
        assert exp.search(repr(poop_okra)) is not None
        assert str(poop_okra) == "Okra💩"
        if not six.PY3:
            assert unicode(poop_okra) == u"Okra💩"

    def test_string_coercion(self):
        class DisplayProxy():
            def __init__(self, name):
                self.name = name
            
            def __str__(self):
                return self.name
        
        proxy_okra = VegetableEnumValue('gross', 'okra', DisplayProxy('okra'))
        assert '%s' % (proxy_okra) == 'okra'

    def test_specific_lookup_error_is_caught(self):
        with self.assertRaises(Vegetable.LookupError):
            Vegetable.lookup('canonical_name', 'meat')

    def test_other_specific_lookup_error_is_not_caught(self):
        class Meat(RichEnum):
            COW = RichEnumValue("cow", "Cow")

        with self.assertRaises(EnumLookupError) as cm:
            Vegetable.lookup('canonical_name', 'meat')

        self.assertNotIsInstance(cm.exception, Meat.LookupError)
