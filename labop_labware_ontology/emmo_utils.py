"""_____________________________________________________________________

:PROJECT: LabOP Labware Ontology

*  ontology definition helper functions *

:details:  ontology definition helper functions.

.. note:: -
.. todo:: - 
________________________________________________________________________
"""

import owlready2

def en(s):
    """Returns `s` as an English location string."""
    return owlready2.locstr(s, lang='en')


def pl(s):
    """Returns `s` as a plain literal string."""
    return owlready2.locstr(s, lang='')