"""_____________________________________________________________________

:PROJECT: LabOP Labware Ontology

* Terminology box of the Labware Ontology *

:details:  Main module implementation.

            python module that defines an ontology of common labware classes that are used in a scientific lab, based on EMMOntoPy
            it should be possible to use this ontology to automatically get the right SI units for the properties of the labware
            and to automatically get the right EMMO classes for the labware
            as much as possible, the ontology should be based on EMMO, but it may be necessary to add some classes and properties
            that are not in EMMO
            as much as possible should be inferred from EMMO, but it may be necessary to add some axioms
            the ontology should be able to be used in a lab notebook, and should be able to be used to automatically generate
            a labware inventory
            the ontology should be able to be used to automatically generate a labware database


.. note:: -
.. todo:: - 
________________________________________________________________________
"""


import os
import argparse
import sys
import pathlib
import logging

from ontopy import World
from ontopy.utils import write_catalog

from labop_labware_ontology.emmo_utils import en, pl

from owlready2 import DatatypeProperty, FunctionalProperty, ObjectProperty, AllDisjoint, Thing

from labop_labware_ontology import __version__ # Version of this ontology
from labop_labware_ontology.export_ontology import export_ontology

#from labop_labware_ontology.emmo_extension_tbox import EMMOExtensionTBox

