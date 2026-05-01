#!/usr/bin/python3

import pprint
import re
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import sys

from .checks_post_srmpls_child import check_isis_srmpls_settings

current_dir = Path(__file__).parent
parent_dir = current_dir.parent
superparent_dir = parent_dir.parent
sys.path.append(str(superparent_dir))
from mp import connect_to_devices, disconnect_from_devices






def checks_after_enabling_srmpls(connections:list[list[BaseConnection, str, str, str]], isis_process_name: str, sr_blocks: list[int]):

    # set#1: checks for isis
    # check#11: SRGB/SRLB in ISIS process (get interfaces from there) (show isis instance <process_name> protocol)
    # check#12: SID/label is allocated in ISIS (show isis instance <process_name> segment-routing label <label>)
    # check#13: uLoopAvoidance enabled with specific timer value (show isis instance <process_name> microloop avoidance)
    # check#14: TI-LFA is enabled on all core interfaces (show isis instance <process_name> interface <interface>)
    # check#15: confirm that adj SIDs/labels are allocated for each ISIS interface (show isis adjacency detail <interface> level 2)
    # check#16: confirm that Prefix-SID Index is present is local LSP (show isis instance 1 database r03.00-00 verbose | utility egrep -A2 'IP-Extended 172.16.0.3/32')
    
    # set#2: checks for bgp
    # check21: confirm that local label for local prefix is allocated (show bgp ipv4 labeled-unicast <prefix> detail)

    # set#3: checks for rib
    # ? for some reason 'show route <local_pefix> detail' does not show local label

    # set#4: checks for fib (mpls, cef)
    # check#41: confirm that local SR-MPLS label/SID is present in FIB table


    #check1: make sure that SRLB and SRGB are configured correctly
    check1_result: list = []
    for connection in connections:
        check1_result.append(check_srmpls_sr_blocks_config (connection, sr_blocks))
    print('-' * 50)
    print('Result of checking SRLB and SRGB blocks (show run segment-routing)')
    for item in check1_result:
        print(f'device: {item[1]} ({item[0]}), check_result: {item[2]}, comment: {item[3]}')
    print('-' * 50)

    #check2: make sure that SRGB is allocated normally and ISIS and BGP use it
    check2_result: list = []
    for connection in connections:
        check2_result.append(check_srmpls_label_16000 (connection, isis_process_name))
    print('-' * 50)
    print('Result of checking SRGB allocation (show mpls label table label 16000)')
    for item in check2_result:
        print(f'device: {item[1]} ({item[0]}), check_result: {item[2]}, comment: {item[3]}')
    print('-' * 50)



if __name__ == "__main__":
    pass