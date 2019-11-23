#
# memory-test
# created date: 23/11/2019
# name: Emilio Coronado
# description: a basic script that reserves a % of memory from the system and then allocates a % of that reserved memory to simulate large memory usage and constraints
#
import os
import time
import sys
import psutil
import argparse
from cgroups import Cgroup
from memory_profiler import profile
from psutil._common import bytes2human

def calculate_memory(reserve_pct, consume_pct):
    # From % to MB
    total_memory = psutil.virtual_memory().total / 1024 / 1024
    reserve_qty = (total_memory * reserve_pct) / 100
    consume_qty = (reserve_qty * consume_pct) / 100
   
    return reserve_qty, consume_qty

def reserve_system_memory(memory_qty):
    # http://man7.org/linux/man-pages/man7/cgroups.7.html
    # system memory to be reserved to the script
    cg = Cgroup('my-container')
    cg.set_memory_limit(memory_qty)
    cg.add(os.getpid()) 

def fill_memory(memory_qty):
    # consume: MB of reserved memory
    dummy_buffer = []
    dummy_buffer = ['A' * 1024 * 1024 for _ in range(0, memory_qty)]

    return dummy_buffer

def mem_info():
    nt = psutil.virtual_memory()
    # Pretty print the tuple returned in psutil.virtual_memory()
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value)
        print('%-10s : %7s' % (name.capitalize(), value))

# Check differences in memory usage using the memory profiler
@profile
def mem_check():
    pass

def main():
    # Parsing arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", required=True, help="Percentage of system memory reserved used by the script")

    # TODO: Arguments should be validated
    args = vars(ap.parse_args())
    reserve_pct = 80 
    consume_pct = int(args['m'])

    # Calculate the amount of RAM in MB to reserve and allocate
    reserve, consume = calculate_memory(reserve_pct, consume_pct)

    # Reserve system_mem_pct % of system memory resources for this script
    reserve_system_memory(reserve)

    # Check available memory    
    mem_info()
    print('RESERVED MB:', reserve)
    print('CONSUMED MB:', consume)

    # Simulate memory usage, allocating process_mem_pct % of reserved memory
    data = fill_memory(consume)

    # Check memory has taken from right places
    mem_check()
    mem_info()

    # Wait for the killing signal
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
