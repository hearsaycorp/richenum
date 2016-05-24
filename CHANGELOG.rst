Changelog
=========

1.2.0 (2016-04-15)
------------------
    - added simple ``LookupError`` members that are thrown when
      ``RichEnum.lookup`` is called for a nonexistent attr/val pair.
      Users can choose to catch either the specific ``LookupError`` or
      continue to catch ``EnumLookupError``.

1.1.0 (2014-04-17)
------------------
    - support for Python 3 and PyPy

1.0.4 (2013-12-03)
------------------
    - Better unicode handling in ``__str__``, ``__unicode__``, and
      ``__repr__`` magic methods.

1.0.3 (2013-12-03)
------------------
    - Stop throwing warnings.

1.0.2 (2013-11-05)
------------------
    - Suppress warnings from mismatched type comparisons when generated
      in RichEnum.lookup.

1.0.1 (2013-09-20)
------------------
    - Raise warnings when comparing enum values to other types, but not
      when checking membership or comparing to None.

1.0.0 (2013-08-16)
------------------
    - Initial public release.
