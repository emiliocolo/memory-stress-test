#
# memory-test
# created date: 23/11/2019
# name: Emilio Coronado
# description: a basic script that reserves a % of memory from the system and then allocates a % of that reserved memory to simulate large memory usage and constraints
#
import os
import time
import sys
import signal
import psutil
import subprocess
import traceback
import argparse
from cgroups import Cgroup
from cgroups.user import create_user_cgroups
from memory_profiler import profile
from sys import getsizeof
from psutil._common import bytes2human

def process_info():
    # Returns the process information
    process = psutil.Process(os.getpid())
    return process

def mem_info(swap=False):
    # Prints system memory information
    print('MEMORY\n------')
    pprint_ntuple(psutil.virtual_memory())

    if swap == True:
        print('\nSWAP\n----')
        pprint_ntuple(psutil.swap_memory())

def system_reserve_memory(system_mem_pct):
    # Function that reserves system memory, based on Linux cgroups
    # http://man7.org/linux/man-pages/man7/cgroups.7.html
    # system_mem_pct: % of system memory to be reserved to the script

    try:
        # setup cgroup directory for this user
        user = os.getlogin()
        create_user_cgroups(user)

        # First we create the cgroup and we set it's cpu and memory limits
        cg = Cgroup('mm')
        cg.set_cpu_limit(50)  # TODO : get these as command line options
        cg.set_memory_limit(500)

        # Then we a create a function to add a process in the cgroup
        def in_cgroup():
            try:
                pid = os.getpid()
                cg = Cgroup('mm')
               # for env in env_vars:
               #     log.info('Setting ENV %s' % env)
               #     os.putenv(*env.split('=', 1))

                # Set network namespace
               # netns.setns(netns_name)

                # add process to cgroup
                cg.add(pid)

               # os.chroot(layer_dir)
               # if working_dir != '':
               #     log.info("Setting working directory to %s" % working_dir)
               #     os.chdir(working_dir)
            except Exception as e:
                traceback.print_exc()
               # log.error("Failed to preexecute function")
               # log.error(e)
        #cmd = start_cmd
        #log.info('Running "%s"' % cmd)
        #process = subprocess.Popen(cmd, preexec_fn=in_cgroup, shell=True)
        #process.wait()
        #print(process.stdout)
        #log.error(process.stderr)
    except Exception as e:
        traceback.print_exc()
        #log.error(e)
    finally:
        print('done')
        #log.info('Finalizing')
        #NetNS(netns_name).close()
        #netns.remove(netns_name)
        #ipdb.interfaces[veth0_name].remove()
        #log.info('done')

def process_fill_memory(process_mem_pct, verbose=False):
    # Simulate a process that takes all the reserved memory
    # process_mem_pct: % of memory usage to be allocated/simulated

    dummy_buffer = []
    dummy_buffer = ['A' * 1024 * 1024 for _ in range(0, 100)]

    # Display some stats about the data generated
    if verbose:
        print('Generated ', len(dummy_buffer), 'elements of size: ', getsizeof(dummy_buffer[0]) >> 20, 'MB')
        total = 0
        for i in range(len(dummy_buffer)):
            total += getsizeof(dummy_buffer[i])
        print(total >> 20, 'MB')
        print(total >> 30, 'GB')

    return dummy_buffer

def pprint_ntuple(nt):
    # Pretty print the tuple returned in psutil.virtual_memory()
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value)
        if name == 'free':
            print('%-10s : %7s' % (name.capitalize(), value))

@profile
def mem_check():
    # Check differences in memory usage using the memory profiler
    pass

def main():
    # Intercept some system signals to exit clean
    def terminate(signum, frame):
        print('Exiting ...')
        sys.exit()

    signal.signal(signal.SIGINT, terminate)
    signal.signal(signal.SIGTERM, terminate)

    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-sm", required=True, help="Percentage of system memory reserved to the script")
    ap.add_argument("-pm", required=True, help="Percentage of the reserved memory to be taken by the process")

    # TODO: Arguments should be validated
    args = vars(ap.parse_args())
    system_mem_pct = int(args['sm'])
    process_mem_pct = int(args['pm'])

    # let's ask about information from this process
    ps = process_info()

    # Reserve system_mem_pct % of system memory resources for this script
    # system_reserve_mem(ps, system_mem_pct)

    # Check available memory
    mem_info()

    # Simulate memory usage, allocating process_mem_pct % of reserved memory
    data = process_fill_memory(process_mem_pct)

    # Wait for the killing signal, and print free memory, every 60 s
    count = 0
    while True:
        time.sleep(10)
        print('.')
        if count == 6:
            # Check from profiler we still are using memory
            mem_check()
            # Check available memory
            mem_info()
            count = 0
        count += 1

if __name__ == "__main__":
    main()
