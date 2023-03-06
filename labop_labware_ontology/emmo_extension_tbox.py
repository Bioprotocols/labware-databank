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


class EMMOTBox:
    def __init__(self, emmo_world=None) -> None:

        self.labop_labware_base_iri = 'http://www.labop.org/labware'
        self.labop_labware_version_iri = f'http://www.labop.org/{__version__}/labware'

        output_filename_base = os.path.join('labop_labware_tbox')
        self.labop_labware_owl_filename = f'{output_filename_base}-v{__version__}.owl'
        self.labop_labware_ttl_filename = f'{output_filename_base}-v{__version__}.ttl'

        # TODO: use main EMMO ontology :  https://raw.githubusercontent.com/emmo-repo/EMMO/master/emmo-inferred.ttl
        # alternative url   "https://raw.githubusercontent.com/emmo-repo/EMMO/master/self.emmo.ttl"

        self.emmo_url = (
            'https://raw.githubusercontent.com/emmo-repo/emmo-repo.github.io/'
            'master/versions/1.0.0-beta/emmo-inferred-chemistry2.ttl')

        self.emmo_url_local = os.path.join(pathlib.Path(
            __file__).parent.resolve(), "emmo", "emmo-inferred-chemistry2")

        if os.path.isfile(self.emmo_url_local + '.ttl'):
            self.emmo_url = self.emmo_url_local

        #self.emmo_world = World(filename="emmo_labware.sqlite3")
        if emmo_world is not None:
            self.emmo_world = emmo_world
        else:
            self.emmo_world = World()
            # self.emmo_world.onto_path.append("../emmo")

            self.emmo = self.emmo_world.get_ontology(self.emmo_url)
            self.emmo.load()  # reload_if_newer = True
            self.emmo.sync_python_names()  # Synchronize annotations
            self.emmo.base_iri = self.emmo.base_iri.rstrip('/#')
            self.catalog_mappings = {self.emmo.base_iri: self.emmo_url}

                # Create new ontology: labOP-labware - lolw
        self.lolw = self.emmo_world.get_ontology(self.labop_labware_base_iri)
        if emmo_world is None:
            self.lolw.imported_ontologies.append(self.emmo)
        self.lolw.sync_python_names()

    # defining the  labOP-labware ontology
    def define_ontology(self):
        logging.debug('defining labware ontology')

        with self.lolw:

            # Terminology Component (TBox) 

            # Basic Relations
            # ================

            class hasType(self.lolw.hasConvention):
                """Associates a type (string, number...) to a property."""

            class isTypeOf(self.lolw.hasConvention):
                """Associates a property to a type (string, number...)."""
                inverse_property = hasType

            # TODO: shall be moved to EMMO extension module

            # Physical Properties
            # ====================

            class Length(self.emmo.Length):
                """"Length
                extends EMMO:Length
                """
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Length")

                # add reference SI unit
                referenceUnit = self.emmo.Metre

                length = 0.0

            class Volume(self.emmo.Volume):
                """Volume
                extends EMMO:Volume """
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Volume")

                # add reference SI unit
                referenceUnit = self.emmo.CubicMetre

            class Mass(self.emmo.Mass):
                """Mass 
                extends EMMO:Mass """
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Mass")

                # add reference SI unit
                referenceUnit = self.emmo.Kilogram

            class MolecularWeight:
                """Molecular Weight
                extends EMMO: """
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Molecular_weight")

                # add reference SI unit
                #referenceUnit = self.emmo.KilogramPerMole

            class Density(self.emmo.Density):
                """Density 
                extends EMMO:Density """
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Density")

                # add reference SI unit
                #referenceUnit = self.emmo.KilogramPerCubicMetre

            class Force(self.emmo.Force):
                """Force of a labware, e.g. for screw caps""" 
                # add quantity“Scoping:
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Force")

                # reference SI unit
                referenceUnit = self.emmo.Newton

            class Torque(self.emmo.Torque):
                """Torque of a labware, e.g. for screw caps""" 
                # add quantity“Scoping:
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Torque")

                # reference SI unit
                referenceUnit = self.emmo.NewtonMetre

            class Viscosity:
                """Viscosity of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Viscosity")

                #referenceUnit = self.emmo.PascalSecond

            class SurfaceTension(self.emmo.Force):
                """Surface Tension of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Surface_tension")

                #referenceUnit = self.emmo.NewtonPerMetre
                # 
                
            class ThermalConductivity:
                """Thermal Conductivity of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Thermal_conductivity")


            class ElectricConductance(self.emmo.ElectricConductance):
                """Electric Conductance of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Electric_conductivity")


                #referenceUnit = self.emmo.SiemensPerMetre

            class TensileStrength(self.emmo.Force):
                """Tensile Strength of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Tensile_strength")

                #referenceUnit = self.emmo.NewtonPerSquareMetre

            class ImpactStrength(self.emmo.Energy):
                """Impact Strength of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Impact_strength")

                #referenceUnit = self.emmo.JoulePerSquareMetre

            class Hardness:
                """Hardness of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Hardness")

                #referenceUnit = self.emmo.ShoreD

            class ModulusOfElasticity(self.emmo.Force):
                """Modulus of Elasticity of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Modulus_of_elasticity")

                #referenceUnit = self.emmo.NewtonPerSquareMetre

            class MeltingPoint(self.emmo.ThermodynamicTemperature):
                """Melting Point of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Melting_point")

                referenceUnit = self.emmo.Kelvin

            class BoilingPoint(self.emmo.ThermodynamicTemperature):
                """Boiling Point of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Boiling_point")

                referenceUnit = self.emmo.Kelvin

            class FlashPoint(self.emmo.ThermodynamicTemperature):
                """Flash Point of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Flash_point")

                referenceUnit = self.emmo.Kelvin

            # optical properties
            
            class RefractiveIndex:
                """Refractive Index of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Refractive_index")

            
            class ColorCMYK:
                """Color in CMYK color model format."""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/CMYK_color_model")

            class AbsorptionSpectrum:
                """Absorption Spectrum of a substance"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Absorption_spectrum")

                
            # AllDisjoint([Length, Volume, Mass, Force, Torque, Density, 
            #             Viscosity, SurfaceTension, ThermalConductivity, ElectricConductance, TensileStrength, 
            #             ImpactStrength, Hardness, ModulusOfElasticity, MeltingPoint, BoilingPoint, FlashPoint, 
            #             RefractiveIndex, AbsorptionSpectrum])

            # substance extension of EMMO 

            class Substance(self.emmo.ChemicalSubstance):
                """Polymer, properties, like solvent tolerance, transparency, ...."""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Substance")

                molecularWeight = MolecularWeight()
                density = Density()
                meltingPoint = MeltingPoint()
                boilingPoint = BoilingPoint()
                flashPoint = FlashPoint()

                # pyhsical properties
                viscosity = Viscosity()
                surfaceTension = SurfaceTension()
                thermalConductivity = ThermalConductivity()
                electricConductance = ElectricConductance()
                tensileStrength = TensileStrength()
                impactStrength = ImpactStrength()
                hardness = Hardness()
                modulusOfElasticity = ModulusOfElasticity()
                
                # optical properties
                refractiveIndex = RefractiveIndex()
                colorCMYK = ColorCMYK()
                absorptionSpectrum = AbsorptionSpectrum()

           
          
                

            



            
