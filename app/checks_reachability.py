#!/usr/bin/python3



import pprint
import re
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import sys
from netmiko.base_connection import BaseConnection


from .checks_reachability_child import srmpls_ping, mpls_ping, srmpls_trace, mpls_trace, trace_result_analysis, ping_result_analysis

current_dir = Path(__file__).parent
parent_dir = current_dir.parent
superparent_dir = parent_dir.parent
sys.path.append(str(superparent_dir))
from mp import connect_to_devices, disconnect_from_devices



# from .connect import connect_to_devices, disconnect_from_devices
# from netmiko.base_connection import BaseConnection
# import pprint
# import re

# from .checks_reachability_child import srmpls_ping, mpls_ping, srmpls_trace, mpls_trace, trace_result_analysis, ping_result_analysis


def build_ping_srmpls_report (connections:list[list[BaseConnection, str, str, str]], hosts2ping: list[str]):
        # srmpls ping results (per device)
    for device_connection in connections:
        srmpls_ping_result: list[list[str, int, str, str]] = srmpls_ping(device_connection, hosts2ping)
        analysis: list[int] = ping_result_analysis(srmpls_ping_result)
        print(f'srmpls ping result for {device_connection[2]} ({device_connection[1]}): total_cnt: {analysis[0]}, success_cnt: {analysis[1]}, no_success_cnt: {analysis[2]}, failed_commands_cnt: {analysis[3]}')
        for item in srmpls_ping_result:
            print(f'  host: {item[0]}, result: {item[1]}, comment: {item[2]}') # removed , content: {item[3][:100].replace('\n', ';')}
    print('-' * 50)


def build_ping_mpls_report (connections:list[list[BaseConnection, str, str, str]], hosts2ping: list[str]):
    # classic mpls ping results (per device)
    for device_connection in connections:
        mpls_ping_result: list[list[str, int, str, str]] = mpls_ping(device_connection, hosts2ping)
        analysis: list[int] = ping_result_analysis(mpls_ping_result)
        print(f'standard mpls ping result for {device_connection[2]} ({device_connection[1]}): total_cnt: {analysis[0]}, success_cnt: {analysis[1]}, no_success_cnt: {analysis[2]}, failed_commands_cnt: {analysis[3]}')
        for item in mpls_ping_result:
            print(f'  host: {item[0]}, result: {item[1]}, comment: {item[2]}') # removed , content: {item[3][:100].replace('\n', ';')}
    print('-' * 50)


def build_trace_srmpls_report (connections:list[list[BaseConnection, str, str, str]], hosts2ping: list[str]):
    # srmpls trace results (per device)
    for device_connection in connections:
        srmpls_trace_result: list[list[str, bool, int, str, list[str], str]] = srmpls_trace(device_connection, hosts2ping)
        analysis: list[int] = trace_result_analysis(srmpls_trace_result)
        print(f'srmpls trace result for {device_connection[2]} ({device_connection[1]}): total_cnt: {analysis[0]}, success_cnt: {analysis[1]}, no_success_cnt: {analysis[2]}, failed_commands_cnt: {analysis[3]}')
        for item in srmpls_trace_result:
            print(f'  host: {item[0]}, result: {item[1]}, hops: {item[2]}, comment: {item[3]}, label_stack: {item[4]}') # removed , content: {item[3][:100].replace('\n', ';')}
    print('-' * 50)


def build_trace_mpls_report (connections:list[list[BaseConnection, str, str, str]], hosts2ping: list[str]):
    # mpls trace results (per device)
    for device_connection in connections:
        mpls_trace_result: list[list[str, bool, int, str, list[str], str]] = mpls_trace(device_connection, hosts2ping)
        analysis: list[int] = trace_result_analysis(mpls_trace_result)
    
        print(f'standard mpls trace result for {device_connection[2]} ({device_connection[1]}): total_cnt: {analysis[0]}, success_cnt: {analysis[1]}, no_success_cnt: {analysis[2]}, failed_commands_cnt: {analysis[3]}')
        for item in mpls_trace_result:
            print(f'  host: {item[0]}, result: {item[1]}, hops: {item[2]}, comment: {item[3]}, label_stack: {item[4]}') # removed , content: {item[3][:100].replace('\n', ';')}
    print('-' * 50)




if __name__ == "__main__":
    pass