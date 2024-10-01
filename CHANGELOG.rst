=========
Changelog
=========
------------------
2.0.2 (2024-10-01)
------------------
    - Remove unavailable link for blog post from README.rst

------------------
2.0.1 (2024-06-06)
------------------
    - Fix README.rst

------------------
2.0.0 (2024-06-04)
------------------
    - Remove six
    - Remove python 3.7 support
    - Add python 3.9 and 3.10 support
    - Remove tox.ini

------------------
1.2.1 (2016-09-16)
------------------
    - ``EnumLookupError`` class now inherits from built-in ``LookupError``.

------------------
1.2.0 (2016-04-15)
------------------
    - added simple ``LookupError`` members that are thrown when
      ``RichEnum.lookup`` is called for a nonexistent attr/val pair.
      Users can choose to catch either the specific ``LookupError`` or
      continue to catch ``EnumLookupError``.

------------------
1.1.0 (2014-04-17)
------------------
    - support for Python 3 and PyPy

------------------
1.0.4 (2013-12-03)
------------------
    - Better unicode handling in ``__str__``, ``__unicode__``, and
      ``__repr__`` magic methods.

------------------
1.0.3 (2013-12-03)
------------------
    - Stop throwing warnings.

------------------
1.0.2 (2013-11-05)
------------------
    - Suppress warnings from mismatched type comparisons when generated
      in RichEnum.lookup.

------------------
1.0.1 (2013-09-20)
------------------
    - Raise warnings when comparing enum values to other types, but not
      when checking membership or comparing to None.

------------------
1.0.0 (2013-08-16)
------------------
    - Initial public release.
