Changelog
=========

1.0.3 (2013-11-27)
------------------
    -  Remove warning messages when making lookup() calls against members that are lists
    by checking to see if the member is an iterable first.

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
