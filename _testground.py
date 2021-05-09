#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recreate ABC (abstract base classes) in Python compatible with QObject derivates.

This is my testground for testing and debugging.
See FakeABC.py for clean solution.

https://stackoverflow.com/questions/28720217/multiple-inheritance-metaclass-conflict
https://stackoverflow.com/questions/49384161/python-mixing-pyqt5-and-abc-abcmeta
https://bugreports.qt.io/browse/PYSIDE-1434

Author: Adrian Sausenthaler (sausix)
"""

from abc import abstractmethod  # Does hint PyCharm to missing abc implementations!
from PySide2.QtCore import QObject
# from PyQt5.QtCore import QObject


# qmeta = type(QObject)  # <class 'Shiboken.ObjectType'>


# print(dir(SolutionClass))  # ['__abstractmethods__', ...,  '_abc_impl']


class FakeABC:  # Don't derive from '<class type>'!
    """

    Does not get called because this class is not derived from "type"
    def __new__(cls, *args, **kwargs):
        print("__new__:", cls)
        return super().__new__(cls, *args, **kwargs)
    """

    def __init__(self):
        print("Checking ABC --------")
        print("mro:", self.__class__.__mro__)
        if hasattr(self, "__abstractmethods__"):
            abstracts = getattr(self, "__abstractmethods__")

            print("abstracts:")
            for absm in abstracts:
                attr_local = getattr(self, absm[0])

                if callable(attr_local) and hasattr(attr_local, "__isabstractmethod__"):
                    print("Missing:", absm[0])
                else:
                    print("Implemented ok:", absm[0])

        print("---------------------")

    def __init_subclass__(cls, *args, **kwargs):
        print("\n\n__init_subclass__:", cls.__name__, "\nBase:", cls.__base__)

        new_abstractmethods = tuple((key, value) for key, value in cls.__dict__.items() if callable(value) and hasattr(value, "__isabstractmethod__"))
        if new_abstractmethods:
            print("New abstract methods:")
            for absm in new_abstractmethods:
                print(absm)
            print("Setting _fakeabc_impl")
            setattr(cls, "_fakeabc_impl", True)

        if hasattr(cls.__base__, "__abstractmethods__"):
            base_abstractmethods = getattr(cls.__base__, "__abstractmethods__")
            print("Found base_abstractmethods:", base_abstractmethods)
            # will contain duplicates in this testing version. final version has a set of strings here.
            new_abstractmethods = base_abstractmethods + new_abstractmethods

        # Local copy of old and new abc methods
        cls.__abstractmethods__ = new_abstractmethods

        print("hasattr __abstractmethods__:", hasattr(cls, "__abstractmethods__"))
        print("hasattr _fakeabc_impl:", hasattr(cls, "_fakeabc_impl"))
        print("All abstractmetods: ")
        for absm in cls.__abstractmethods__:
            print(absm)


# class Module(QObject, metaclass=ABCMeta):
class Module(QObject, FakeABC):
    def __init__(self):
        print("init Module")
        QObject.__init__(self)

        # Explicit call required when deriving from two classes.
        # Check can only be done when FakeABC.__init__ gets called.
        FakeABC.__init__(self)

    @abstractmethod
    def abc_func1(self):
        pass

    @abstractmethod
    def abc_func2(self):
        pass

# print(dir(Module))  # ['__abstractmethods__', ...,  '_abc_impl', 'load']


class Module2(Module):
    @abstractmethod
    def abc_module2_func(self):
        # Add another abstract method
        pass

    @abstractmethod
    def abc_func1(self):
        # Redefining an abstractmethod
        pass


class TestModule(Module2):
    testmodule_classvar = 1

    def __init__(self):
        print("init TestModule")
        self.testmodule_instancevar = 1
        super().__init__()

    def abc_func1(self):
        # Define only one abstract method
        pass

# Not defining another abstract method:
#    def abc_func2(self):
#        pass
# -> TypeError: Can't instantiate abstract class TestModule with abstract method load


print("Instantiate...")

t = TestModule()

print("Instantiated")

print("Check isinstance...")
print("TestModule:", isinstance(t, TestModule))
print("Module2:", isinstance(t, Module2))
print("Module:", isinstance(t, Module))
print("FakeABC:", isinstance(t, FakeABC))

print("Check issubclass (upward: True)...")
print("TestModule, Module2:", issubclass(TestModule, Module2))
print("TestModule, Module:", issubclass(TestModule, Module))
print("TestModule, FakeABC:", issubclass(TestModule, FakeABC))
print("Module2, Module:", issubclass(Module2, Module))
print("Module2, FakeABC:", issubclass(Module2, FakeABC))
print("Module, FakeABC:", issubclass(Module, FakeABC))

print("Check issubclass (downward: False)...")
print("Module2, TestModule:", issubclass(Module2, TestModule))
print("Module, TestModule:", issubclass(Module, TestModule))
print("FakeABC, TestModule:", issubclass(FakeABC, TestModule))
print("Module, Module2:", issubclass(Module, Module2))
print("FakeABC, Module2:", issubclass(FakeABC, Module2))
print("FakeABC, Module:", issubclass(FakeABC, Module))
