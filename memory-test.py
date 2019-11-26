#
# memory-test
# created date: 23/11/2019
# name: Emilio Coronado
# Basic script that reserves a % of memory from the system and then allocates 
# a % of reserved memory to simulate large memory usage and constraints
#
import os
import time
import sys
import psutil
import argparse
from cgroups import Cgroup
from memory_profiler import profile
from psutil._common import bytes2human

MEGABYTE = 1024 * 1024

def memory_calculate(reserve_pct, consume_pct):
    # From % to MB
    total_memory = psutil.virtual_memory().total / MEGABYTE
    reserve_mbytes = (total_memory * reserve_pct) / 100
    consume_mbytes = (reserve_mbytes * consume_pct) / 100
    return reserve_mbytes, consume_mbytes

def memory_reserve(mbytes):
    # http://man7.org/linux/man-pages/man7/cgroups.7.html
    # system memory to be reserved to the script
    cg = Cgroup('my-container')
    cg.set_memory_limit(mbytes)
    cg.add(os.getpid()) 

def memory_fill(mbytes):
    # consume: MB of reserved memory
    dummy_buffer = []
    dummy_buffer = ['A' * MEGABYTE for _ in range(0, int(mbytes))]
    return dummy_buffer

def memory_info():
    # Pretty print the tuple returned in psutil.virtual_memory()
    nt = psutil.virtual_memory()
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value)
        print('%-10s : %7s' % (name.capitalize(), value))

# Check differences in memory usage using the memory profiler
@profile
def memory_check():
    pass

def main():
    # Parsing arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", required=True, type=int, help="Percentage of system reserved memory used by the script")
    args = ap.parse_args()
    consume_pct = args.m
    reserve_pct = 80 

    # Check available memory    
    memory_info()
    
    # Calculate the amount of RAM in MB to reserve and consume from percentage
    reserve_mbytes, consume_mbytes = memory_calculate(reserve_pct, consume_pct)
    print('RESERVED MB:', int(reserve_mbytes))
    print('CONSUMED MB:', int(consume_mbytes))

    # Reserve system memory
    memory_reserve(reserve_mbytes)

    # Simulate memory usage, allocating from reserved memory
    data = memory_fill(consume_mbytes)

    # Check memory has taken from right places
    memory_check()
    memory_info()

    # Wait for the killing signal
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
