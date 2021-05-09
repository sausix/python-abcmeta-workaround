# -*- coding: utf-8 -*-

"""
Recreate ABC (abstract base classes) in Python compatible with QObject derivates.

See test.py for usage.

Author: Adrian Sausenthaler (sausix)
"""


class FakeABC:  # Don't derive from '<class type>'!
    def __init__(self):
        if not hasattr(self, "__abstractmethods__"):
            # Some is using abstract base classes without abstracting at least one methods with '@abstractmethod'
            # Ok. I'm fine with that.
            return

        # Check if we have implemented all of them
        abstracts = getattr(self, "__abstractmethods__")  # type: set[str]

        missing_methods = tuple(methodname for methodname in abstracts
                                if hasattr(self, methodname) and
                                not callable(getattr(self, methodname))
                                or hasattr(getattr(self, methodname), "__isabstractmethod__")
                                )

        if missing_methods:
            raise TypeError("Can't instantiate abstract class {} without having all abtract methods "
                            "implemented: {}".format(self.__class__.__name__, ", ".join(missing_methods)))

    def __init_subclass__(cls, *args, **kwargs):
        # Collect new abc methods if defined in a subclass of myself
        new_abstractmethods = set(key for key, value
                                  in cls.__dict__.items()
                                  if callable(value)
                                  and hasattr(value, "__isabstractmethod__"))

        if hasattr(cls.__base__, "__abstractmethods__"):
            # A base has already abc methods defined. Merge old and new names.
            base_abstractmethods = getattr(cls.__base__, "__abstractmethods__")  # type: set[str]
            new_abstractmethods.update(base_abstractmethods)

        if new_abstractmethods:
            # Derive to local copy of merged set of abc method names
            cls.__abstractmethods__ = new_abstractmethods
