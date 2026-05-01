#!/usr/bin/python3

import pprint
import re
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import sys
from netmiko.base_connection import BaseConnection


current_dir = Path(__file__).parent
parent_dir = current_dir.parent
superparent_dir = parent_dir.parent
sys.path.append(str(superparent_dir))
from mp import connect_to_devices, disconnect_from_devices


def srmpls_ping (connection:list[BaseConnection, str, str, str], hosts2ping: list[str]) -> list[list[str, int, str, str]]:
    """
    the function does srmpls pings for specific router/connection towards hosts from hosts2ping list
    input: connection/router details (connection object, router ip, router hostname, etc.)
    output: result for each ping (for each host) with success rate and optional comment
    """ 
    result: list[list[str, int, str]] = []
    for host in hosts2ping:
        # print(connection[1])
        if host == connection[4]: # host ip is the router ip -> skip
            continue
        worklist: list[str, int, str] = [] # result of ping for specific host: host_ip, success rate, comment, content
        worklist.append(host)
        raw_output: str = connection[0].send_command(f'ping sr-mpls {host}/32')
        content: list[str] = raw_output.split('\n')
        for line in content:
            if 'Success rate' in line: # ping was done, some result was provided
                worklist.append(line.split()[3])
                worklist.append('ping was done') # empty comment
                worklist.append(raw_output)
        if len(worklist) != 4: # means that smth wrong with the command
                worklist.append(0)
                worklist.append(f'incorrect command: ping sr-mpls {host}/32') # empty comment
                worklist.append(raw_output)
        
        result.append(worklist)
    
    return result





def mpls_ping (connection:list[BaseConnection, str, str, str], hosts2ping: list[str]) -> list[list[str, int, str, str]]:
    """
    the function does classic mpls pings for specific router/connection towards hosts from hosts2ping list
    input: connection/router details (connection object, router ip, router hostname, etc.)
    output: result for each ping (for each host) with success rate and optional comment
    """ 
    result: list[list[str, int, str]] = []
    for host in hosts2ping:
        # print(connection[1])
        if host == connection[4]: # host ip is the router ip -> skip
            continue
        worklist: list[str, int, str] = [] # result of ping for specific host: host_ip, success rate, comment, content
        worklist.append(host)
        raw_output: str = connection[0].send_command(f'ping mpls ipv4 {host}/32')
        content: list[str] = raw_output.split('\n')
        for line in content:
            if 'Success rate' in line: # ping was done, some result was provided
                worklist.append(line.split()[3])
                worklist.append('ping was done') # empty comment
                worklist.append(raw_output)
        if len(worklist) != 4: # means that smth wrong with the command
                worklist.append(0)
                worklist.append(f'incorrect command: ping mpls ipv4 {host}/32') # empty comment
                worklist.append(raw_output)
        
        result.append(worklist)
    
    return result





def srmpls_trace (connection:list[BaseConnection, str, str, str], hosts2ping: list[str]) -> list[list[str, bool, int, str, list[str], str]]:
    """
    the function does srmpls trace for specific router/connection towards hosts from hosts2ping list
    input: connection/router details (connection object, router ip, router hostname, router type, router loopback etc.)
    output: result for each trace (for each host) with success rate and label stack
    """ 
    result: list[list[str, bool, int, str, list[str], str]] = [] # dauther list: host_ip, success_bool_value, hops, comment, list of labels used, raw output
    for host in hosts2ping:
        if host == connection[4]: # host ip is the router ip -> skip
            continue
        worklist: list[str, bool, int, str, list[str]] = [] # result of trace for specific host: host_ip, success_bool_value, number of hops, comment, list of labels used, raw_output
        label_stack: list[str] = [] # label stack
        worklist.append(host) # item #0
        raw_output: str = connection[0].send_command(f'trace sr-mpls {host}/32')
        content: list[str] = raw_output.split('\n')
        for line in content:
            if line.startswith('!'): # success sign
                worklist.append(True) # result of trace, item #1
                worklist.append(int(line.split()[1])) # number of hops towards destination, item #2
            elif line.startswith('Q'): # unable to send query
                worklist.append(False) # result of trace, item #1
                worklist.append(-1) # number of hops towards destination, item#2
            else: 
                match = re.search('^. (\d+) \d+\.\d+\.\d+\.\d+ MRU \d+ \[Labels: (\S+) Exp', line)
                if match:
                    label_stack.append(match.group(2))

        # check is worklist lenght has expected value of 3: host, result, number of hops 
        if len(worklist) == 3:
            worklist.append('trace was done') # comment, item#3
            worklist.append(label_stack) # label stack, item#4
            worklist.append(raw_output) # raw output, item#5

        else: # means that smth wrong with the command
            worklist.append(False) # uncussessful trace sigh, item#1
            worklist.append(-1) # number of hops, item#2
            worklist.append(f'incorrect command: trace sr-mpls {host}/32') # comment, item#3
            worklist.append(label_stack) # label stack, item#4
            worklist.append(raw_output) # raw output, item#5
        
        result.append(worklist)
    
    return result







