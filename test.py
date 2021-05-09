#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from FakeABC import FakeABC
from PySide2.QtCore import QObject
from abc import abstractmethod  # Does hint PyCharm to missing abc implementations!


class HighestBaseClass(QObject, FakeABC):
    """My primary class providing some abc methods"""

    def __init__(self):
        QObject.__init__(self)

        # Explicit call required when deriving from two classes.
        # Check can only be done when FakeABC.__init__ gets called.
        FakeABC.__init__(self)

    @abstractmethod
    def abc_func1(self):
        """Defining an abstract method"""

    @abstractmethod
    def abc_func2(self):
        """Defining another abstract method"""


class LowerBaseClass(HighestBaseClass):
    """Secondary base class adding some more abc methods and overwriting an existing one"""
    @abstractmethod
    def abc_lower_base_class_func(self):
        """Defining a third abstract method"""

    @abstractmethod
    def abc_func1(self):
        """Redefining an abstractmethod"""


class MyModule(LowerBaseClass):
    """Creating the final class which depends on all abc methods"""

    def __init__(self):
        print("init MyModule")
        super().__init__()  # Call to base class is mandatory

    def abc_func1(self):
        """Implementing only one abstract method"""

# Not defining other abstract methods will throw an exception on instantiation.
# Uncomment them for testing.
#    def abc_lower_base_class_func(self):
#        pass

#    def abc_func2(self):
#        pass

print("Testing instantiation...")
instance = MyModule()
print("Done (without exception).")

print("\nCheck isinstance...")
print("MyModule:", isinstance(instance, MyModule))
print("LowerBaseClass:", isinstance(instance, LowerBaseClass))
print("HighestBaseClass:", isinstance(instance, HighestBaseClass))
print("FakeABC:", isinstance(instance, FakeABC))

print("\nCheck issubclass (upward: True)...")
print("MyModule, LowerBaseClass:", issubclass(MyModule, LowerBaseClass))
print("MyModule, HighestBaseClass:", issubclass(MyModule, HighestBaseClass))
print("MyModule, FakeABC:", issubclass(MyModule, FakeABC))
print("LowerBaseClass, HighestBaseClass:", issubclass(LowerBaseClass, HighestBaseClass))
print("LowerBaseClass, FakeABC:", issubclass(LowerBaseClass, FakeABC))
print("HighestBaseClass, FakeABC:", issubclass(HighestBaseClass, FakeABC))

print("\nCheck issubclass (downward: False)...")
print("LowerBaseClass, MyModule:", issubclass(LowerBaseClass, MyModule))
print("HighestBaseClass, MyModule:", issubclass(HighestBaseClass, MyModule))
print("FakeABC, MyModule:", issubclass(FakeABC, MyModule))
print("HighestBaseClass, LowerBaseClass:", issubclass(HighestBaseClass, LowerBaseClass))
print("FakeABC, LowerBaseClass:", issubclass(FakeABC, LowerBaseClass))
print("FakeABC, HighestBaseClass:", issubclass(FakeABC, HighestBaseClass))
