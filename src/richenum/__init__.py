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


__version__ = 'unknown'
try:
    __version__ = __import__('pkg_resources').get_distribution('richenum').version
except Exception as e:
    pass
