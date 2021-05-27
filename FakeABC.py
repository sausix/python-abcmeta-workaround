# -*- coding: utf-8 -*-

"""
Recreate ABC (abstract base classes) in Python compatible with QObject derivates.

See test.py for usage.

Author: Adrian Sausenthaler (sausix)

Version 2:
 - Now supports abstract staticmethods, classmethods and properties
"""


class FakeABC:  # Don't derive from '<class type>'!
    def __init__(self):
        if not hasattr(self, "__abstractmethods__"):
            # Someone is using abstract base classes without abstracting at least one method with '@abstractmethod'
            # Ok. I'm fine with that.
            return

        # Check if we have implemented all of them
        abstract_attributes = getattr(self, "__abstractmethods__")  # type: set[str]

        # Check instance having all cumulatively collected abstract attributes overriden by it's base classes.
        #
        # if an attr of the instance still has an attribute "__isabstractmethod__"
        #   it's an unoverwritten abstract method, staticmethod or classmethod.
        #
        # Every Property always has an "__isabstractmethod__" attribute.
        #   Detail is in the content. True hints to an abstract property, False is an overridden, standard property.
        missing_attributes = set(attr for attr in abstract_attributes
                                 if hasattr(self, attr) and
                                 hasattr(getattr(self, attr), "__isabstractmethod__")
                                 or getattr(getattr(self.__class__, attr), "__isabstractmethod__", False)
                                 )

        if missing_attributes:
            raise TypeError("Can't instantiate class {} without having all abstract methods or attributes "
                            "implemented: {}".format(self.__class__.__name__, ", ".join(missing_attributes)))

    def __init_subclass__(cls, *args, **kwargs):
        # Collect new abstract attributes if defined in this subclass level
        new_abstract_attributes = set(attrname for attrname, attr
                                      in cls.__dict__.items()
                                      if hasattr(attr, "__isabstractmethod__"))

        if hasattr(cls.__base__, "__abstractmethods__"):
            # A base of this class has already abstract attributes defined. Merge old and new names.
            base_abstract_attributes = getattr(cls.__base__, "__abstractmethods__")  # type: set[str]
            new_abstract_attributes.update(base_abstract_attributes)

        if new_abstract_attributes:
            # Derive to local copy of merged set of abstract attribute names
            cls.__abstractmethods__ = new_abstract_attributes
