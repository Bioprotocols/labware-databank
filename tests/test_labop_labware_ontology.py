#!/usr/bin/env python
"""Tests for `labop_labware_ontology` package."""
# pylint: disable=redefined-outer-name
from labop_labware_ontology import __version__
from labop_labware_ontology.labop_labware_ontology_interface import LOLabwareDBInterface
from labop_labware_ontology.labop_labware_ontology_impl import LabwareDBInterface

def test_version():
    """Sample pytest test function."""
    assert __version__ == "0.0.1"

def test_LOLabwareInterface():
    """ testing the formal interface (GreeterInterface)
    """
    assert issubclass(LabwareDBInterface, LOLabwareDBInterface)

def test_LabwareInterface():
    """ Testing LabwareDBInterface class
    """
    lwi = LabwareDBInterface()
     
    assert lwi.lolw_tbox.lolwt_base_iri == 'http://www.labop.org/labware-t#'

