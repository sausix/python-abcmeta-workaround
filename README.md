# python-abcmeta-workaround

Recreated ABC (abstract base classes) in Python for compatibility with QObject and derivates of PySide2.

This is a wonky workaround. Not a perfect solution.

Author: Adrian Sausenthaler (sausix)


**New version**: Now supporting abstract staticmethods, classmethods and properties


### Abstract base classes?

In short: They define rules for classes.

```python
from abc import ABCMeta, abstractmethod


class MyABC(metaclass=ABCMeta):
    @abstractmethod
    def must_have(self):
        """
        This is an abstract method which must be implemented by all deriving classes
        """


class MyClass(MyABC):
    """A class which does not implement all abstract methods of it's abstract base class"""
# Commented out:
#    def must_have(self):
#        pass


m = MyABC()
```


Not implementing one of these methods results in an error:
```
Traceback (most recent call last):
  File "...simple_abc.py", line 18, in <module>
    m = MyABC()
TypeError: Can't instantiate abstract class MyABC with abstract method must_have
```


### The Qt problem
Spent many hours of investigation and I'm not sure why there's no way to use that with QObject derivates from Qt (PySide) 

```python
from abc import ABCMeta, abstractmethod
from PySide2.QtCore import QObject


class MyABC(QObject, metaclass=ABCMeta):
    def __init__(self):
        QObject.__init__(self)  # or super()

    @abstractmethod
    def must_have(self):
        """
        This is an abstract method which must be implemented by all deriving classes
        """


class MyClass(MyABC):
    """A class which has implemented all required methods"""
    def must_have(self):
        """I'm here!"""


m = MyABC()
```

It's typical metaclass conflict as decribed [here](http://www.phyast.pitt.edu/~micheles/python/metatype.html).

```
Traceback (most recent call last):
  File "...qtmeta.py", line 5, in <module>
    class MyABC(QObject, metaclass=ABCMeta):
TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases
```

There's an open bug report and a ["solution"](https://bugreports.qt.io/browse/PYSIDE-1434).

BUT... It also eliminates the main feature of the `abc` module. Missing methods don't throw an error. And we definately want these errors!


### The solution

Little bit wonky but works.

Difference:  
Throws the `TypeError` during instantiation and not while reading a class definition, which is not another ABCMeta and has unimplemented abc methods.


Add `FakeABC` class from [FakeABC.py](FakeABC.py) as an base to make your class an abstract base class together with `QObject`.

```python
from FakeABC import FakeABC
from PySide2.QtCore import QObject
from abc import abstractmethod  # ABCMeta and ABC are useless


class MyQtBaseClass(QObject, FakeABC):
    """Primary class providing some abc methods"""

    def __init__(self):
        # Single super() call may not catch all inits of base classes.
        QObject.__init__(self)
        # Calling FakeABC.__init__ is important!
        FakeABC.__init__(self)

    @abstractmethod
    def abc_func1(self):
        """Defining an abstract method"""

        
class MyClass(MyQtBaseClass):
    """A class which may have implemented all required methods"""
    def abc_func1(self):
        """I'm here!"""


m = MyClass()  # Throws an error here if abc methods are missing:
```

```
TypeError: Can't instantiate abstract class MyClass without having all abtract methods implemented: abc_func1
```

Also supports adding further abc methods in subclasses.

See [test.py](test.py) for full example and instance and subclass tests.

Did test it on Linux with `PySide2==5.15.2` only. May behave different in other combinations.


### Better solution?

If there's a better way, let me know!


### PyQt5

Oh boy. There's something strange going on using this workaround with PyQt5. Don't use it.

`TypeError: sequence item 0: expected str instance, tuple found`  
or  
`TypeError: '<' not supported between instances of 'function' and 'function'`

Strange error messages don't match the visible code and appear between `m = MyClass()` and a print in `MyClass.__init__`.
