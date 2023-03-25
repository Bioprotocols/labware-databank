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
import numpy as np

from labop_labware_ontology import __version__ # Version of this ontology
from labop_labware_ontology.emmo_utils import en, pl
from labop_labware_ontology.export_ontology import export_ontology

class LOLabwareABox:
    def __init__(self, lw_abox_filename:str = None, emmo_world=None, emmo=None, emmo_url: str = None, lw_tbox=None) -> None:

        # TDOO: move ontolgy definition to here

        self.emmo = emmo
        self.emmo_url = emmo_url
        self.lolwt = lw_tbox.lolwt
        
        self.base_iri = 'http://www.labop.org/labware-a#'
        self.lolwa_version_iri = f'http://www.labop.org/{__version__}/labware-a'

        print("LOLabwareABox:lw_abox_filename:", lw_abox_filename)

        if lw_abox_filename is None:
            self.lolwa = emmo_world.get_ontology(self.base_iri)
        else:
            print("loading ontology from file: ", lw_abox_filename, " ...")
            self.lolwa = emmo_world.get_ontology(lw_abox_filename).load()
            print(" ##### classes:", list(self.lolwa.classes()))  

        self.emmo.imported_ontologies.append(self.lolwa)
        self.emmo.sync_python_names()

    def export(self, path: str = ".", format='turtle') -> None:
        """save ontology """
        print("LOLabwareABox:export: path:", path)
        export_ontology(ontology=self.lolwa, path=path, onto_base_filename='labop_labware_abox', format=format, emmo_url=self.emmo_url)


    # cleaning id string, by replace - with _ and removing spaces, stripping and lowercasing
    def clean_id(self, id_str):
        return id_str.replace("-","_").replace(" ","").strip().lower()


    def import_csv(self, csv_filename="labware_catalogue.csv"):
        
        labware_cat_df = pd.read_csv(csv_filename, delimiter=";")
        labware_cat_df = labware_cat_df.reset_index()  # make sure indexes pair with number of rows

        # create the labware individuals
        with self.lolwa:
            for index,row in labware_cat_df.iterrows():
                print( self.clean_id(row['Id']), "-- >", row['Manufacturer'], row['ProductID'], row['UNSPSC'], "EC: ", row['eClass'] )
                law = self.lolwt.Labware( self.clean_id(row['Id']),
                                        # ;Description;ImageLink/URL;UNSPSC;eClass;Vendor;CatalogueID;WellCount;ColumnCount;RowCount;LabwareLength/mm;LabwareWidth/mm;LabwareHeight/mm;Mass/g;LabwareMaterial;SurfaceTreatment;Color;WellVolume/ul;A1Position(col,row);WellDiameter/mm;WellColDistance/mm;WellRowDistance/mm;WellDepth/mm;WellShape;WellBottomShape;Liddable/bool;Lid((Manufacturer, ProdID));Applications;AcceptableLids
                                        hasManufacturer=row['Manufacturer'],
                                        hasProductID=row['ProductID'] if row['ProductID'] is not np.nan else "unknown",
                                        # LabWareType
                                        # Description
                                        #hasImageLink=row['ImageLink/URL'] if row['ImageLink/URL'] is not np.nan else "http://",
                                        #hasUNSPSC=row['UNSPSC'] if row['UNSPSC'] is not np.nan else "unknown",
                                        #hasEClass=row['eClass'] if row['eClass'] is not np.nan else "unknown",
                                        #hasVendorName=row['Vendor'],
                                        #hasVendorProductID=row['CatalogueNumber'],
                                        hasNumWells=row['WellCount'] if row['WellCount'] is not np.nan else 0,
                                        hasNumCols=row['ColumnCount'] if row['ColumnCount'] is not np.nan else 0,
                                        hasNumRows=row['RowCount'] if row['RowCount'] is not np.nan else 0,
                                        hasLength=self.emmo.Length(length=row['LabwareLength/mm']) if row['LabwareLength/mm'] is not np.nan else 0,
                                        hasWidth=self.emmo.Length(length=row['LabwareWidth/mm']) if row['LabwareWidth/mm'] is not np.nan else 0,
                                        hasHeight=self.emmo.Length(length=row['LabwareHeight/mm']) if row['LabwareHeight/mm'] is not np.nan else 0,
                                        hasGrippingHeight=self.emmo.Length(length=float(row['LabwareHeight/mm']) - 2 )  if row['LabwareHeight/mm'] is not np.nan else 0,
                #                         hasMass=row['Weight[g]'],
                #                         # LabwareMaterial
                #                         # SurfaceTreatment;
                #                         # Color
                #                         hasColorDescription=row['Color'],
                #                         # WellVolume[ul]
                                        hasWellVolume=row['WellVolume/ul'] if row['WellVolume/ul'] is not np.nan else 0,
                #                         # A1Position[col,row];
                #                         hasA1Position=row['A1Position[col,row]'],
                #                         # WellColDistance[mm]
                #                         hasWellDistanceRow=row['WellRowDistance[mm]'],
                #                         # WellRowDistance[mm]
                #                         hasWellDistanceCol=row['WellColDistance[mm]'],
                #                         # WellDepth[mm]
                #                         hasWellDepth=row['WellDepth[mm]'],
                #                         # WellShape
                #                         hasShapeWell=row['WellShape'],
                #                         # WellBottomShape
                #                         hasShapeWellBottom=row['WellBottomShape'],
                #                         # Liddable[bool]
                #                         isLiddable=row['Liddable[bool]'],
                #                         # Lid[[Manufacturer,ProdNumber]];
                #                         # Applications;
                #                         # Notes
                                    )
                
