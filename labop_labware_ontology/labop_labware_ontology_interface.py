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

class LOLabwareInterface(metaclass=ABCMeta):
    """ LabOP Labware Ontology formal Interface
        TODO: test, if ABC baseclass is working
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'save_ontology') and 
                callable(subclass.save_ontology) or 
                NotImplemented)
        
    @abstractclassmethod 
    def save_ontology(self, filename : str = None,  format='turtle') -> None:
        """ save ontology"""