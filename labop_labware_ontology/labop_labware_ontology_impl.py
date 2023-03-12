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
    def __init__(self, db_path: str = None, db_name: str = None) -> None:
        """Implementation of the LOLabwareInterface
        """

        print("++++:", __version__)

        db_name_full = None


        # TODO: in later versions, we need to distinguish between top-level, mid-level and specific ontologies 
        output_filename_base = os.path.join('..', 'ontologies', 'labop_labware_tbox')
        self.lolw_owl_filename = f'{output_filename_base}-v{__version__}.owl'
        self.lolw_ttl_filename = f'{output_filename_base}-v{__version__}.ttl'

        self.lolw_base_iri = 'http://www.labop.org/labware#'
        self.lolw_version_iri = f'http://www.labop.org/{__version__}/labware'

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


        # TODO: use main EMMO ontology :       
        # alternative url   "https://raw.githubusercontent.com/emmo-repo/EMMO/master/self.emmo.ttl"

        self.emmo_url = "emmo-development" # (
        #    'https://raw.githubusercontent.com/emmo-repo/emmo-repo.github.io/'
        #    'master/versions/1.0.0-beta/emmo-inferred-chemistry2.ttl')
        self.emmo_url_local = os.path.join(pathlib.Path(
            __file__).parent.resolve(), "emmo", "emmo-inferred")

        if os.path.isfile(self.emmo_url_local + '.ttl'):
            self.emmo_url = self.emmo_url_local

        # for persistent storage of ontology:
        #self.emmo_world = World(filename="emmo_labop_labware.sqlite3")
        if db_path is not None:
            if not os.path.exists(db_path):
                os.makedirs(db_path)
            db_name_full = os.path.join(db_path, db_name)

        if db_name_full is not None:
            self.emmo_world = World(filename=db_name_full)
        else:  # in memory SQLITE database
            self.emmo_world = World()
        self.emmo = self.emmo_world.get_ontology(self.emmo_url)
        self.emmo.load()  # reload_if_newer = True
        self.emmo.sync_python_names()  # Synchronize annotations
        self.emmo.base_iri = self.emmo.base_iri.rstrip('/#')
        self.catalog_mappings = {self.emmo.base_iri: self.emmo_url}

        self.lolw = self.emmo_world.get_ontology(self.lolw_base_iri)
        self.lolw.imported_ontologies.append(self.emmo)
        self.lolw.sync_python_names()

        # extending EMMO with Labware specific classes and properties
        self.emmo_ext_tbox = EMMOExtensionTBox(self.emmo)

        # importing labOP ontology modules

        self.lolw_tbox = LOLabwareTBox(self.emmo, self.lolw)
        #self.lolw_tbox.define_ontology()
        #self.lolw.imported_ontologies.append(self.lolw_tbox.lolw)

        self.lolw_abox = LOLabwareABox(self.emmo, self.lolw)

        self.lolw.sync_python_names()

    def save_ontologies(self, path: str = "../ontologies/", format='turtle') -> None:
        """save all ontologies """

        export_ontology(ontology=self.emmo, path=path, onto_filename='labop_labware_emmo', format=format, emmo_url=self.emmo_url)
        export_ontology(ontology=self.lolw, path=path, onto_filename='labop_labware_tbox', format=format, emmo_url=self.emmo_url)


    


