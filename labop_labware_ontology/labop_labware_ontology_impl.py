"""_____________________________________________________________________

:PROJECT: LabOP Labware Ontology

* Main module implementation *

:details:  Main module implementation.

.. note:: -
.. todo:: - 
________________________________________________________________________
"""


import logging

from .labop_labware_ontology_interface import GreeterInterface

class HelloWorld(GreeterInterface):
    def __init__(self) -> None:
        """Implementation of the GreeterInterface
        """
        
    def greet_the_world(self, name: str) -> str:
        """greeting module - adds a name to a greeting

        :param name: person to greet
        :type name: str
        """
        logging.debug(f"Greeting: {name}")
        return f"Hello world, {name} !"        

