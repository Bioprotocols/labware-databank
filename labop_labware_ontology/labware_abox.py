
# python module that defines the individuals of the labware ontology. Since it contains the individuals, it is called the ABox ("A" for "assertions").


import os
import pathlib
import logging
import pandas as pd


class LOLabwareABox:
    def __init__(self, emmo=None, lolwt=None, lolwa=None) -> None:

        # TDOO: move ontolgy definition to here

        self.emmo = emmo
        self.lolwt = lolwt
        self.lolwa = lolwa

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
                
