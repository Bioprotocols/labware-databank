"""_____________________________________________________________________

:PROJECT: LabOP Labware Ontology

* Ontology export module *

:details:  generic ontology export module.

.. note:: -
.. todo:: - check rdflib formats
          - check emmo url
          - reactivate mappings
          - check, if base iri is set correctly
          - add prefix mapping
________________________________________________________________________
"""

import os
import logging
import rdflib

from labop_labware_ontology import __author__, __email__, __contributors__, __version__  # Version of this ontology
from labop_labware_ontology.emmo_utils import en, pl

def export_ontology(ontology = None, 
                    path: str = None,
                    base_iri: str = 'https://labop.org',
                    onto_base_filename: str = None,
                    title: str = None, 
                    description: str = None,
                    license: str = 'This ontology is released under the Creative Commons Attribution 4.0 International license (CC BY 4.0)',
                    license_url: str = 'https://creativecommons.org/licenses/by/4.0/',
                    format='turtle',
                    emmo_url: str = "http://emmo.info/emmo#") -> None:
        """Export/save the ontology to file.

        :param filename: Filename to save the ontology to.
        :param format: Format to save the ontology in [turtle, rdfxml, owlxml, ntriples, json-ld].

        :TODO: add prefix mapping
        """

        # output_filename_base = os.path.join('..', 'ontologies', 'labop_labware_tbox')
        # self.lolw_owl_filename = f'{output_filename_base}-v{__version__}.owl'
        # self.lolw_ttl_filename = f'{output_filename_base}-v{__version__}.ttl'

        # ontology file ending dictionary, based on rdflib formats
        onto_file_ending = { 'turtle': '.ttl', 'xml': '.rdf', 'owl': '.owl', 'ntriples': '.nt', 'json-ld': '.jsonld' }

        onto_filename_full = os.path.join(path, onto_base_filename) + onto_file_ending[format]
        
        print("base / ver. iri: ---->", onto_filename_full, ontology.base_iri)

        # Save new ontology as owl
        # ontology.sync_attributes(name_policy='uuid', 
        #                          class_docstring='elucidation',
        #                          name_prefix='labop_')
        
        version_iri = f"{base_iri}/{__version__}/{onto_base_filename}"

        ontology.set_version(version_iri=version_iri)
        ontology.dir_label = False

        #! reactivate ontology.catalog_mappings[self.lolw_version_iri] = self.lolw_ttl_filename 

        #################################################################
        # Annotate the ontology metadata
        #################################################################

        ontology.metadata.abstract.append(en(f"{description}\n {license}\n"))

        ontology.metadata.title.append(en(title))
        ontology.metadata.creator.append(en(__author__))
        ontology.metadata.contributor.append(en(__contributors__))
        ontology.metadata.publisher.append(en(__author__))
        ontology.metadata.license.append(en(license_url))
        ontology.metadata.versionInfo.append(en(__version__))
        ontology.metadata.comment.append(en(
            'The EMMO requires FaCT++ reasoner plugin in order to visualize all'
            'inferences and class hierarchy (ctrl+R hotkey in Protege).'))
        ontology.metadata.comment.append(en(
            'This ontology is generated with data from the EMMOntoPy Python package.'))
        ontology.metadata.comment.append(en(
            f'Contacts:\n {__author__} \n {__email__ }\n\n'))
        
       
        ontology.save(onto_filename_full, overwrite=True, format=format)

        #olw.save(labop_measurement_owl_filename, overwrite=True)
        #!write_catalog(self.lolw_tbox.catalog_mappings)
        # olw.sync_reasoner()
        # olw.save('olw-measurement-inferred.ttl', overwrite=True)
        # ...and to the sqlite3 database.
        # world.save()

        return

        #-------- inference ....


        # Manually change url of EMMO to `emmo_url` when importing it to make
        # it resolvable without consulting the catalog file.  This makes it possible
        # to open the ontology from url in Protege
        
        g = rdflib.Graph()
        g.parse(onto_filename_full, format='turtle')
        for s, p, o in g.triples(
                (None, rdflib.URIRef('http://www.w3.org/2002/07/owl#imports'), None)):
            if 'emmo-inferred' in o:
                g.remove((s, p, o))
                g.add((s, p, rdflib.URIRef(emmo_url)))
        g.serialize(destination=onto_filename_full, format='turtle')