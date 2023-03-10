# python module that defines an ontology of common labware classes that are used in a scientific lab, based on EMMOntoPy
# it should be possible to use this ontology to automatically get the right SI units for the properties of the labware
# and to automatically get the right EMMO classes for the labware
# as much as possible, the ontology should be based on EMMO, but it may be necessary to add some classes and properties
# that are not in EMMO
# as much as possible should be inferred from EMMO, but it may be necessary to add some axioms
# the ontology should be able to be used in a lab notebook, and should be able to be used to automatically generate
# a labware inventory
# the ontology should be able to be used to automatically generate a labware database


import os
import pathlib
import logging

from ontopy import World
from ontopy.utils import write_catalog

import owlready2
from owlready2 import DatatypeProperty, FunctionalProperty, ObjectProperty, AllDisjoint

from labop_labware_ontology.__init__ import __version__  # Version of this ontology


# --- ontology definition helper functions

def en(s):
    """Returns `s` as an English location string."""
    return owlready2.locstr(s, lang='en')


def pl(s):
    """Returns `s` as a plain literal string."""
    return owlready2.locstr(s, lang='')


class LOLabwareTBox:
    def __init__(self, emmo=None, lolw=None) -> None:


        self.emmo = emmo
        self.lolw = lolw

        # --- ontology definition

        # define the ontology
        self.define_ontology()

    # defining the  labOP-labware ontology
    def define_ontology(self):
        logging.debug('defining labware ontology')

        with self.lolw:

            # Terminology Components (TBox) 


            # labware visual representation
            
            class ModelIcon:
                """Icon of the labware in X format. SVG ?"""
            

            class Model2D:
                """2D model of the labware in X format. SVG ?"""

            class Model3D:
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
            
            class ShapeWell:
                """Well overall / top well shape,e.g. round, square, buffeled,..."""
            
            class ShapeWellBottom:
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

            class ShapePolygonXY:
                """Generalized shape polygon for more complex well shapes, in xy plane / direction."""

            class ShapePolygonZ:
                """Generalized shape polygon for more complex well shapes, in z direction = rotation axis."""

            class ShapeModel2D:
                """2D model of Well shape"""

            class ShapeModel3D:
                """3D model of Well shape"""

            class FirstInteractionPosition(self.emmo.Vector):
                """Position of first interaction point of a pipette tip with a well or a needle with a septum, rel. to the upper left corner of the labware. - what about round labware?"""


            #AllDisjoint([DepthWell, ShapeWell, ShapeWellBottom, TopRadiusXY, BottomRadiusXY, BottomRadiusZ, ConeAngle, ConeDepth, ShapePolygonXY, ShapePolygonZ, ShapeModel2D, ShapeModel3D, FirstInteractionPosition])


            # Labware Vendor related properties
            # =================================

            class Vendor:
                """Labware Vendor"""

            class VendorProductNumber:
                """Labware Vendor Product Number"""

            # UNSPSC
            class UNSPSC:
                """United Nations Standard Products and Services Code (UNSPSC) for labware"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/UNSPSC")

            # eCl@ss
            class EClass:
                """eCl@ss for labware"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/EClass")


            # Labware Classes
            # ====================

            # Basic ------

            class Labware(self.lolw.Device):
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
                

            class hasLengthTolerance(self.emmo.Length >> float, FunctionalProperty, DatatypeProperty):
                """Labware relative length tolerance (= measured width/target width)."""
            
            class hasWidth(Labware >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Labware total width, without  any additions, like lids etc."""
            
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

            
            class hasColor(Labware >> str, FunctionalProperty):
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

            class hasManifacturer(Labware >> str, FunctionalProperty):
                 """Name of the Manufacturer """
            
            class isProductType(Labware >> str, FunctionalProperty):
                """Labware product Type"""

            class hasModelNumber(Labware >> str, FunctionalProperty):
                """Labware model number"""

            class hasProductNumber(Labware >> str, FunctionalProperty):
                """Manufacturer Product Number of the Labware"""

            class hasWellVolume(Labware >> float, FunctionalProperty):
                """Total Labware volume """

            class hasWellDistRow(Labware >> float, FunctionalProperty):
                """wWll-to-well distance in row direction"""
            
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

            class hasShapeModel2D(Labware >> str, FunctionalProperty):
                """2D model of Well shape"""

            class hasShapeModel3D(Labware >> str, FunctionalProperty):
                """3D model of Well shape"""

            # labware with screw cap

            class hasScrewCap(Labware >> bool, FunctionalProperty):
                """Screw cap type"""

            class hasScrewCapMaterial(Labware >> str, FunctionalProperty):
                """Screw cap material"""
            
            class hasScrewCapColor(Labware >> str, FunctionalProperty):
                """Screw cap color"""


            # labware with snap cap


            
            # further properties:

            # lengthAtEdge, lengthOverall, isSLAS1-2004complian

            # isSLAS1-2004compliant

            

            # all disjoined properties

            # special labware classes
            # can be used for faster type testing
            # ===================================================

            class SLAS_4_2004_96_Well_Plate(Labware):
                """96 Well Microtiter Plate according to SLAS 4-2004 standard"""
                equivalent_to = [ Labware & hasNumCols.value(12) &  hasNumRows.value(8) & hasNumWells.value(96) 
                                & hasWellVolume.value(100) & hasWellDistRow.value(9) & hasWellDistCol.value(9) 
                                & hasDepthWell.value(14.5) & hasShapeWell.value("round") & hasShapeWellBottom.value("flat") 
                                & hasTopRadiusXY.value(4.5) & hasBottomRadiusXY.value(4.5) & hasBottomRadiusZ.value(0) 
                                & hasConeAngle.value(0) & hasConeDepth.value(0) & hasShapePolygonXY.value(0) 
                                & hasShapePolygonZ.value(0) & hasShapeModel2D.value("circle") & hasShapeModel3D.value("cylinder") 
                                & hasScrewCap.value(False) & hasScrewCapMaterial.value("N/A") & hasScrewCapColor.value("N/A") 
                                & hasColor.value("#FFFFFF") & hasMaterial.value("polystyrene") & hasMass.value(0) 
                                & hasMaxSheerForce.value(0) & hasCoatingMaterial.value("N/A") & hasSetptum.value(False) 
                                & hasSeptumMaterial.value("N/A") & hasSeptumPenetrationForce.value(0) & isLiddable.value(False) & isStackable.value(True) 
                                & isSealable.value(False) & hasManifacturer.value("N/A") & isProductType.value("N/A") & hasModelNumber.value("N/A") & hasProductNumber.value("N/A") ]
                
            

            

                

            



            