class LOLabwareTBox:
    def __init__(self,
                 emmo_world=None, 
                 emmo=None, 
                 emmo_url: str = None) -> None:

        self.emmo = emmo
        self.emmo_world = emmo_world
        self.emmo_url = emmo_url
        
        self.lolwt_base_iri = 'http://www.labop.org/labop_labware_tbox#'
        
        self.lolwt = self.emmo_world.get_ontology(self.lolwt_base_iri)
        #self.lolwt.sync_attributes(name_policy="uuid", name_prefix="LOLWT_")

        self.lolwt.sync_python_names()
        # --- ontology definition
        self.define_ontology()

        self.emmo.imported_ontologies.append(self.lolwt)

    def export(self, path: str = ".", format='turtle') -> None:
        """save ontology """
        export_ontology(ontology=self.lolwt, path=path, onto_base_filename='labop_labware_tbox', format=format, emmo_url=self.emmo_url)

    def define_ontology(self):
        """defining the  labOP-labware ontology Terminology Box (TBox) """
        logging.debug('defining labware ontology')

        with self.lolwt:

            # Terminology Components (TBox) 

            class MeltingPoint(self.emmo.ThermodynamicTemperature):
                """Melting Point of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Melting_point")

            class BoilingPoint(self.emmo.ThermodynamicTemperature):
                """Boiling Point of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Boiling_point")

            class FlashPoint(self.emmo.ThermodynamicTemperature):
                """Flash Point of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Flash_point")


            # labware visual representation
            
            class ModelIcon(self.emmo.Thing):
                """Icon of the labware in X format. SVG ?"""
            

            class Model2D(self.emmo.Thing):
                """2D model of the labware in X format. SVG ?"""

            class Model3D(self.emmo.Thing):
                """3D model of the labware in X format. STL ?"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/3D_modeling")

            
            # AllDisjoint([ModelIcon, Model2D, Model3D])
           
           
            # multiwell labware
            # =================

            class WellVolume(self.emmo.Volume):
                """Total Labware volume """

            class WellDistRow(self.emmo.Length):
                """wWll-to-well distance in row direction"""
            
            class WellDistCol(self.emmo.Length):
                """"Well-to-well distance in column direction"""

            AllDisjoint([WellVolume, WellDistRow, WellDistCol])

            # Well properties of labware with wells
            class DepthWell(self.emmo.Length):
                """Well total well depth=hight"""
            
            class ShapeWell(self.emmo.Thing):
                """Well overall / top well shape,e.g. round, square, buffeled,..."""
            
            class ShapeWellBottom(self.emmo.Thing):
                """Well, bottom shape, flat, round, conical-"""

            class TopRadiusXY(self.emmo.Length):
                """Well radius of a round well at the top opening in x-y plane."""

            class BottomRadiusXY(self.emmo.Length):
                """Radius of a round bottom in xy plane / direction."""

            class BottomRadiusZ(self.emmo.Length):
                """Radius of a round bottom in z (hight) direction."""

            class ConeAngle(self.emmo.Angle):
                """Opening angle of cone in deg."""

            class ConeDepth(self.emmo.Length):
                """Depth of cone from beginning of conical shape."""

            class ShapePolygonXY(self.emmo.Thing):
                """Generalized shape polygon for more complex well shapes, in xy plane / direction."""

            class ShapePolygonZ(self.emmo.Thing):
                """Generalized shape polygon for more complex well shapes, in z direction = rotation axis."""

            class ShapeModel2D(self.emmo.Thing):
                """2D model of Well shape"""

            class ShapeModel3D(self.emmo.Thing):
                """3D model of Well shape"""

            class FirstInteractionPosition(self.emmo.Vector):
                """Position of first interaction point of a pipette tip with a well or a needle with a septum, rel. to the upper left corner of the labware. - what about round labware?"""


            #AllDisjoint([DepthWell, ShapeWell, ShapeWellBottom, TopRadiusXY, BottomRadiusXY, BottomRadiusZ, ConeAngle, ConeDepth, ShapePolygonXY, ShapePolygonZ, ShapeModel2D, ShapeModel3D, FirstInteractionPosition])


            # Labware Vendor related properties
            # =================================

            class Vendor(self.emmo.Thing):
                """Labware Vendor"""

            class VendorProductNumber(self.emmo.Thing):
                """Labware Vendor Product Number"""

            # UNSPSC
            class UNSPSC(self.emmo.Thing):
                """United Nations Standard Products and Services Code (UNSPSC) for labware"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/UNSPSC")

            # eCl@ss
            class EClass(self.emmo.Thing):
                """eCl@ss for labware"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/EClass")

            

            # Labware Classes
            # ====================

            # Basic properties

            class hasName(self.emmo.Symbol):
                """Name of something"""
                primaryName = []
                alternativeNames = []


            class Manufacturer(self.emmo.Thing):
                """Labware Manufacturer"""

                # URL of the manufacturer website
                # alternative names 
                # create Individuals for each manufacturer
                manufacturerURL = ""
                hasName

            class SKU(self.emmo.Thing):
                """Stock Keeping Unit (SKU) for labware"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Stock_keeping_unit")
                
                # Vendor or Manufacturer
                # Vendor SKU
                # Manufacturer SKU
                # buissiness ontology for SKU - http://purl.org/goodrelations/v1#hasStockKeepingUnit



            class Model2D(self.emmo.Thing):
                """2D model of the labware in X format. SVG ?"""

                modelURL = ""    # URL to the model
                model2D = ""     # 2D model as string representation of the model

            class Model3D(self.emmo.Thing):
                """3D model of the labware in X format. STL ?"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/3D_modeling")

                modelURL = ""    # URL to the model
                model3D = ""     # 3D model as string representation of the model


            class Labware(self.emmo.Device):
                """Labware is a utility device that all experiments are done with and which is not actively measuring. Examples: a container, a pipette tip, a reactor, ... """
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Labware")

                # is_a = [self.lolw.has_Material.some(str),
                #         self.lolw.has_NumCols.some(int),
                #         self.lolw.has_NumRows.some(int)]

            #  Relations / Properties
            # ========================

            # Physical Properties

            #class hasLength:
                # """"Labware total length """
                # is_a = [
                #     self.lolw.hasReferenceUnit.only(
                #         self.lolw.hasPhysicalDimension.only(self.lolw.Length)
                #     ),
                #     hasType.exactly(1, self.lolw.Real), ]

            # class hasWidth(FunctionalProperty):
            #     """Labware total width, """
            #     domain = [Labware]
            #     range = [Width]

            # class hasHeight(Labware >> self.lolw.Height, FunctionalProperty):
            #     """Labware total hight, without  any additions, like lids etc. """

            # class hasLengthTolerance(Labware >> self.emmo.Length, FunctionalProperty, ObjectProperty):
            #     """Labware length tolerance."""

            class hasLength(Labware >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Labware total length, without  any additions, like lids etc."""
                # alternativeNames = ["has horizontal depth"]
                # check definitions and common usage of length, width, height, depth, diameter, radius, ...
                # https://www.wikidata.org/wiki/Property:P5524

                

            class hasLengthTolerance(self.emmo.Length >> float, FunctionalProperty, DatatypeProperty):
                """Labware relative length tolerance (= measured width/target width)."""
            
            class hasWidth(Labware >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Labware total width, without  any additions, like lids etc."""
                # 
                
            
            class hasWidthTolerance(self.emmo.Length >> float, FunctionalProperty, DatatypeProperty):
                """Labware relative width tolerance (= measured width/target width)."""
            
            class hasHeight(Labware >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Labware total hight, without  any additions, like lids etc. """

            class hasHeightTolerance(self.emmo.Length >> float, FunctionalProperty, DatatypeProperty):
                """Labware height tolerance."""

            class hasGrippingHeight(Labware >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Labware total hight, without  any additions, like lids etc. """

            class hasGrippingHeightLidding(Labware >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Labware total hight, without  any additions, like lids etc. """
            
            class hasGrippingHeightWithLid(Labware >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Labware total hight, without  any additions, like lids etc. """

            class hasGrippingPressure(Labware >> self.emmo.Pressure, FunctionalProperty, ObjectProperty):
                """Labware max gripping pressure."""

            class hasRadiusXY(Labware >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Labware radius of a round shape in XY direction """

            class hasRadiusZ(Labware >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Labware radius of a round shape in XY direction """

            class hasVolume(Labware >> float, FunctionalProperty):
                """Total Labware volume """

            class hasHightLidded(Labware >> float, FunctionalProperty):
                """Labware total hight, with additions, like lids etc."""

            class hasHightStacked(Labware >> float, FunctionalProperty):
                """Labware stacking height without any additions, like lids."""

            class hasHightStackedLidded(Labware >> float, FunctionalProperty):
                """Labware stacking height with additions, like lids."""

            class hasMass(Labware >> float, FunctionalProperty):
                """Mass of the Labware """

            class hasMaxSheerForce(Labware >> self.emmo.Force, FunctionalProperty):
                """Max sheer force of the Labware, e.g. during centrifugation"""

            class hasCoatingMaterial(Labware >> str, FunctionalProperty):
                """Labware coating material"""

            class hasColorDescription(Labware >> str):
                """Labware color description, e.g. white, black, opaque, blue, transparent, ..."""

            class isTransparent(Labware >> bool, FunctionalProperty):
                """Labware is transparent in the visible range between 380 and 780 nm"""

            class hasColorRGB(Labware >> str, FunctionalProperty):
                """Labware color in RGB hex encoding"""

            class isLiddable(Labware >> bool, FunctionalProperty):
                """labware is liddable"""

            class isStackable(Labware >> bool, FunctionalProperty):
                """labware is stackable"""

            class isSealable(Labware >> bool, FunctionalProperty):
                """container is sealable"""

            class hasSetptum(Labware >> bool, FunctionalProperty):
                """Setptum of the Labware"""

            class hasMaterial(Labware >> str, DatatypeProperty):
                """Polymer, properties, like solvent tolerance, transparency, ...."""

            class hasSeptumMaterial(Labware >> str, FunctionalProperty):
                """Septum material"""

            class hasSeptumPenetrationForce(Labware >> self.emmo.Force, FunctionalProperty):
                """Septum penetration force"""


            # multiwell labware

            class hasNumCols(Labware >> int, FunctionalProperty):
                """Number of Columns of muti-well labware"""

            class hasNumRows(Labware >> int, FunctionalProperty):
                """Number of Rows of Labware"""

            class hasNumWells(Labware >> int, FunctionalProperty):
                """Number of Wells of muti-well labware"""

            # Production Properties / Metadata

            class hasManufacturer(Labware >> Manufacturer, FunctionalProperty):
                 """Name of the Manufacturer """
            
            class isProductType(Labware >> str, FunctionalProperty):
                """Labware product Type"""

            class hasModelID(Labware >> str, FunctionalProperty):
                """Labware model ID/number"""

            class hasProductID(Labware >> str, FunctionalProperty):
                """Manufacturer Product ID/Number of the Labware"""

            # multiwell labware properties

            class hasWellVolume(Labware >> float, FunctionalProperty):
                """Total Labware volume """

            class hasA1Position(Labware >> str, FunctionalProperty):
                """Labware A1 position"""

            class hasWellDistRow(Labware >> float, FunctionalProperty):
                """Well-to-well distance in row direction"""
            
            class hasWellDistCol(Labware >> float, FunctionalProperty):
                """"Well-to-well distance in column direction"""

            # Well properties of labware with wells
            class hasDepthWell(Labware >> float, FunctionalProperty):
                """Well total well depth=hight"""
            
            class hasShapeWell(Labware >> str, FunctionalProperty):
                """Well overall / top well shape,e.g. round, square, buffeled,..."""
            
            class hasShapeWellBottom(Labware >> str, FunctionalProperty):
                """Well, bottom shape, flat, round, conical-"""

            class hasTopRadiusXY(Labware >> float, FunctionalProperty):
                """Well radius of a round well at the top opening in x-y plane."""

            class hasBottomRadiusXY(Labware >> float, FunctionalProperty):
                """Radius of a round bottom in xy plane / direction."""

            class hasBottomRadiusZ(Labware >> float, FunctionalProperty):
                """Radius of a round bottom in z (hight) direction."""

            class hasConeAngle(Labware >> float, FunctionalProperty):
                """Opening angle of cone in deg."""

            class hasConeDepth(Labware >> float, FunctionalProperty):
                """Depth of cone from beginning of conical shape."""

            class hasShapePolygonXY(Labware >> float, FunctionalProperty):
                """Generalized shape polygon for more complex well shapes, in xy plane / direction."""

            class hasShapePolygonZ(Labware >> str, FunctionalProperty):
                """Generalized shape polygon for more complex well shapes, in z direction = rotation axis."""

            class hasShapeModel2D(Labware >> Model2D, FunctionalProperty, ObjectProperty):
                """2D model of Well shape"""

            class hasShapeModel3D(Labware >> Model3D, FunctionalProperty, ObjectProperty):
                """3D model of Well shape"""

            class hasImageLink(Labware >> str, FunctionalProperty):
                """Link to image of the Labware"""

            # labware with screw cap

            class hasScrewCap(Labware >> bool, FunctionalProperty):
                """Screw cap type"""

            class hasScrewCapMaterial(Labware >> str, FunctionalProperty):
                """Screw cap material"""
            
            class hasScrewCapColor(Labware >> str, FunctionalProperty):
                """Screw cap color"""


            # labware with snap cap


            # vendor specific properties
            class hasVendorName(Labware >> str, FunctionalProperty):
                """Vendor name"""
            class hasVendorProductID(Labware >> str, FunctionalProperty):
                """Vendor Product ID"""
            class hasUNSPSC(Labware >> str, FunctionalProperty):
                """UNSPSC code"""

            class hasEClass(Labware >> str, FunctionalProperty):
                """EClass code"""

            class hasEAN(Labware >> str, FunctionalProperty):
                """EAN code"""

            
            # further properties:

            # lengthAtEdge, lengthOverall, isSLAS1-2004compliant

            # isSLAS1-2004compliant

            

            # all disjoined properties

            # special labware classes
            # can be used for faster type testing
            # ===================================================

            class SLAS_1_2004_Plate(Labware):
                """Microtiter Plate according to SLAS 4-2004 standard"""
                equivalent_to = [ Labware & hasNumCols.value(12) &  hasNumRows.value(8) & hasNumWells.value(96) 
                                & hasWellVolume.value(100) & hasWellDistRow.value(9) & hasWellDistCol.value(9) 
                                & hasDepthWell.value(14.5) & hasShapeWell.value("round") & hasShapeWellBottom.value("flat") 
                                & hasTopRadiusXY.value(4.5) & hasBottomRadiusXY.value(4.5) & hasBottomRadiusZ.value(0) 
                                & hasConeAngle.value(0) & hasConeDepth.value(0) & hasShapePolygonXY.value(0) 
                                & hasShapePolygonZ.value(0) & hasShapeModel2D.value("circle") & hasShapeModel3D.value("cylinder") 
                                & hasScrewCap.value(False) & hasScrewCapMaterial.value("N/A") & hasScrewCapColor.value("N/A") 
                                & hasColorRGB.value("#FFFFFF") & hasMaterial.value("polystyrene") & hasMass.value(0) 
                                & hasMaxSheerForce.value(0) & hasCoatingMaterial.value("N/A") & hasSetptum.value(False) 
                                & hasSeptumMaterial.value("N/A") & hasSeptumPenetrationForce.value(0) & isLiddable.value(False) & isStackable.value(True) 
                                & isSealable.value(False) & hasManufacturer.value("N/A") & isProductType.value("N/A") & hasModelID.value("N/A") & hasProductID.value("N/A") ]
                
            class SLAS_2_2004_4_Plate(Labware):
                """Microtiter Plate according to SLAS 4-2004 standard"""
                equivalent_to = [ Labware & hasNumCols.value(12) &  hasNumRows.value(8) & hasNumWells.value(96) 
                                & hasWellVolume.value(100) & hasWellDistRow.value(9) & hasWellDistCol.value(9) 
                                & hasDepthWell.value(14.5) & hasShapeWell.value("round") & hasShapeWellBottom.value("flat") 
                                & hasTopRadiusXY.value(4.5) & hasBottomRadiusXY.value(4.5) & hasBottomRadiusZ.value(0) 
                                & hasConeAngle.value(0) & hasConeDepth.value(0) & hasShapePolygonXY.value(0) 
                                & hasShapePolygonZ.value(0) & hasShapeModel2D.value("circle") & hasShapeModel3D.value("cylinder") 
                                & hasScrewCap.value(False) & hasScrewCapMaterial.value("N/A") & hasScrewCapColor.value("N/A") 
                                & hasColorRGB.value("#FFFFFF") & hasMaterial.value("polystyrene") & hasMass.value(0) 
                                & hasMaxSheerForce.value(0) & hasCoatingMaterial.value("N/A") & hasSetptum.value(False) 
                                & hasSeptumMaterial.value("N/A") & hasSeptumPenetrationForce.value(0) & isLiddable.value(False) & isStackable.value(True) 
                                & isSealable.value(False) & hasManufacturer.value("N/A") & isProductType.value("N/A") & hasModelID.value("N/A") & hasProductID.value("N/A") ]
                
            class SLAS_2_2004_4_1_Plate(Labware):
                """Microtiter Plate according to SLAS 4-2004 standard"""
                equivalent_to = [ Labware & hasNumCols.value(12) &  hasNumRows.value(8) & hasNumWells.value(96) 
                                & hasWellVolume.value(100) & hasWellDistRow.value(9) & hasWellDistCol.value(9) 
                                & hasDepthWell.value(14.5) & hasShapeWell.value("round") & hasShapeWellBottom.value("flat") 
                                & hasTopRadiusXY.value(4.5) & hasBottomRadiusXY.value(4.5) & hasBottomRadiusZ.value(0) 
                                & hasConeAngle.value(0) & hasConeDepth.value(0) & hasShapePolygonXY.value(0) 
                                & hasShapePolygonZ.value(0) & hasShapeModel2D.value("circle") & hasShapeModel3D.value("cylinder") 
                                & hasScrewCap.value(False) & hasScrewCapMaterial.value("N/A") & hasScrewCapColor.value("N/A") 
                                & hasColorRGB.value("#FFFFFF") & hasMaterial.value("polystyrene") & hasMass.value(0) 
                                & hasMaxSheerForce.value(0) & hasCoatingMaterial.value("N/A") & hasSetptum.value(False) 
                                & hasSeptumMaterial.value("N/A") & hasSeptumPenetrationForce.value(0) & isLiddable.value(False) & isStackable.value(True) 
                                & isSealable.value(False) & hasManufacturer.value("N/A") & isProductType.value("N/A") & hasModelID.value("N/A") & hasProductID.value("N/A") ]

            class SLAS_4_2004_Plate(Labware):
                """96 Well Microtiter Plate according to SLAS 4-2004 standard"""
                equivalent_to = [ Labware & hasNumCols.value(12) &  hasNumRows.value(8) & hasNumWells.value(96) 
                                & hasWellVolume.value(100) & hasWellDistRow.value(9) & hasWellDistCol.value(9) 
                                & hasDepthWell.value(14.5) & hasShapeWell.value("round") & hasShapeWellBottom.value("flat") 
                                & hasTopRadiusXY.value(4.5) & hasBottomRadiusXY.value(4.5) & hasBottomRadiusZ.value(0) 
                                & hasConeAngle.value(0) & hasConeDepth.value(0) & hasShapePolygonXY.value(0) 
                                & hasShapePolygonZ.value(0) & hasShapeModel2D.value("circle") & hasShapeModel3D.value("cylinder") 
                                & hasScrewCap.value(False) & hasScrewCapMaterial.value("N/A") & hasScrewCapColor.value("N/A") 
                                & hasColorRGB.value("#FFFFFF") & hasMaterial.value("polystyrene") & hasMass.value(0) 
                                & hasMaxSheerForce.value(0) & hasCoatingMaterial.value("N/A") & hasSetptum.value(False) 
                                & hasSeptumMaterial.value("N/A") & hasSeptumPenetrationForce.value(0) & isLiddable.value(False) & isStackable.value(True) 
                                & isSealable.value(False) & hasManufacturer.value("N/A") & isProductType.value("N/A") & hasModelID.value("N/A") & hasProductID.value("N/A") ]
                
            class SLAS_1_2004_96_Well_Plate(Labware):
                """96 Well Microtiter Plate according to SLAS 4-2004 standard"""
                equivalent_to = [ Labware & hasNumCols.value(12) &  hasNumRows.value(8) & hasNumWells.value(96) 
                                & hasWellVolume.value(100) & hasWellDistRow.value(9) & hasWellDistCol.value(9) 
                                & hasDepthWell.value(14.5) & hasShapeWell.value("round") & hasShapeWellBottom.value("flat") 
                                & hasTopRadiusXY.value(4.5) & hasBottomRadiusXY.value(4.5) & hasBottomRadiusZ.value(0) 
                                & hasConeAngle.value(0) & hasConeDepth.value(0) & hasShapePolygonXY.value(0) 
                                & hasShapePolygonZ.value(0) & hasShapeModel2D.value("circle") & hasShapeModel3D.value("cylinder") 
                                & hasScrewCap.value(False) & hasScrewCapMaterial.value("N/A") & hasScrewCapColor.value("N/A") 
                                & hasColorRGB.value("#FFFFFF") & hasMaterial.value("polystyrene") & hasMass.value(0) 
                                & hasMaxSheerForce.value(0) & hasCoatingMaterial.value("N/A") & hasSetptum.value(False) 
                                & hasSeptumMaterial.value("N/A") & hasSeptumPenetrationForce.value(0) & isLiddable.value(False) & isStackable.value(True) 
                                & isSealable.value(False) & hasManufacturer.value("N/A") & isProductType.value("N/A") & hasModelID.value("N/A") & hasProductID.value("N/A") ]
                
            class SLAS_4_2004_96_Well_Plate(Labware):
                """96 Well Microtiter Plate according to SLAS 4-2004 standard"""
                equivalent_to = [ Labware & hasNumCols.value(12) &  hasNumRows.value(8) & hasNumWells.value(96) 
                                & hasWellVolume.value(100) & hasWellDistRow.value(9) & hasWellDistCol.value(9) 
                                & hasDepthWell.value(14.5) & hasShapeWell.value("round") & hasShapeWellBottom.value("flat") 
                                & hasTopRadiusXY.value(4.5) & hasBottomRadiusXY.value(4.5) & hasBottomRadiusZ.value(0) 
                                & hasConeAngle.value(0) & hasConeDepth.value(0) & hasShapePolygonXY.value(0) 
                                & hasShapePolygonZ.value(0) & hasShapeModel2D.value("circle") & hasShapeModel3D.value("cylinder") 
                                & hasScrewCap.value(False) & hasScrewCapMaterial.value("N/A") & hasScrewCapColor.value("N/A") 
                                & hasColorRGB.value("#FFFFFF") & hasMaterial.value("polystyrene") & hasMass.value(0) 
                                & hasMaxSheerForce.value(0) & hasCoatingMaterial.value("N/A") & hasSetptum.value(False) 
                                & hasSeptumMaterial.value("N/A") & hasSeptumPenetrationForce.value(0) & isLiddable.value(False) & isStackable.value(True) 
                                & isSealable.value(False) & hasManufacturer.value("N/A") & isProductType.value("N/A") & hasModelID.value("N/A") & hasProductID.value("N/A") ]
                
            

            

def parse_command_line():
    """ Looking for command line arguments"""

    description = "oso_data"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("_", nargs="*")

    # ontologie output format

    parser.add_argument('-p', '--path', type=str, default='.',
                        help='output path (default: ".")')

    parser.add_argument('-f', '--format', type=str, default='turtle',
                        help='output format (default: turtle)')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    # add more arguments here

    return parser.parse_args()
            
def main():
    """Console script for oso_data."""
        # or use logging.INFO (=20) or logging.ERROR (=30) for less output
    logging.basicConfig(
        format='%(levelname)-4s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)
    
    
    args = parse_command_line()
        
    if len(sys.argv) <= 2:
        logging.debug("no arguments provided !")
        return -1

    print("Arguments: " + str(args._))
    
    logger = logging.getLogger(__name__)

    EMMO_url = "https://emmo-repo.github.io/versions/1.0.0-beta5/emmo-inferred.ttl"
    

    # loading EMMO ontology
    emmo_world = World()

    emmo_filename = os.getenv("EMMO_FILENAME", default=EMMO_url)
        
    print("==== emmo env set to: ", emmo_filename )

    if emmo_filename is not None:
        emmo = emmo_world.get_ontology(emmo_filename)    
    
    emmo.load()               # reload_if_newer = True
    emmo.sync_python_names()  # synchronize annotations
    #self.emmo.base_iri = self.emmo.base_iri.rstrip('/#')
    #self.catalog_mappings = {self.emmo.base_iri: emmo_url}

    lolw_tbox = LOLabwareTBox( emmo_url = EMMO_url,
                            emmo_world=emmo_world,
                            emmo=emmo)

    if args.path and args.format:
        lolw_tbox.export(path=args.path, format=args.format)

        logger.info("LOLW instance created")

        return 0


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
