# Generated by sila2.code_generator; sila2.__version__: 0.10.2
from __future__ import annotations

import os
import logging
import pandas as pd

from typing import TYPE_CHECKING

from sila2.server import MetadataDict

from labop_labware_ontology.labware_tbox import LOLabwareTBox


from ..generated.labwarequeryservice import LabwareQueryServiceBase, SPARQLQuery_Responses

if TYPE_CHECKING:
    from ..server import Server


class LabwareQueryServiceImpl(LabwareQueryServiceBase):
    def __init__(self, parent_server: Server) -> None:
        super().__init__(parent_server=parent_server)

        self.lw = LOLabwareTBox()
        self.lw.define_ontology()

        self.load_labware()

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
    'lolw': "http://www.labop.org/labware#",
}

        self.graph = self.lw.emmo_world.as_rdflib_graph()

        for prefix, iri in self.prefix_dict.items():
            print(prefix, "--- ", iri )
            self.graph.bind(prefix, iri)



    def load_labware(self) -> None:
        #raise NotImplementedError  # TODO
        print(os.getcwd())

        logging.info(f"load loading labware")

        strateos_csv = "./strateos_labware.csv"
        strateos_cont_df = pd.read_csv(strateos_csv, delimiter=";")
        strateos_cont_df = strateos_cont_df.reset_index()  # make sure indexes pair with number of rows

        with self.lw.lolw:     
            for index,row in strateos_cont_df.iterrows():
                print(row['Id'], "-- >", row['WellCount'])
                law = self.lw.lolw.Labware( row['Id'],
                                        hasManifacturer=row['Vendor'],
                                        hasNumRows=row['WellCount'] / row['ColumnCount'], 
                                        hasNumCols=row['ColumnCount'],
                                        hasNumWells=row['WellCount'],
                                        #hasHeight=row['Height (mm)'],
                                        #hasWellVolume=row['Well Volume (ul)'],
                                        )        

    def SPARQLQuery(self, Query: str, *, metadata: MetadataDict) -> SPARQLQuery_Responses:
        #raise NotImplementedError  # TODO

        logging.info(f"SPARQLQuery called with Query: {Query}")

        results = list(self.lw.emmo_world.sparql(Query))

        #res = F"{Query} -> {self.lw.lolw.mtp_96_flat_uv.is_a} "

        return SPARQLQuery_Responses(Result=str(results))
