#!/usr/bin/python3

import pprint
import re
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import sys
from netmiko.base_connection import BaseConnection

from .checks_pre_srmpls_child import check_srmpls_label_16000, check_srmpls_sr_blocks_config

current_dir = Path(__file__).parent
parent_dir = current_dir.parent
superparent_dir = parent_dir.parent
sys.path.append(str(superparent_dir))
from mp import connect_to_devices, disconnect_from_devices



def checks_pre_srmpls(connections:list[list[BaseConnection, str, str, str]], isis_process_name: str, sr_blocks: list[int]):


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