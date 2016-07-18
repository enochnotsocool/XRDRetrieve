#!/usr/bin/env python
#*******************************************************************************
 #
 #  Filename    : retrievecrab.py
 #  Description : High level function for retrieving file sof a singel crab job
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
#*******************************************************************************

import sys
import optparse
import src.crablogger as cl ## Loading custom package

def retrievecrab(argv=sys.argv):
    parser = optparse.OptionParser("Options for retrieving crab file")
    parser.add_option("-s","--site"   , dest="site"   , help="Site of where the output is stored",                      type='string' )
    parser.add_option("-d","--dirfln" , dest="dirfln" , help="The path specified in the crab config file",              type='string' )
    parser.add_option("-p","--primary", dest="primary", help="Name of the primary dataset (first entry in DAS query)",  type='string' )
    parser.add_option("-c","--crabjob", dest="crabjob", help="Name of crab jobs as defined in crab configuration file", type='string' )
    parser.add_option("-o","--output" , dest="output" , help="Output directory, defaulted to be the this directory",    type='string', default="./" )
    parser.add_option("-r","--refresh", dest="refresh", help="Generate new log file", action="store_true" )

    opt, args = parser.parse_args( argv )

    if not opt.site or not opt.dirfln or not opt.primary or not opt.crabjob:
        print "Error! Option is not specified!\n"
        parser.print_help()
        return 1

    logger = cl.CrabLogger( opt.site, opt.dirfln, opt.primary, opt.crabjob, opt.output )

    logger.getoutput(opt.refresh)

    return 0




if __name__ == "__main__":
    sys.exit(retrievecrab())
