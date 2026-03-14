# richenum

![Build Status](https://github.com/hearsaycorp/richenum/actions/workflows/python-version-tests.yml/badge.svg)
[![Latest PyPI Version](https://img.shields.io/pypi/v/richenum.svg)](https://pypi.python.org/pypi/richenum/)
[![Python versions](https://img.shields.io/pypi/pyversions/richenum.svg)](https://pypi.org/project/richenum/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/richenum.svg)](https://pypi.org/project/richenum/)

## About

An enum library for Python.

- `enum`: A simple enum implementation that maps a variable to a constant.
- `RichEnum`: An enum implementation that offers more functionality than a basic enum, including a canonical name and a display name.
- `OrderedRichEnum`: Like `RichEnum`, but each enum value also has an index and iteration is sorted by index.

## Links

- [GitHub](https://github.com/hearsaycorp/richenum)
- [PyPI](https://pypi.python.org/pypi/richenum/)

## Installation

```bash
pip install richenum
```

## Example Usage

### enum

```python
>>> from richenum import enum
>>> MY_ENUM = enum(FOO=1, BAR=2)
>>> MY_ENUM.FOO
1
>>> MY_ENUM.BAR
2
```

### RichEnum

```python
>>> from richenum import RichEnum, RichEnumValue
>>> class MyRichEnum(RichEnum):
...    FOO = RichEnumValue(canonical_name="foo", display_name="Foo")
...    BAR = RichEnumValue(canonical_name="bar", display_name="Bar")
...
>>> MyRichEnum.FOO
RichEnumValue - canonical_name: 'foo'  display_name: 'Foo'
>>> MyRichEnum.from_canonical("foo")
RichEnumValue - canonical_name: 'foo'  display_name: 'Foo'
```

### OrderedRichEnum

```python
>>> from richenum import OrderedRichEnum, OrderedRichEnumValue
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
```

## Related Packages

- `django-richenum`: Makes `RichEnum` and `OrderedRichEnum` available as model and form fields in Django.
  [GitHub](https://github.com/hearsaycorp/django-richenum), [PyPI](https://pypi.python.org/pypi/django-richenum/)
- `enum`: Starting with Python 3.4, there is a standard library for enumerations. This package has a similar API but is not directly compatible.

## Contributing

1. Fork the repo from [GitHub](https://github.com/hearsaycorp/richenum).
2. Make your changes.
3. Add unittests for your changes.
4. Run [pep8](https://pypi.python.org/pypi/pep8), [pyflakes](https://pypi.python.org/pypi/pyflakes), and [pylint](https://pypi.python.org/pypi/pylint) to make sure your changes follow the Python style guide and do not have any errors.
5. Add yourself to the AUTHORS file (in alphabetical order).
6. Send a pull request from your fork to the main repo.
