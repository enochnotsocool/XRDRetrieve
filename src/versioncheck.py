#*******************************************************************************
 #
 #  Filename    : versioncheck.py
 #  Description : Functions for detecting require tool version
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
#*******************************************************************************

from distutils.version import LooseVersion
import sys
import subprocess

python_version_min = (2,7)
python_version_max = (3,0)
xrdfs_version_min = "4.2.1"

def CheckVersionReq():

    requirements="""
    Requirements:
      - python{0}
      - xrdfs > {1}
    """.format(
        ".".join( str(x) for  x in python_version_min ) ,
        xrdfs_version_min
    )
    pyversion_str = [ str(x) for x in sys.version_info ]
    pyversion_str = '.'.join( pyversion_str )

    if sys.version_info >= python_version_max:
        print "Your python is too new! ", pyversion_str
        print requirements
        raise Exception("Version Error")
    if sys.version_info <  python_version_min:
        print "Your python is too old! ", pyversion_str
        print requirements
        raise Exception("Version Error")

    proc = subprocess.Popen(
        ["xrdcp", "--version" ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, xrdversion = proc.communicate()

    if xrdversion.startswith('v'):
        xrdversion = xrdversion.strip("v")
    if LooseVersion(xrdversion) < LooseVersion(xrdfs_version_min):
        print "You xrdfs is too old!", xrdversion
        print requirements
        raise Exception("Version Error")



if __name__ == "__main__" :
    CheckVersionReq()
