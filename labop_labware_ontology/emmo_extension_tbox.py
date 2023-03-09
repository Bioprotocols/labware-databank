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


class EMMOExtensionTBox:
    def __init__(self, emmo_ontology=None) -> None:

      
        self.emmo = emmo_ontology

        # --- ontology definition

        # define the ontology
        self.define_ontology()

        

    # defining the  labOP-labware ontology
    def define_ontology(self):
        logging.debug('defining labware ontology')

        with self.emmo:

            # Terminology Component (TBox) 


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

           
          
                

            



            
