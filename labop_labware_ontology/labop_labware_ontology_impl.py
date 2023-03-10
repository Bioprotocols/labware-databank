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
import rdflib  # noqa: E402, F401

from ontopy import World
from ontopy.utils import write_catalog

import owlready2

from .labop_labware_ontology_interface import LOLabwareInterface
from .__init__ import __version__  # Version of this ontology

from .emmo_extension_tbox import EMMOExtensionTBox
from .labware_tbox import LOLabwareTBox
from .labware_abox import LOLabwareABox

logger = logging.getLogger(__name__)


# --- ontology definition helper functions

def en(s):
    """Returns `s` as an English location string."""
    return owlready2.locstr(s, lang='en')


def pl(s):
    """Returns `s` as a plain literal string."""
    return owlready2.locstr(s, lang='')


class LOLabware(LOLabwareInterface):
    def __init__(self, db_path: str = None, db_name: str = None) -> None:
        """Implementation of the LOLabwareInterface
        """

        self.__version__ = __version__
        print("++++:", self.__version__)

        db_name_full = None


        # TODO: in later versions, we need to distinguish between top-level, mid-level and specific ontologies 
        output_filename_base = os.path.join('..', 'ontologies', 'labop_labware_tbox')
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

        # extending EMMO

        self.emmo_ext_tbox = EMMOExtensionTBox(self.emmo)

        # importing labOP ontology modules

        self.lolw_tbox = LOLabwareTBox(self.emmo, self.lolw)
        #self.lolw_tbox.define_ontology()
        #self.lolw.imported_ontologies.append(self.lolw_tbox.lolw)

        self.lolw_abox = LOLabwareABox(self.emmo, self.lolw)

        self.lolw.sync_python_names()

    def save_ontologies(self, path: str = ".", format='turtle') -> None:
        """save all ontologies """

        self.save_ontology(ontology=self.lolw, path=path, onto_filename='labop_labware_tbox', format=format)


    def save_ontology(self, ontology = None, path: str = None, onto_filename: str = None, format='turtle'):
        """Save the ontology to file.

        :param filename: Filename to save the ontology to.
        :param format: Format to save the ontology in.

        :TODO: add prefix mapping
        """
        
        print("base iri: ---->", ontology.base_iri)

        # Save new ontology as owl
        ontology.sync_attributes(name_policy='uuid', 
                                 class_docstring='elucidation',
                                 name_prefix='labop_')
        
        version_iri = f"http://www.labop.org/{self.__version__}/{onto_filename}"

        ontology.set_version(version_iri=version_iri)
        ontology.dir_label = False

        #!self.lolw_tbox.catalog_mappings[self.lolw_version_iri] = self.lolw_ttl_filename 

        #################################################################
        # Annotate the ontology metadata
        #################################################################

        ontology.metadata.abstract.append(en(
                'An EMMO-based domain ontology for scientific labware.'
                'labop-labware is released under the Creative Commons Attribution 4.0 '
                'International license (CC BY 4.0).'))

        ontology.metadata.title.append(en('LabOP-Labware'))
        ontology.metadata.creator.append(en('mark doerr'))
        ontology.metadata.contributor.append(en('university greifswald'))
        ontology.metadata.publisher.append(en('mark doerr'))
        ontology.metadata.license.append(en(
            'https://creativecommons.org/licenses/by/4.0/legalcode'))
        ontology.metadata.versionInfo.append(en(self.__version__))
        ontology.metadata.comment.append(en(
            'The EMMO requires FaCT++ reasoner plugin in order to visualize all'
            'inferences and class hierarchy (ctrl+R hotkey in Protege).'))
        ontology.metadata.comment.append(en(
            'This ontology is generated with data from the ASE Python package.'))
        ontology.metadata.comment.append(en(
            'Contacts:\n'
            'mark doerr\n'
            'University Greifswald\n'
            'email: mark.doerr@suni-greifswald.de\n'
            '\n'
            ))

        ontology.save(onto_filename, overwrite=True)
        #olw.save(labop_measurement_owl_filename, overwrite=True)
        #!write_catalog(self.lolw_tbox.catalog_mappings)
        # olw.sync_reasoner()
        # olw.save('olw-measurement-inferred.ttl', overwrite=True)
        # ...and to the sqlite3 database.
        # world.save()


        # Manually change url of EMMO to `emmo_url` when importing it to make
        # it resolvable without consulting the catalog file.  This makes it possible
        # to open the ontology from url in Protege
        
        # g = rdflib.Graph()
        # g.parse(onto_filename , format='turtle')
        # for s, p, o in g.triples(
        #         (None, rdflib.URIRef('http://www.w3.org/2002/07/owl#imports'), None)):
        #     if 'emmo-inferred' in o:
        #         g.remove((s, p, o))
        #         g.add((s, p, rdflib.URIRef(self.emmo_url)))
        # g.serialize(destination=onto_filename, format='turtle')


