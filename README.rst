========
richenum
========
.. image:: https://travis-ci.org/hearsaycorp/richenum.png
    :alt: Build Status
    :target: https://travis-ci.org/#!/hearsaycorp/richenum/

.. image:: https://img.shields.io/pypi/v/richenum.svg
    :alt: Latest PyPI Version
    :target: https://pypi.python.org/pypi/richenum/

=====
About
=====
A enum library for Python.

enum
  A simple enum implementation that maps a "variable" to a constant.
RichEnum
  An enum implementation that offers more functionality than a basic enum, hence the
  name: RichEnum. Provided functionality include specifying a canonical name and a display name.
  The canonical name should be used if you need to do a lookup or reference in your code.
  The display name should be used if you need to display text to a user.
OrderedRichEnum
  Exactly like RichEnum but also has an index specified for each enum value. Also, iteration over
  an OrderedRichEnum will be sorted (ascending) by the enum value's index.

-----
Links
-----
| `GitHub <https://github.com/hearsaycorp/richenum>`_
| `PyPi <https://pypi.python.org/pypi/richenum/>`_
| `Blog post about the motivation behind RichEnum <http://engineering.hearsaysocial.com/2013/09/16/enums-in-python/>`_

============
Installation
============
.. code:: bash

    $ pip install richenum

=====
Example Usage
=====
----
enum
----
.. code:: python

    >>> from richenum import enum
    >>> MY_ENUM = enum(FOO=1, BAR=2)
    >>> MY_ENUM.FOO
    1
    >>> MY_ENUM.BAR
    2

--------
RichEnum
--------
.. code:: python

    >>> from richenum import RichEnum, RichEnumValue
    >>> class MyRichEnum(RichEnum):
    ...    FOO = RichEnumValue(canonical_name="foo", display_name="Foo")
    ...    BAR = RichEnumValue(canonical_name="bar", display_name="Bar")
    ...
    >>> MyRichEnum.FOO
    RichEnumValue - canonical_name: 'foo'  display_name: 'Foo'
    >>> MyRichEnum.from_canonical("foo")
    RichEnumValue - canonical_name: 'foo'  display_name: 'Foo'


---------------
OrderedRichEnum
---------------
.. code:: python

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


================
Related Packages
================

django-richenum
  Makes RichEnum and OrderedRichEnum available in as model fields and form fields in Django.

  | `GitHub <https://github.com/hearsaycorp/django-richenum>`_

  | `PyPi <https://pypi.python.org/pypi/django-richenum/>`_

enum
  Starting with Python 3.4, there is a standard library for enumerations.
  This class has a similar API, but is not directly compatible with that
  class.


============
Contributing
============

#. Fork the repo from `GitHub <https://github.com/hearsaycorp/richenum>`_.
#. Make your changes.
#. Add unittests for your changes.
#. Run `pep8 <https://pypi.python.org/pypi/pep8>`_, `pyflakes <https://pypi.python.org/pypi/pyflakes>`_, and `pylint <https://pypi.python.org/pypi/pyflakes>`_ to make sure your changes follow the Python style guide and doesn't have any errors.
#. Add yourself to the AUTHORS file (in alphabetical order).
#. Send a pull request from your fork to the main repo.
