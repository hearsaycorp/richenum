import collections
import copy
from functools import total_ordering
import logging
import numbers
from six import PY3
from six import string_types
from six import with_metaclass

from operator import itemgetter

if PY3:
    unicode = str  # workaround for flake8


logger = logging.getLogger(__name__)


class EnumConstructionException(Exception):
    """
    Raised whenever there's an error in an Enum's declaration.
    """
    pass


class EnumLookupError(Exception):
    """
    Raised when an enum cannot be found by the specified method of lookup.
    """
    pass


def _str_or_ascii_replace(stringy):
    if PY3:
        return stringy
    else:
        if isinstance(stringy, str):
            stringy = stringy.decode('utf-8')
        return stringy.encode('ascii', 'replace')


def _items(dict):
    try:
        return dict.iteritems()
    except AttributeError:
        return dict.items()


def _values(dict):
    try:
        return dict.itervalues()
    except AttributeError:
        return dict.values()


def enum(**enums):
    """
    A basic enum implementation.

    Usage:
        >>> MY_ENUM = enum(FOO=1, BAR=2)
        >>> MY_ENUM.FOO
        1
        >>> MY_ENUM.BAR
        2
    """
    # Enum values must be hashable to support reverse lookup.
    if not all(isinstance(val, collections.Hashable) for val in _values(enums)):
        raise EnumConstructionException('All enum values must be hashable.')

    # Cheating by maintaining a copy of original dict for iteration b/c iterators are hard.
    # It must be a deepcopy because new.classobj() modifies the original.
    en = copy.deepcopy(enums)
    e = type('Enum', (_EnumMethods,), dict((k, v) for k, v in _items(en)))

    try:
        e.choices = [(v, k) for k, v in sorted(_items(enums), key=itemgetter(1))]  # DEPRECATED
    except TypeError:
        pass
    e.get_id_by_label = e.__dict__.get
    e.get_label_by_id = dict((v, k) for (k, v) in _items(enums)).get

    return e


@total_ordering
class RichEnumValue(object):
    def __init__(self, canonical_name, display_name, *args, **kwargs):
        self.canonical_name = canonical_name
        self.display_name = display_name

    def __repr__(self):
        return "<%s: %s ('%s')>" % (
            self.__class__.__name__,
            _str_or_ascii_replace(self.canonical_name),
            _str_or_ascii_replace(self.display_name),
        )

    def __unicode__(self):
        return unicode(self.display_name)

    def __str__(self):
        return self.display_name if PY3 else unicode(self).encode(
            'utf-8', 'xmlcharrefreplace')

    def __hash__(self):
        return hash(self.canonical_name)

    def __lt__(self, other):
        if other is None:
            return -1
        if not isinstance(other, type(self)):
            return -1
        return self.canonical_name < other.canonical_name

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, type(self)):
            return False
        return self.canonical_name == other.canonical_name

    def __ne__(self, other):
        return not (self.__eq__(other))

    def choicify(self, value_field="canonical_name", display_field="display_name"):
        """
        DEPRECATED

        Returns a tuple that's compatible with Django's choices.
        https://docs.djangoproject.com/en/dev/ref/models/fields/#choices
        """
        return (getattr(self, value_field), getattr(self, display_field))


@total_ordering
class OrderedRichEnumValue(RichEnumValue):
    def __init__(self, index, canonical_name, display_name, *args, **kwargs):
        super(OrderedRichEnumValue, self).__init__(canonical_name, display_name, args, kwargs)
        if not isinstance(index, numbers.Integral):
            raise EnumConstructionException("Index must be an integer type, not: %s" % type(index))
        if index < 0:
            raise EnumConstructionException("Index cannot be a negative number")

        self.index = index

    def __repr__(self):
        return "<%s #%s: %s ('%s')>" % (
            self.__class__.__name__,
            self.index,
            _str_or_ascii_replace(self.canonical_name),
            _str_or_ascii_replace(self.display_name),
        )

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.index < other.index
        else:
            return True

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.index == other.index
        else:
            return False

    def __hash__(self):
        """
        __hash__ is not inherited from base class when __eq__
        is overridden
        """
        return hash(self.canonical_name + str(self.index))


def _setup_members(cls_attrs, cls_parents, member_cls):
        members = []

        # Find qualified "EnumValue" attributes.
        # Field names must be UPPERCASE, not prefixed with _ ("internal"),
        # and values must be EnumValue-derived.
        last_type = None
        for attr_key, attr_value in cls_attrs.items():
            # Skip "internal" attributes
            if attr_key.startswith("_"):
                continue

            if not attr_key.isupper():  # Implementation desiderata
                continue

            if isinstance(attr_value, member_cls):
                members.append(attr_value)
            else:
                raise EnumConstructionException("Invalid attribute: %s" % attr_key)

            attr_type = type(attr_value)
            if last_type and attr_type != last_type:
                raise EnumConstructionException("Differing member types: have seen %s,"
                                                " encountered %s" % (last_type, attr_type))
            else:
                last_type = attr_type

        if "__virtual__" not in cls_attrs and cls_parents not in [
                (object, ), (_EnumMethods, )
        ] and not members:
            raise EnumConstructionException(
                "Must specify at least one attribute when using RichEnum")

        return members


class _BaseRichEnumMetaclass(type):
    def __iter__(cls):
        for item in cls.members():
            yield item

    def __len__(cls):
        return len(cls.members())

    def __contains__(cls, item):
        # Check membership without comparing enum values to other types.
        members = cls.members()
        if not members:
            return False
        if not type(members[0]) == type(item):
            return False
        return (item in members)


