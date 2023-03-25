#!/usr/bin/env python3
# vim:fileencoding=utf-8
"""_____________________________________________________________________

:PROJECT: LabOP Labware Ontology

* Main module command line interface *

:details:  Main module command line interface. 
           !!! Warning: it should have a diffent name than the package name.

.. note:: -
.. todo:: - 
________________________________________________________________________
"""

"""Main module implementation. !!! Warning: it should have a diffent name than the package name. """
"""Console script for labop_labware_ontology."""

import argparse
import sys
import logging
from labop_labware_ontology import __version__

from labop_labware_ontology.labop_labware_ontology_impl import LabwareInterface

logging.basicConfig(
    format="%(levelname)-4s| %(module)s.%(funcName)s: %(message)s",
    level=logging.DEBUG,
)    

def parse_command_line():
    """ Looking for command line arguments"""

    description = "labop_labware_ontology"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("_", nargs="*")

    parser.add_argument(
        "-i", "--import-csv", action="store", default="labware_catalogue.csv", help="import labware csv catalogue file"
    )

    parser.add_argument(
        "-p", "--output-path", action="store", help="save all labware ontologies in the given output path"
    )

    parser.add_argument(
        "-f", "--output-format", action="store", help="save all labware ontologies in the given format [turtle, owl, rdf, xml, n3, nt, json-ld]"
    )

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    # add more arguments here

    return parser.parse_args()

def main():
    """Console script for labop_labware_ontology."""
        # or use logging.INFO (=20) or logging.ERROR (=30) for less output
    logging.basicConfig(
        format='%(levelname)-4s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)
    
    
    args = parse_command_line()
        
    if len(sys.argv) <= 2:
        logging.debug("no arguments provided !")


    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into labop_labware_ontology.__main__")
    
    lolw = LabwareInterface()
    if args.output_format:
        lolw.export_ontologies(csv_filename=args.import_csv, path=args.output_path, format=args.output_format)
    #logging.debug(greeting)
    
    return 0


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
