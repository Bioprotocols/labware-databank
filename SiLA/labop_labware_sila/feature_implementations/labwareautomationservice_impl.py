# Generated by sila2.code_generator; sila2.__version__: 0.10.2
from __future__ import annotations

from typing import TYPE_CHECKING

import logging

from sila2.server import MetadataDict

from ..generated.labwareautomationservice import (
    GetGrippingHeight_Responses,
    GetLabwareDimensions_Responses,
    GetLabwareWellVolume_Responses,
    LabwareAutomationServiceBase,
)

from labop_labware_ontology.labop_labware_ontology_impl import LabwareInterface

if TYPE_CHECKING:
    from ..server import Server


class LabwareAutomationServiceImpl(LabwareAutomationServiceBase):
    def __init__(self, parent_server: Server) -> None:
        super().__init__(parent_server=parent_server)

        # load all ontologies
       
        print("**** ------", self.parent_server.emmo_filename)

        self.labware_ontology = LabwareInterface( emmo_filename=self.parent_server.emmo_filename, 
                                                  lw_tbox_filename=self.parent_server.lw_tbox_filename, 
                                                  lw_abox_filename=self.parent_server.lw_abox_filename)
        self.lw_abox = self.labware_ontology.lolw_abox.lolwa


    def GetLabwareDimensions(
        self, Manufacturer: str, ProductID: str, Unit: str, *, metadata: MetadataDict
    ) -> GetLabwareDimensions_Responses:
        
        logging.debug(f"lw dimensions: Manufacturer: {Manufacturer}, productID: {ProductID}, unit: {Unit}")

        try:
            res = self.lw_abox.search(hasManufacturer=Manufacturer, hasProductID=ProductID)[0]
            print(res)
            lw_dimensions = { "Length": res.hasLength.length, "Width": res.hasWidth.length, "Height": res.hasHeight.length }
            return GetLabwareDimensions_Responses(Dimensions=str(lw_dimensions))
        except Exception as e:
            logging.error(f"Error: {e}")
            # TODO: raise error
            return GetLabwareDimensions_Responses(Dimensions="{}")
        

    def GetGrippingHeight(
        self, Manufacturer: str, ProductID: str, Unit: str, Lidded: bool, *, metadata: MetadataDict
    ) -> GetGrippingHeight_Responses:

        logging.debug(f"Manufacturer: {Manufacturer}, productID: {ProductID}, unit: {Unit}, lidded: {Lidded}")

        try:
            res = self.lw_abox.search(hasManufacturer=Manufacturer, hasProductID=ProductID)[0]
            if Lidded:
                return GetGrippingHeight_Responses(GrippingHeight=res.hasGrippingHeightWithLid.length)
            else:
                return GetGrippingHeight_Responses(GrippingHeight=res.hasGrippingHeight.length)
        except Exception as e:
            logging.error(f"Error: {e}")
            # TODO: raise error
            return GetGrippingHeight_Responses(GrippingHeight=0.0)
        


    def GetLabwareWellVolume(
        self, Manufacturer: str, ProductID: str, Unit: str, *, metadata: MetadataDict
    ) -> GetLabwareWellVolume_Responses:
        

        try:
            res = self.lw_abox.search(hasManifacturer = Manufacturer, hasProductID = ProductID)[0]
            return GetLabwareWellVolume_Responses(Volume=res.hasWellVolume.volume)
        except Exception as e:
            logging.error(f"Error: {e}")
            # TODO: raise error
            return GetLabwareWellVolume_Responses(Volume=0.0)

        