class _RichEnumMetaclass(_BaseRichEnumMetaclass):
    def __new__(cls, cls_name, cls_parents, cls_attrs):
        members = _setup_members(cls_attrs, cls_parents, RichEnumValue)
        # Use tuple when possible when setting internal attributes to prevent modification
        cls_attrs['_MEMBERS'] = tuple(members)
        cls_attrs['LookupError'] = type('LookupError', (EnumLookupError,), {})
        return super(_RichEnumMetaclass, cls).__new__(cls, cls_name, cls_parents, cls_attrs)


class _OrderedRichEnumMetaclass(_BaseRichEnumMetaclass):
    def __new__(cls, cls_name, cls_parents, cls_attrs):
        members = _setup_members(cls_attrs, cls_parents, OrderedRichEnumValue)
        members.sort(key=lambda x: x.index)

        # Use tuple when possible when setting internal attributes to prevent modification
        cls_attrs['_MEMBERS'] = tuple(members)
        cls_attrs['LookupError'] = type('LookupError', (EnumLookupError,), {})

        # we want to validate that there are not two items at the same index, so lets do that here
        seen = set()
        for member in members:
            if member.index in seen:
                raise EnumConstructionException("Index already defined: %s." % (member.index))
            seen.add(member.index)

        return super(_OrderedRichEnumMetaclass, cls).__new__(cls, cls_name, cls_parents, cls_attrs)

    ############################################################################
    # Overwriting built-ins
    ############################################################################

    def get(self, key, default=None):
        return getattr(self, key, default)


class _EnumMethods(object):
    @classmethod
    def members(cls):
        return cls._MEMBERS  # pylint: disable=E1101

    @classmethod
    def lookup(cls, field, value):
        for member in cls:  # pylint: disable=E1133
            member_value = getattr(member, field)

            if member_value == value:
                return member

            if (
                not isinstance(member_value, string_types) and
                isinstance(member_value, collections.Iterable) and
                value in member_value
            ):
                return member
        raise cls.LookupError('Could not find member matching %s = %s in enum %s'  # pylint: disable=no-member
                              % (field, value, cls)
                              )

    @classmethod
    def from_canonical(cls, canonical_name):
        return cls.lookup('canonical_name', canonical_name)  # pylint: disable=E1101

    @classmethod
    def from_display(cls, display_name):
        return cls.lookup('display_name', display_name)  # pylint: disable=E1101

    @classmethod
    def choices(cls, value_field='canonical_name', display_field='display_name'):
        """
        DEPRECATED

        Returns a list of 2-tuples to be used as an argument to Django Field.choices

        Implementation note: choices() can't be a property
        See:
            http://www.no-ack.org/2011/03/strange-behavior-with-properties-on.html
            http://utcc.utoronto.ca/~cks/space/blog/python/UsingMetaclass03
        """
        return [m.choicify(value_field=value_field, display_field=display_field) for m in cls.members()]


class RichEnum(with_metaclass(_RichEnumMetaclass, _EnumMethods)):
    """
    Enumeration that can represent a name for referencing (canonical_name) and
    a name for displaying (display_name).

    Usage:

        >>> class MyRichEnum(RichEnum):
        ...    FOO = RichEnumValue(canonical_name="foo", display_name="Foo")
        ...    BAR = RichEnumValue(canonical_name="bar", display_name="Bar")
        ...
        >>> MyRichEnum.FOO
        RichEnumValue - canonical_name: 'foo'  display_name: 'Foo'
        >>> MyRichEnum.from_canonical("foo")
        RichEnumValue - canonical_name: 'foo'  display_name: 'Foo'

    Notes:
        1) display_name can be a string that's marked for translation.
           We recommend that display name be a lazily translated string for
           RichEnums in constants files.
        2) Subclassing RichEnumValue is nice, that way when the RichEnumValue
           is logged/printed, it'll show your custom RichEnumValue and it'll be
           easier to differentiate between all of your different RichEnums.

   """
    __virtual__ = True


class OrderedRichEnum(with_metaclass(_OrderedRichEnumMetaclass, _EnumMethods)):
    """
    Use OrderedRichEnum when you need a RichEnum with index-based
    access into the enum, e.g. OrderedRichEnumExample.from_index(0),
    and iteration over the enums sorted by index.

    If you don't need index-based access or sorted entries, please use regular RichEnum
    instead. It's more explicit.

    Usage:

        >>> class MyOrderedRichEnum(OrderedRichEnum):
        ...    FOO = OrderedRichEnumValue(index=1, canonical_name="foo", display_name="Foo")
        ...    BAR = OrderedRichEnumValue(index=2, canonical_name="bar", display_name="Bar")
        ...
        >>> MyOrderedRichEnum.FOO
        OrderedRichEnumValue - idx: 1  canonical_name: 'foo'  display_name: 'Foo'
        >>> MyOrderedRichEnum.from_canonical("foo")
        OrderedRichEnumValue - idx: 1  canonical_name: 'foo'  display_name: 'Foo'
        >>> MyOrderedRichEnum.from_index(1)
        OrderedRichEnumValue - idx: 1  canonical_name: 'foo'  display_name: 'Foo'
    """
    __virtual__ = True

    @classmethod
    def from_index(cls, index):
        return cls.lookup('index', index)  # pylint: disable=E1101
