#!/usr/bin/python3

from typing import Final


GREEN: Final = '\033[92m'
YELLOW: Final = '\033[93m'
RED: Final = '\033[91m'
BLUE: Final = '\033[94m'
RESET: Final = '\033[0m'





def main():

    from netmiko import ConnectHandler
    import sys
    import pprint
    from pathlib import Path
    from argparse import ArgumentParser, Namespace
    import json
    import logging
    from logging.handlers import RotatingFileHandler
   

    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    sys.path.append(str(parent_dir))
    from utils import csv2list, yaml2dict, get_filnames_in_folder, text2list, get_input_parameters
    from mp import connect_to_devices, disconnect_from_devices

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



    
    # from .checks import check1, srmpls_ping, mpls_ping, srmpls_trace, mpls_trace, trace_result_analysis, ping_result_analysis
    from .checks_reachability import build_ping_mpls_report, build_ping_srmpls_report
    from .checks_reachability import build_trace_mpls_report, build_trace_srmpls_report

    # from .checks_pre_srmpls import checks_pre_srmpls
    from .checks_phase0_pre_srmpls import checks_phase0_pre_srmpls





    logger.info("Main started")

    settings: dict[str,dict[str,str]] = get_input_parameters()
    print('-' * 50)
    pprint.pprint(settings)
    print('-' * 50)

    routers_csv_file: Path = parent_dir / 'input' / settings['parameters']['devices']
    routers_details: list[list[str]] = csv2list(routers_csv_file)

    hosts2ping: list[str] = text2list(parent_dir / 'input' / settings['parameters']['hosts2ping'])
    pprint.pprint(routers_details)
    pprint.pprint(hosts2ping)
    print('-' * 50)

    connections:list[list[BaseConnection, str, str, str]] = connect_to_devices(settings, routers_details)



    
    # prechecks before srmpls configuration
    if settings['checks']['phase0_pre']: # phase0_pre is True
        checks_phase0_pre_srmpls(connections, settings['parameters']['isis_process_name'], settings['parameters']['sr_blocks'])
        print('-' * 50)


    # postcheck



    # check mpls reachability (ping)
    if settings['checks']['reachability_mpls_ping']: # reachability_mpls_ping is True
        build_ping_mpls_report(connections, hosts2ping)
        print('-' * 50)

    # check srmpls reachability (ping)
    if settings['checks']['reachability_srmpls_ping']: # reachability_srmpls_ping is True
        build_ping_srmpls_report(connections, hosts2ping)
        print('-' * 50)

    # check mpls reachability (trace)
    if settings['checks']['reachability_mpls_trace']: # reachability_mpls_trace is True
        build_trace_mpls_report(connections, hosts2ping)
        print('-' * 50)

    # check srmpls reachability (trace)
    if settings['checks']['reachability_srmpls_trace']: # reachability_srmpls_trace is True
        build_trace_srmpls_report(connections, hosts2ping)
        print('-' * 50)


    disconnect_from_devices(connections)

    logger.info("Main finished")

    print('-' * 50)




if __name__ == "__main__":
    main()