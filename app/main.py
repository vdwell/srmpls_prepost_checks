#!/usr/bin/python3



def main():

    from netmiko import ConnectHandler
    import sys
    import pprint
    from pathlib import Path
    from argparse import ArgumentParser, Namespace
    import json
    import logging
    from logging.handlers import RotatingFileHandler
    from .utils import get_input_parameters


    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    sys.path.append(str(parent_dir))
    from utils import csv2list, yaml2dict, get_filnames_in_folder, text2list

    modules = ['main', 'connect']
    log_directory: Path = parent_dir / 'logs'

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root.addHandler(ch)


    for module_name in modules:
        logger = logging.getLogger(module_name)
        # logger = logging.getLogger(mod.__name__)
        log_file: Path = log_directory / f"{module_name}.log"
        fh = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s [%(threadName)s]: %(message)s"))
        logger.addHandler(fh)



    from .connect import connect_to_devices, disconnect_from_devices
    from .checks import check1, srmpls_ping, mpls_ping, srmpls_trace, mpls_trace, trace_result_analysis





    logger.info("Main started")

    mydict: dict[str,dict[str,str]] = get_input_parameters()
    print('-' * 50)
    pprint.pprint(mydict)
    print('-' * 50)

    routers_csv_file: Path = parent_dir / 'input' / mydict['parameters']['devices']
    routers_details: list[list[str]] = csv2list(routers_csv_file)

    hosts2ping: list[str] = text2list(parent_dir / 'input' / mydict['parameters']['hosts2ping'])
    pprint.pprint(routers_details)
    pprint.pprint(hosts2ping)
    print('-' * 50)

    connections:list[list[BaseConnection, str, str, str]] = connect_to_devices(mydict, routers_details)


    # show bgp sessions raw output
    # for connection in connections:
    #     print('-' * 50)
    #     print(f'output for {connection[1]}:')
    #     raw_output = connection[0].send_command('show bgp sessions')
    #     print(raw_output)
    #     print('-' * 50)


    #per device
    # for device_connection in connections:
    #     check1_result: list[str, str, bool, str] = check1(device_connection)
    #     print(f"check1 result for {check1_result[0]} is: {check1_result[2]}, comment {check1_result[3]}")
    # print('-' * 50)

    # srmpls ping results (per device)
    # for device_connection in connections:
    #     srmpls_ping_result: list[list[str, int, str, str]] = srmpls_ping(device_connection, hosts2ping)
    #     print(f'srmpls ping result for {device_connection[1]}:')
    #     for item in srmpls_ping_result:
    #         print(f'  host: {item[0]}, result: {item[1]}, comment: {item[2]}') # removed , content: {item[3][:100].replace('\n', ';')}
    # print('-' * 50)


    # classic mpls ping results (per device)
    # for device_connection in connections:
    #     mpls_ping_result: list[list[str, int, str, str]] = mpls_ping(device_connection, hosts2ping)
    #     print(f'mpls ping result for {device_connection[1]}:')
    #     for item in mpls_ping_result:
    #         print(f'  host: {item[0]}, result: {item[1]}, comment: {item[2]}') # removed , content: {item[3][:100].replace('\n', ';')}
    # print('-' * 50)



    # srmpls trace results (per device)
    for device_connection in connections:
        srmpls_trace_result: list[list[str, bool, int, str, list[str], str]] = srmpls_trace(device_connection, hosts2ping)
        analysis: list[int] = trace_result_analysis(srmpls_trace_result)
        print(f'srmpls ping result for {device_connection[1]}: total:cnt: {analysis[0]}, success_cnt: {analysis[1]}, no_success_cnt: {analysis[2]}, failed_commands_cnt: {analysis[3]}')
        for item in srmpls_trace_result:
            print(f'  host: {item[0]}, result: {item[1]}, hops: {item[2]}, comment: {item[3]}, label_stack: {item[4]}') # removed , content: {item[3][:100].replace('\n', ';')}
    print('-' * 50)



    # mpls trace results (per device)
    for device_connection in connections:
        mpls_trace_result: list[list[str, bool, int, str, list[str], str]] = mpls_trace(device_connection, hosts2ping)
        analysis: list[int] = trace_result_analysis(mpls_trace_result)
    
        print(f'mpls ping result for {device_connection[1]}: total:cnt: {analysis[0]}, success_cnt: {analysis[1]}, no_success_cnt: {analysis[2]}, failed_commands_cnt: {analysis[3]}')
        for item in mpls_trace_result:
            print(f'  host: {item[0]}, result: {item[1]}, hops: {item[2]}, comment: {item[3]}, label_stack: {item[4]}') # removed , content: {item[3][:100].replace('\n', ';')}
    print('-' * 50)












    disconnect_from_devices(connections)


    logger.info("Main finished")

if __name__ == "__main__":
    main()