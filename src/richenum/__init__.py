from .enums import enum, EnumConstructionException, RichEnumValue, OrderedRichEnumValue, OrderedRichEnum, RichEnum, EnumLookupError


__all__ = [
    'enum',
    'EnumConstructionException',
    'RichEnumValue',
    'OrderedRichEnumValue',
    'OrderedRichEnum',
    'RichEnum',
    'EnumLookupError',
]


try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('richenum').version
except Exception as e:
    VERSION = 'unknown'
