#!/usr/bin/env python
#*******************************************************************************
 #
 #  Filename    : retrievecrab.py
 #  Description : High level function for retrieving file sof a singel crab job
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
#*******************************************************************************

import sys
import argparse
import src.crablogger as cl ## Loading custom package
import src.versioncheck as vc

def retrievecrab(argv=sys.argv):

    ## Run version check before anything
    vc.CheckVersionReq()

    parser = argparse.ArgumentParser("Options for retrieving crab file")
    parser.add_argument("-s","--site"   ,
        help="Site of where the output is stored",
        type=str, default='eoscms.cern.ch', )
    parser.add_argument("-d","--dirfln" ,
        help="The path specified in the crab config file",
        type=str, required=True)
    parser.add_argument("-p","--primary",
        help="Name of the primary dataset (first entry in DAS query)",
        type=str, required=True)
    parser.add_argument("-c","--crabjob",
        help="Name of crab jobs as defined in crab configuration file",
        type=str, required=True)
    parser.add_argument("-o","--output" ,
        help="Output directory, default to be present working directory",
        type=str, default="./", )
    parser.add_argument("-r","--refresh",
        help="Generate new log file",
        action="store_true", )

    try:
        arg = parser.parse_args( argv[1:] )
    except:
        parser.print_help()
        raise

    logger = cl.CrabLogger( arg.site, arg.dirfln, arg.primary, arg.crabjob, arg.output )

    logger.getoutput(arg.refresh)

    return 0


if __name__ == "__main__":
    sys.exit(retrievecrab())
