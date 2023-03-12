"""_____________________________________________________________________

:PROJECT: LabOP Labware Ontology

* Main module implementation *

:details: python module that defines the individuals of the labware ontology. 
          Since it contains the individuals, it is called the ABox ("A" for "assertions").

.. note:: -
.. todo:: - 
________________________________________________________________________
"""



import os
import pathlib
import logging
import pandas as pd

from labop_labware_ontology import __version__ # Version of this ontology
from labop_labware_ontology.emmo_utils import en, pl
from labop_labware_ontology.export_ontology import export_ontology

class LOLabwareABox:
    def __init__(self, emmo_world=None, emmo=None, emmo_url: str = None, lw_tbox=None) -> None:

        # TDOO: move ontolgy definition to here

        self.emmo = emmo
        self.emmo_url = emmo_url
        self.lolwt = lw_tbox.lolwt
        
        self.lolwa_base_iri = 'http://www.labop.org/labware-a#'
        self.lolwa_version_iri = f'http://www.labop.org/{__version__}/labware-a'

        self.lolwa = emmo_world.get_ontology(self.lolwa_base_iri)
        self.emmo.imported_ontologies.append(self.lolwa)
        self.emmo.sync_python_names()

    def export(self, path: str = "../ontologies/", format='turtle') -> None:
        """save ontology """
        export_ontology(ontology=self.lolwa, path=path, onto_base_filename='labop_labware_abox', format=format, emmo_url=self.emmo_url)


    def import_csv(self, csv_filename="labware_catalogue.csv"):
        
        labware_cat_df = pd.read_csv(csv_filename, delimiter=";")
        labware_cat_df = labware_cat_df.reset_index()  # make sure indexes pair with number of rows

        # create the labware individuals
        with self.lolwa:
            for index,row in labware_cat_df.iterrows():
                print(row['Id'], "-- >", row['Manifacturer'], row['ProductID'] )
                law = self.lolwa.Labware( row['Id'],
                                        #Id;Manifacturer;
                                        hasManifacturer=row['Manifacturer'],
                                        #ProductID;
                                        hasProductID=row['ProductID'],
                                        # Description
                                        # ImageLink[URL]
                                        # UNSPSC
                                        # eCl@ss
                                        # Vendor
                                        # CatalogueNumber
                                        # WellCount
                                        hasNumWells=row['WellCount'],
                                        # ColumnCount;
                                        hasNumCols=row['ColumnCount'],
                                        # RowCount
                                        hasNumRows=row['RowCount'],
                                        # LabwareLength[mm]
                                        # LabwareWidth[mm]
                                        # LabwareHeight[mm]
                                        hasHeight=row['LabwareHeight[mm]'],
                                        # Weight[g]
                                        hasWeight=row['Weight[g]'],
                                        # LabwareMaterial
                                        # SurfaceTreatment;
                                        # Color
                                        # WellVolume[ul]
                                        # A1Position[col,row];
                                        # WellColDistance[mm]
                                        # WellRowDistance[mm]
                                        # WellDepth[mm]
                                        # WellShape
                                        # WellBottomShape
                                        # Liddable[bool]
                                        # Lid[[Manufacturer,ProdNumber]];
                                        # Applications;
                                        # Notes
                                    )
                
