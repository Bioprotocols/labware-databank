"""_____________________________________________________________________

:PROJECT: LabOP Labware Ontology

* Main module implementation *

:details:  Main module implementation.

.. note:: -
.. todo:: - 
________________________________________________________________________
"""

import os
import pathlib
import logging
from enum import Enum, auto
from ontopy import World
from ontopy.utils import write_catalog

import owlready2

from .labop_labware_ontology_interface import LOLabwareInterface
from .__init__ import __version__  # Version of this ontology

from .labware_tbox import LOLabwareTBox

logger = logging.getLogger(__name__)


class UsedOntologies(Enum):
    MEASUREMENT: int = auto()
    LABWARE: int = auto()
    DEVICES: int = auto()
    DUBLIN_CORE: int = auto()
    FOAF: int = auto()


class LOLabware(LOLabwareInterface):
    def __init__(self, db_path: str = None, db_name: str = None) -> None:
        """Implementation of the LOLabwareInterface
        """

        print("++++:", __version__)

        db_name_full = None


        # TODO: in later versions, we need to distinguish between top-level, mid-level and specific ontologies 
        output_filename_base = os.path.join('..', '..', 'labop_labware')
        self.lolw_owl_filename = f'{output_filename_base}-v{__version__}.owl'
        self.lolw_ttl_filename = f'{output_filename_base}-v{__version__}.ttl'

        self.lolw_base_iri = 'http://www.labop.org/labware#'
        self.lolw_version_iri = f'http://www.labop.org/{__version__}/labware'

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

        self.emmo_url = (
            'https://raw.githubusercontent.com/emmo-repo/emmo-repo.github.io/'
            'master/versions/1.0.0-beta/emmo-inferred-chemistry2.ttl')
        self.emmo_url_local = os.path.join(pathlib.Path(
            __file__).parent.resolve(), "emmo", "emmo-inferred-chemistry2")

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

        # importing labOP ontology modules

        lolw_tbox = LOLabwareTBox(self.emmo_world)
        lolw_tbox.define_ontology()
        self.lolw.imported_ontologies.append(lolw_tbox.lolw)
        self.lolw.sync_python_names()

    def save_ontology(self, filename: str = None, format='turtle'):
        """Save the ontology to file.

        :param filename: Filename to save the ontology to.
        :param format: Format to save the ontology in.
        """
        if filename is None:
            filename = self.lolw_ttl_filename
        self.lolw.save(file=filename, format=format)
