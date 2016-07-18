#*******************************************************************************
 #
 #  Filename    : logformat.py
 #  Description : Log format for of a single dataset
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
 # The log format should be in the following format:
 # [CRAB TIMESTAMP]
 # [ROOTFILE_REMOTE_ABS] [TIMESTAMP OF FILE] [SIZE_AT_REMOTE]
 # [ROOTFILE_REMOTE_ABS] [TIMESTAMP OF FILE] [SIZE_AT_REMOTE]
 # [ROOTFILE_REMOTE_ABS] [TIMESTAMP OF FILE] [SIZE_AT_REMOTE]
 # ...
#*******************************************************************************

class LogTable(object):

    def __init__(self, filename=None):
        self.timestamp = "" ## Creating null time stamp
        self.entrylist = {} ## Creating empty table
        if filename:
            self.load(filename)

    def load(self,filename):
        lines = [line.rstrip('\n') for line in open(filename) ]
        self.timestamp = lines[0]
        for entryline in lines[1:]:
            remotepath, timestamp, remotesize = entryline.split()
            self.entrylist[remotepath] = (timestamp, remotesize)

    def write(self,filename):
        logfile = open(filename,'w')
        logfile.write( self.timestamp + '\n' )
        for remotepath, (timestamp,remotesize) in self.entrylist.iteritems():
            logfile.write( "{} {} {}\n".format( remotepath, timestamp, remotesize) )

    def dump(self):
        print self.timestamp
        for remotepath, (timestamp,remotesize) in self.entrylist.iteritems():
            print "{} {} {}".format( remotepath, timestamp,remotesize )

    def setentry(self,remotepath,timestamp,remotesize):
        self.entrylist[remotepath] = (timestamp,remotesize)

    def getfiletime(self,remotepath):
        return self.entrylist[remotepath][0]

    def getfilesize(self,remotepath):
        return self.entrylist[remotepath][1]


if __name__ == "__main__":
    mytable = LogTable("testlog.test" )
    mytable.dump()
    mytable.write("testlog_out.txt")
