#!/usr/bin/env python
"""Tests for `labop_labware_ontology` package."""
# pylint: disable=redefined-outer-name
from labop_labware_ontology import __version__
from labop_labware_ontology.labop_labware_ontology_interface import GreeterInterface
from labop_labware_ontology.labop_labware_ontology_impl import HelloWorld

def test_version():
    """Sample pytest test function."""
    assert __version__ == "0.0.1"

def test_GreeterInterface():
    """ testing the formal interface (GreeterInterface)
    """
    assert issubclass(HelloWorld, GreeterInterface)

def test_HelloWorld():
    """ Testing HelloWorld class
    """
    hw = HelloWorld()
    name = 'yvain'
    assert hw.greet_the_world(name) == f"Hello world, {name} !"

