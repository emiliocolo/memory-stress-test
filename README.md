# Memory Stress Test

### Description
A Python script to reserve and stress system memory resources from Linux machines.

This script reserves system resources using Linux Kernel cgroups https://en.wikipedia.org/wiki/Cgroups, 
http://man7.org/linux/man-pages/man7/cgroups.7.html through cgroups convenience python module that simplifies 
the operations of having to walk through and manipulate the file system directly.

It also uses the PSUTILS module to get system memory stats and a MEMORY_PROFILER module to check the simulated memory
allocated by a dummy buffer.

### Requirements
Linux and basic Python installation, included pip for install required modules, 
it works in local and virtual environments, tested over Python 2.7 and Python 3.6 branches.

### Requirements Notes on cgroups ( from cgroups package README.md ):
https://github.com/francisbouvier/cgroups/blob/master/README.md

Root and non-root usage

To use cgroups the current user has to have root privileges OR existing cgroups sub-directories.

In order to create those cgroups sub-directories you use the user_cgroups command as root.

sudo user_cgroups USER

N.B.: This will only give the user permissions to manage cgroups in his or her own sub-directories and process. It wiil not give the user permissions on other cgroups, process, or system commands.

N.B.: You only need to execute this script once.

### Installation
git clone this repository

pip install -r requirements.txt

### Usage
python memory-stress-test -m [% of the reserved memory to be consumed ]

### Useful References
CGROUPS Python Module
https://github.com/francisbouvier/cgroups

CGROUPS-UTILS Python Module and Library
https://github.com/peo3/cgroup-utils

PSUTILS
https://psutil.readthedocs.io/en/latest/

### MEMORY-PROFILER
https://pypi.org/project/memory-profiler/
