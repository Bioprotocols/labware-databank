"""_____________________________________________________________________

:PROJECT: LabOP Labware Ontology

* Labop labware interface implementation *

:details:  Main module LabwareInterface implementation.

.. note:: -
.. todo:: - 
________________________________________________________________________
"""

import os
import pathlib
import logging

from ontopy import World
from ontopy.utils import write_catalog

#import owlready2

from labop_labware_ontology.labop_labware_ontology_interface import LOLabwareInterface
from labop_labware_ontology import __version__  # Version of this ontology

from labop_labware_ontology.emmo_extension_tbox import EMMOExtensionTBox
from labop_labware_ontology.labware_tbox import LOLabwareTBox
from labop_labware_ontology.labware_abox import LOLabwareABox

from labop_labware_ontology.export_ontology import export_ontology

logger = logging.getLogger(__name__)

class LabwareInterface(LOLabwareInterface):
    def __init__(self, db_path: str = None, 
                 db_name: str = None,
                 emmo_filename: str = None,
                 lw_tbox_filename: str = None,
                 lw_abox_filename: str = None) -> None:
        """Implementation of the LOLabwareInterface
        """
        db_name_full = None

        # might be moved to export_ontology.py
        self.prefix_dict = {
            'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
            'xml': "http://www.w3.org/XML/1998/namespace",
            'xsd': "http://www.w3.org/2001/XMLSchema#",
            'owl': "http://www.w3.org/2002/07/owl#",
            'skos': "http://www.w3.org/2004/02/skos/core#",
            'dc': "http://purl.org/dc/elements/1.1/",
            'dcterm': "http://purl.org/dc/terms/",
            'dctype': "http://purl.org/dc/dcmitype/",
            'foaf': "http://xmlns.com/foaf/0.1/",
            'wd': "http://www.wikidata.org/entity/",
            'ex': "http://www.example.com/",
            'emmo': "http://emmo.info/emmo#",
        }

        # using latest EMMO ontology
        self.emmo_url = "emmo-development"  
        
        # in case of a local copy of EMMO
        # self.emmo_url_local = os.path.join(pathlib.Path(
        #     __file__).parent.resolve(), "emmo")  #self.emmo_url_local + '.ttl'
        if os.path.isfile(emmo_filename):
            self.emmo_url = self.emmo_url_local

        # for persistent storage of ontology:
        
        if db_path is not None and db_name is not None:
            if not os.path.exists(db_path):
                os.makedirs(db_path)
            db_name_full = os.path.join(db_path, db_name) 
        if db_name_full is not None:
            self.emmo_world = World(filename=db_name_full)
        else:  # in memory SQLITE database
            self.emmo_world = World()

        # create EMMO ontology object 
        self.emmo = self.emmo_world.get_ontology(self.emmo_url)
        self.emmo.load()               # reload_if_newer = True
        self.emmo.sync_python_names()  # synchronize annotations
        self.emmo.base_iri = self.emmo.base_iri.rstrip('/#')
        self.catalog_mappings = {self.emmo.base_iri: self.emmo_url}


        # extending EMMO with Labware specific classes and properties
        self.emmo_ext_tbox = EMMOExtensionTBox(self.emmo, self.emmo_url)

        # create Labware Terminology box object
        self.lolw_tbox = LOLabwareTBox(lw_tbox_filename, self.emmo_world, self.emmo, self.emmo_url)
        
        #self.lolw.imported_ontologies.append(self.lolw_tbox.lolw)
        
        # create Labware Assertion Box  (ABox) object
        self.lolw_abox = LOLabwareABox(lw_abox_filename, emmo_world=self.emmo_world, emmo=self.emmo, emmo_url=self.emmo_url, lw_tbox=self.lolw_tbox)

        #self.lolw.sync_python_names()

    def export_ontologies(self, path: str = "../ontologies/", format='turtle') -> None:
        """save all ontologies """

        self.emmo_ext_tbox.export(path=path, format=format)
        self.lolw_tbox.export(path=path, format=format)
        self.lolw_abox.export(path=path, format=format)



