#*******************************************************************************
 #
 #  Filename    : crablogger.py
 #  Description : class for managing crab outputfile logging
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
#*******************************************************************************
import sys, os
import subprocess
import fnmatch
import logformat
from   datetime import datetime
import time

class CrabLogger(object):

    def __init__(self, site, dirfln, primary, crabjob, output):
        self.site        = site
        self.dirfln      = dirfln
        self.primary     = primary
        self.crabjob     = crabjob
        self.output      = output + '/' + crabjob
        self.timestamp   = None
        self.localtable  = logformat.LogTable()
        self.remotetable = None

        ## Testing if crab
        print ">> Begin Initizalizing..."
        if not self.checkremotedir():
            raise Exception('requested crab job path not found at remote location')

        if not self.checklocaldir():
            raise Exception('Error in specifying output!')
        print ">> Finished Initizalizing!"

    def getoutput(self, compare_with_remote=False):
        print ">> Starting comparing...."
        retrievelist = []

        if os.path.isfile( self.logfilename() ):
            self.localtable.load( self.logfilename()  )
        else:
            self.make_remotetable()
            self.localtable = self.remotetable
            self.localtable.write( self.logfilename() )

        if compare_with_remote and not self.remotetable:
            self.make_remotetable()
            retrievelist.extend( self.compare_remote() )
            self.localtable.write( self.logfilename() )

        retrievelist.extend( self.compare_local()  )
        retrievelist = sorted(set( retrievelist )) ## Unique elements only

        if len(retrievelist) == 0 :
            print ">> Everything done! Nothing to retrieve!"
            return

        for remotefile in retrievelist:
            print ">> Start retrieving...."
            self.retrievesingle(remotefile)


    def checkremotedir(self):
        out  = self.listremote(self.remotecrabbase())
        for outline in out:
            outline = os.path.basename( outline )
            if outline > self.timestamp :
                self.timestamp = outline
        return True

    def checklocaldir(self):
        if os.path.isdir(self.output):
            print "Using existing directory..."
            return True
        if not os.path.exists(self.output):
            print "Creating new directory!"
            os.system("mkdir -p " + self.output)
            return True
        elif op.path.isfile(self.output):
            print "Error! output already exsits as a file!"
            return False
        return False


    def remotecrabbase(self):
        return "{}/{}/crab_{}/".format( self.dirfln, self.primary, self.crabjob )

    def logfilename(self):
        return self.output + "/log.txt"

    def make_remotetable(self):
        print "Generating table from remote location, might take some time..."
        self.remotetable = logformat.LogTable() ## scraping everything
        self.remotetable.timestamp = self.timestamp

        for midpath in self.listremote( self.remotecrabbase() + self.timestamp ):
            for rootfile in  fnmatch.filter( self.listremote( midpath ) , '*.root' ):
                path = rootfile
                timestamp,size = self.getfileinfo( rootfile )
                self.remotetable.setentry( path, timestamp, size )

    def listremote(self,query):
        """Using xrdfs ls"""
        proc = subprocess.Popen(["xrdfs", self.site, "ls", query ], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        out, err = proc.communicate()
        if err :
            print "Error detected when calling xrdfs!"
            print "Have you setup your permission? (voms-proxy-init -voms cms -valid 192:0)"
            print "Full command >> xrdfs", self.site, "ls", query
            raise Exception("Error in input!")
        return out.split()

    def getfileinfo(self, remotefile):
        """
        Using xrdfs stat command
        Output of the command is in the format of:
        > Path:   <somepath>
        > Id:     <someid>
        > Size:   <some size in bytes>
        > MTime:  <time in the format: 2016-07-10 23:52:41>
        > Flags:  <some flag>16 (IsReadable)
        """
        proc = subprocess.Popen(["xrdfs", self.site, "stat", remotefile ], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        out,err = proc.communicate()
        out      = out.split('\n')
        size_line = out[2]
        time_line = out[3]
        size = size_line.split()[1].strip()
        time_inputstring = time_line.split(': ')[1].strip()
        time_obj = datetime.strptime( time_inputstring , "%Y-%m-%d %H:%M:%S")
        time_outputstring = time_obj.strftime("%y%m%d_%H%M%S" )
        return time_outputstring, size

    def compare_local(self):
        filelist = []
        for remotepath,pair in self.localtable.entrylist.iteritems() :
            localpath = self.output + '/' + os.path.basename(remotepath)
            if not os.path.isfile( localpath ):
                print "Adding missing file ", os.path.basename(remotepath)
                filelist.append( remotepath )
            else:
                remotesize = pair[1]
                localsize  = str(os.path.getsize(localpath))
                if localsize != remotesize:
                    print "Adding mismatch file ", os.path.basename(remotepath),
                    print "(local:{}/remote:{})".format( localsize , remotesize )
                    filelist.append( remotepath )
        return filelist

    def compare_remote(self):
        filelist = []

        ## Force refresh everything if new tame stamp is detected
        if self.remotetable.timestamp != self.localtable.timestamp :
            print "Remote has a different time stamp! Dropping everything in local log..."
            self.localtable = self.remotetable
            filelist = [x for x in self.localtable.entrylist ]
            return filelist

        for remotepath in self.remotetable.entrylist :
            remotetime = self.remotetable.getfiletime( remotepath )
            remotesize = self.remotetable.getfilesize( remotepath )
            if remotepath not in self.localtable.entrylist:
                print "Adding remote's new file", os.path.basename(remotepath)
                filelist.append(remotepath)
                self.localtable.setentry( remotepath, remotetime, remotesize )
            elif remotetime != self.localtable.getfiletime(remotepath):
                print "Adding remote's updated file", os.path.basename(remotepath)
                filelist.append(remotepath)
                self.localtable.setentry( remotepath, remotetime, remotesize )
            elif remotesize != self.localtable.getfilesize(remotepath):
                print "Adding remote's updated file", os.path.basename(remotepath)
                filelist.append(remotepath)
                self.localtable.setentry( remotepath, remotetime, remotesize )

        return filelist


    def retrievesingle(self,remotepath):
        cmd = "xrdcp -f root://{0}//{1} {2}/{3}".format(
            self.site,
            remotepath,
            self.output,
            os.path.basename(remotepath)
        )
        print "Retrieving file ", os.path.basename(remotepath)
        print cmd
        os.system(cmd)




if __name__ == "__main__":
    mylogger = CrabLogger(
            'eoscms.cern.ch',
            '/store/group/phys_b2g/BprimeKit_Ntuples_CMSSW_80X/',
            'SingleElectron',
            'BPK_80X_SingleElectron_Run2016B-PromptReco-v2',
            '/store/yichen/bpk_ntuples/80X/'
            )
    mylogger.getoutput()
