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



def check_srmpls_sr_blocks_config (connection:list[BaseConnection, str, str, str, str], sr_blocks: list[int]) -> list[str, str,bool,str, list[str]]:
    """
    function to confirm that segment routing configuration for SRLB and SRGB is correct: start/end label values for SRLB and SRGB are correct
    return list consisting of lists: device_ip(str), device_name(str), result check(bool), comment(str), output(list[str])
    """
    result: list[str, str, bool, str, list[str]] = []
    result.append(connection[1])
    result.append(connection[2])

    srlb_flag: bool = False
    srgb_flag: bool = False
    comment: str = ''
    # print(f'local-block {sr_blocks[0]} {sr_blocks[0]}')
    # print(f'global-block {sr_blocks[2]} {sr_blocks[3]}')
    raw_output: str = connection[0].send_command('show running-config segment-routing')

    if 'Invalid input detected' in raw_output:
        result.append(False)
        result.append('Invalid command')
        result.append(content)
        return result

    content: list[str] = raw_output.split('\n')
    for line in content:
        if f'local-block {sr_blocks[0]} {sr_blocks[1]}' in line:
            srlb_flag = True
            comment += 'SRLB'
            continue
        elif f'global-block {sr_blocks[2]} {sr_blocks[3]}' in line:
            srgb_flag = True
            comment += 'SRGB'
            continue
    if srlb_flag and srgb_flag:
        result.append(True)
    else: 
        result.append(False)

    result.append(comment)
    result.append(content)
    
    return result







def check_srmpls_label_16000 (connection:list[BaseConnection, str, str, str, str], isis_process_name: str) -> list[str, str,bool,str, list[str]]:
    """
    function to confirm that range 16000 is used by isis instance x and bgp
    return list consisting of lists: device_name(str), device_ip(str), result check(bool), comment(str), output(list[str])
    """
    result: list[str, str, bool, str, list[str]] = []
    result.append(connection[1])
    result.append(connection[2])

    isis_flag: bool = False
    bgp_flag: bool = False
    comment: str = ''

    raw_output: str = connection[0].send_command('show mpls label table label 16000')
    if 'Invalid input detected' in raw_output:
        result.append(False)
        result.append('Invalid command')
        result.append(content)
        return result

    content: list[str] = raw_output.split('\n')
    for line in content:
        match = re.search(f'ISIS\(A\):{isis_process_name} +InUse', line)
        if match:
            isis_flag = True
            comment += 'ISIS'
            continue
        match = re.search(f'BGP-VPNv4\(A\):bgp-default +InUse', line)
        if match:
            bgp_flag = True
            comment += 'BGP'
            continue
    if isis_flag and bgp_flag:
        result.append(True)
    else: 
        result.append(False)

    result.append(comment)
    result.append(content)
    
    return result








if __name__ == "__main__":
    pass