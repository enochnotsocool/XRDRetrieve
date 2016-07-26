# XRDRetrieve

`XRDRetrieve` is a package aimed to help in the retrieval of [crab jobs](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrab), assuming you only have knowledge of how the [crab configuration file](https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile) is setup. The input options are:

* `-h, --help`: Display options
* `-s, --site`: Site of where the output is stored, this is **NOT** the same as the site you put in your crab file, but rather the url of the site, (T2_CH_CERN would correspond to `eoscms.cern.ch`)
* `-d, --dirfln`:  The directory you put in your crab configuration file.
* `-p, --primary`: The primary tag of the data you are processing, for instance `/SingleMuon/Run2016B-Promptreco-v2/MINIAOD` would be `SingleMuon`
* `-c, --crabjob`: The `requestName` entry in you crab configuration
* `-o, --output`: Where to store the retrieved files. For the a given input `/some/path`, the root files would be stored in `/some/path/<crabjob>`
* `-r, --refresh`: Boolean flag to reprocess *log file*

In the case the file retrieval process fails, of if there is a update from a re-ran job, the fore-mentioned log file keeps track of which files have are up to date and do not require downloading. The `--refresh` flag, tells the program to regenerate a log file by crawling the filesystem of the remote server again. Regardless of whether this flag is placed, on the first run there will always be a crawl.

### Requirements

* [python 2.7](https://www.python.org/download/releases/2.7/)
* [`xrdfs 4.2`](http://xrootd.org/doc/man/xrdfs.1.html) command line utilities

Please note that any xrdfs commands should be able to run without user-interaction. If you need to setup certificate proxies, please do it before running the scripts.


### Design mentalities

After given a base storage directory, a request name, crab will store the output root files in this directory:
```
/<base path>/<primary tag>/crab_<request name>/<timestamp>/0000/<yourfile>.root
```
The time stamp is a unique marker for when the crab file was submitted. When generating our local log file or the first time, we crawl the remote file system to get the following information

* The root files under the directory **with the latest time stamp**
* The size and modification time of each root file

When determining which files should be downloaded, the program checks if:

* If the local version of the file exists. If not then download
* If the local version of the file has exactly the same size as remote counter part.

With the refresh option, we also check our existing log file with one freshly generated:

* If the new log file contains a file not listed in the original, download said file
* If a file's time stamp or size is different between the two log files, download said file
