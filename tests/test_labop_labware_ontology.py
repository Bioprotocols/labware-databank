#!/usr/bin/env python
"""Tests for `labop_labware_ontology` package."""
# pylint: disable=redefined-outer-name
from labop_labware_ontology import __version__
from labop_labware_ontology.labop_labware_ontology_interface import LOLabwareInterface
from labop_labware_ontology.labop_labware_ontology_impl import LabwareInterface

def test_version():
    """Sample pytest test function."""
    assert __version__ == "0.0.1"

def test_LOLabwareInterface():
    """ testing the formal interface (GreeterInterface)
    """
    assert issubclass(LabwareInterface, LOLabwareInterface)

def test_LabwareInterface():
    """ Testing LabwareInterface class
    """
    lwi = LabwareInterface()
    assert lwi.lolw_base_iri == "http://www.labop.org/labware#"

