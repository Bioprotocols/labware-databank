"""_____________________________________________________________________

:PROJECT: LabOP Labware Ontology

* Main module formal interface. *

:details: In larger projects, formal interfaces are helping to define a trustable contract.
          Currently there are two commonly used approaches: 
          [ABCMetadata](https://docs.python.org/3/library/abc.html) or [Python Protocols](https://peps.python.org/pep-0544/)

       see also:
       ABC metaclass
         - https://realpython.com/python-interface/
         - https://dev.to/meseta/factories-abstract-base-classes-and-python-s-new-protocols-structural-subtyping-20bm

.. note:: -
.. todo:: - 
________________________________________________________________________
"""


# here is a 
from abc import ABCMeta, abstractclassmethod

class GreeterInterface(metaclass=ABCMeta):
    """ Greeter formal Interface
        TODO: test, if ABC baseclass is wor
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'greet_the_world') and 
                callable(subclass.greet_the_world) or 
                NotImplemented)
        
    @abstractclassmethod 
    def greet_the_world(self, name: str) -> str:
        """greeting module - adds a name to a greeting

        :param name: person to greet
        :type name: str
        """

