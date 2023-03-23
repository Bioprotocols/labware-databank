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
        self.labware_ontology = LabwareInterface()
        self.lw_abox = self.labware_ontology.lolw_abox.lolwa


    def GetLabwareDimensions(
        self, Manufacturer: str, ProductID: str, Unit: str, *, metadata: MetadataDict
    ) -> GetLabwareDimensions_Responses:
        
        logging.debug(f"lw dimensions: Manufacturer: {Manufacturer}, productID: {ProductID}, unit: {Unit}")

        try:
            res = self.lw_abox.search(hasManifacturer = Manufacturer, hasProductID = ProductID)
        except Exception as e:
            logging.error(f"Error: {e}")
            # TODO: raise error
            return GetLabwareDimensions_Responses(Dimensions="{}")

        lw_dimensions = { "Length": res.hasLength.length, "Width": res.hasWidth.width, "Height": res.hasHeight.height }

        return GetLabwareDimensions_Responses(Dimensions=str(lw_dimensions))
        

    def GetGrippingHeight(
        self, Manufacturer: str, ProductID: str, Unit: str, Lidded: bool, *, metadata: MetadataDict
    ) -> GetGrippingHeight_Responses:

        logging.debug(f"Manufacturer: {Manufacturer}, productID: {ProductID}, unit: {Unit}, lidded: {Lidded}")

        if Lidded:
            gripping_height = 33.333
        else:
            gripping_height = 42.0

        return GetGrippingHeight_Responses(GrippingHeight=gripping_height)

    def GetLabwareWellVolume(
        self, Manufacturer: str, ProductID: str, Unit: str, *, metadata: MetadataDict
    ) -> GetLabwareWellVolume_Responses:
        lw_well_volume = 1000.0

        return GetLabwareWellVolume_Responses(Volume=lw_well_volume)