def mpls_trace (connection:list[BaseConnection, str, str, str], hosts2ping: list[str]) -> list[list[str, bool, int, str, list[str], str]]:
    """
    the function does srmpls trace for specific router/connection towards hosts from hosts2ping list
    input: connection/router details (connection object, router ip, router hostname, router type, router loopback etc.)
    output: result for each trace (for each host) with success rate and label stack
    """ 
    result: list[list[str, bool, int, str, list[str], str]] = [] # dauther list: host_ip, success_bool_value, hops, comment, list of labels used, raw output
    for host in hosts2ping:
        if host == connection[4]: # host ip is the router ip -> skip
            continue
        worklist: list[str, bool, int, str, list[str]] = [] # result of trace for specific host: host_ip, success_bool_value, number of hops, comment, list of labels used, raw_output
        label_stack: list[str] = [] # label stack
        worklist.append(host) # item #0
        raw_output: str = connection[0].send_command(f'trace mpls ipv4 {host}/32')
        content: list[str] = raw_output.split('\n')
        for line in content:
            if line.startswith('!'): # success sign
                worklist.append(True) # result of trace, item #1
                worklist.append(int(line.split()[1])) # number of hops towards destination, item #2
            elif line.startswith('Q'): # unable to send query
                worklist.append(False) # result of trace, item #1
                worklist.append(-1) # number of hops towards destination, item#2
            else: 
                match = re.search('^. (\d+) \d+\.\d+\.\d+\.\d+ MRU \d+ \[Labels: (\S+) Exp', line)
                if match:
                    label_stack.append(match.group(2))

        # check is worklist lenght has expected value of 3: host, result, number of hops 
        if len(worklist) == 3:
            worklist.append('trace was done') # comment, item#3
            worklist.append(label_stack) # label stack, item#4
            worklist.append(raw_output) # raw output, item#5

        else: # means that smth wrong with the command
            worklist.append(False) # uncussessful trace sigh, item#1
            worklist.append(-1) # number of hops, item#2
            worklist.append(f'incorrect command: trace mpls ipv4 {host}/32') # comment, item#3
            worklist.append(label_stack) # label stack, item#4
            worklist.append(raw_output) # raw output, item#5
        
        result.append(worklist)
    
    return result




def ping_result_analysis (ping_results_on_router: list[list[str, int, str, str]]) -> list[int]:
    """
    the function takes list with ping result for each host and extract from there key values (4 items): 
    total number of hosts, 
    total number of successful pings (100% success rate), 
    total number of unsuccessful pings (< 100% success rate),
    total number of wrong/failed commands
    """

    result: list[int] = []

    hosts_total: int = 0
    pings_with_success_flag: int = 0
    pings_without_success_flag: int = 0
    failed_commands: int = 0

    for item in ping_results_on_router:
        hosts_total += 1
        if 'incorrect command' in item[3]:
            failed_commands += 1
            continue
        if item[1] == '100':
            pings_with_success_flag += 1
        else: 
            pings_without_success_flag += 1
    
    result.append(hosts_total)
    result.append(pings_with_success_flag)
    result.append(pings_without_success_flag)
    result.append(failed_commands)

    return result







def trace_result_analysis (trace_results_on_router: list[list[str, bool, int, str, list[str], str]]) -> list[int]:
    """
    the function takes list with trace result for each host and extract from there key values (4 items): 
    total number of hosts, 
    total number of successful traces, 
    total number of unsuccessful traces,
    total number of wrong/failed commands
    """

    result: list[int] = []

    hosts_total: int = 0
    traces_with_success_flag: int = 0
    trace_without_success_flag: int = 0
    failed_commands: int = 0

    for item in trace_results_on_router:
        hosts_total += 1
        if 'incorrect command' in item[3]:
            failed_commands += 1
            continue
        if item[1]:
            traces_with_success_flag += 1
        else: 
            trace_without_success_flag += 1
    
    result.append(hosts_total)
    result.append(traces_with_success_flag)
    result.append(trace_without_success_flag)
    result.append(failed_commands)

    return result






if __name__ == "__main__":
    pass