# MEMORY STRESS TEST

## Description
A Python script to reserve and stress system memory resources from Linux machines.

This script reserves system resources using Linux Kernel cgroups: 
https://en.wikipedia.org/wiki/Cgroups, http://man7.org/linux/man-pages/man7/cgroups.7.html 

There exist a convenience python module called cgroups to simplify the operations of 
having to walk through and manipulate the /proc directory files directly.

On memory stats and profiling, psutils and memory_profiler module are main helpers here.

Last but not least, memory allocation is simulated through a dummy buffer implemented as a python list.

## Requirements
Linux and basic Python installation, included pip for install required modules, 
it works in local and virtual environments, tested over Python 2.7 and Python 3.6 branches.

## Requirements and notes on cgroups ( from cgroups package README.md ):
https://github.com/francisbouvier/cgroups/blob/master/README.md

Root and non-root usage

To use cgroups the current user has to have root privileges OR existing cgroups sub-directories.

In order to create those cgroups sub-directories you use the user_cgroups command as root.
```
sudo user_cgroups USER
```
N.B.: This will only give the user permissions to manage cgroups in his or her own sub-directories and process. It will not give the user permissions on other cgroups, process, or system commands.

N.B.: You only need to execute this script once.

## Installation
```
git clone this repository
pip install -r requirements.txt
```

### Usage
```
python memory-stress-test -m [% of the reserved memory to be consumed ]
```

### Useful references
```
CGROUPS Python Module
https://github.com/francisbouvier/cgroups

CGROUPS-UTILS Python Module and Library
https://github.com/peo3/cgroup-utils

PSUTILS
https://psutil.readthedocs.io/en/latest/

MEMORY-PROFILER
https://pypi.org/project/memory-profiler/
```

### To do's
- Research Python types, objects and runtime sizes to a more accurate simulation of the amount of memory used by the process.
- PSUtils looks like the go to package for OS resources statistics. Get better confidences come from, how accurate measurements are.
- cgroups API, correlation with the Linux OS memory management sub system for better fine tuning and granularity of the simulation.
