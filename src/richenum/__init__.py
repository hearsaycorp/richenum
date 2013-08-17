from .enums import enum
from .enums import EnumConstructionException
from .enums import EnumLookupError
from .enums import OrderedRichEnum
from .enums import OrderedRichEnumValue
from .enums import RichEnum
from .enums import RichEnumValue


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
