#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: Sean Ryan Rivera | srivera8
Semester: Fall 2024

The python code in this file is original work written by
Sean Ryan Rivera. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: The script will display memory usage information using graphs. It will show the system memory usage
if no program is specified. If a program is specified it will show the memory usage of that program.
'''

import argparse
import os, sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    # check the docs for an argparse option to store this as a boolean.
    parser.add_argument("-H", "--human-readable", action="store_true", help="Prints sizes in human readable format")
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use is not.")
    args = parser.parse_args()
    return args
# create argparse function
# -H human readable
# -r running only

def percent_to_graph(percent: float, length: int=20) -> str:
    "turns a percent 0.0 - 1.0 into a bar graph"
    # Convert percentage to determine the number of # for the graph
    fill = int(percent * length)
    blank = length - fill
    # Outputs graph using basic strings
    graph = ''
    while fill > 0:
        graph = graph + '#'
        fill = fill - 1
    while blank > 0:
        graph = graph + ' ' 
        blank = blank - 1
    return graph
# percent to graph function

def get_sys_mem() -> int:
    "return total system memory (used or available) in kB"
    # Opens and read /proc/meminfo file
    f = open('/proc/meminfo', 'r')
    # Find the MemTotal line
    for line in f:
        if 'MemTotal:' in line:
            mem = int(line.split()[1])
            f.close()
            return mem
    f.close()
    return 0

def get_avail_mem() -> int:
    "return total memory that is available"
    f = open('/proc/meminfo', 'r')
        # Find the MemTotal line
    for line in f:
        if 'MemAvailable:' in line:
            mem = int(line.split()[1])
            f.close()
            return mem
    f.close()
    return 0

def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    # Uses pidof to to retrieve PIDs
    cmd = os.popen('pidof ' + app_name)
    output = cmd.read()
    cmd.close()
    if output == '':
        return []
    return output.split()

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    try:
        f = open('/proc/' + proc_id + '/status', 'r')
        for line in f:
            # Look for VmRSS line
            if 'VmRSS:' in line:
                mem = int(line.split()[1])
                f.close()
                return mem
        f.close()
    except:
        return 0
    return 0

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:
        # Show total system memory if program not specified
        total_mem = get_sys_mem()
        avail_mem = get_avail_mem()
        used_mem = total_mem - avail_mem
        percent = used_mem / total_mem
        graph = percent_to_graph(percent, args.length)
        
        if args.human_readable:
            print('Memory' + ' ' * 9 + '[' + graph + ' | ' + str(int(percent*100)) + '%] ' + bytes_to_human_r(used_mem) + '/' + bytes_to_human_r(total_mem))
        else:
            print('Memory' + ' ' * 9 + '[' + graph + ' | ' + str(int(percent*100)) + '%] ' + str(used_mem) + '/' + str(total_mem))
    else:
        # Gets and displays the memory usage for the process specified
        total_mem = get_sys_mem()
        pids = pids_of_prog(args.program)
        if len(pids) > 0:
            for pid in pids:
                # Calculations
                mem_used = rss_mem_of_pid(pid)
                percent = mem_used / total_mem
                graph = percent_to_graph(percent, args.length)
                
                pid_space = ' ' * (14 - len(pid))
                if args.human_readable:
                    print(pid + pid_space + '[' + graph + ' | ' + str(int(percent*100)) + '%] ' + bytes_to_human_r(mem_used) + '/' + bytes_to_human_r(total_mem))
                else:
                    print(pid + pid_space + '[' + graph + ' | ' + str(int(percent*100)) + '%] ' + str(mem_used) + '/' + str(total_mem))
    # process args
    # if no parameter passed, 
    # open meminfo.
    # get used memory
    # get total memory
    # call percent to graph
    # print

    # if a parameter passed:
    # get pids from pidof
    # lookup each process id in /proc
    # read memory used
    # add to total used
    # percent to graph
    # take total our of total system memory? or total used memory? total used memory.
    # percent to graph.
