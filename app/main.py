#!/usr/bin/python3

from .check


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
    superparent_dir = parent_dir.parent
    sys.path.append(str(superparent_dir))
    from utils import csv2list, yaml2dict, get_filnames_in_folder, text2list, get_input_parameters
    from mp import connect_to_devices, disconnect_from_devices

    modules = ['main', 'connect']
    log_directory: Path = superparent_dir / 'logs'

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
    # from .checks_reachability import check_reachability
    # from .checks_pre_srmpls import checks_pre_srmpls
    from .checks_ph





    logger.info("Main started")

    settings: dict[str,dict[str,str]] = get_input_parameters()
    print('-' * 50)
    pprint.pprint(settings)
    print('-' * 50)

    routers_csv_file: Path = superparent_dir / 'input' / settings['parameters']['devices']
    routers_details: list[list[str]] = csv2list(routers_csv_file)

    hosts2ping: list[str] = text2list(superparent_dir / 'input' / settings['parameters']['hosts2ping'])
    pprint.pprint(routers_details)
    pprint.pprint(hosts2ping)
    print('-' * 50)

    connections:list[list[BaseConnection, str, str, str]] = connect_to_devices(settings, routers_details)



    
    # prechecks before srmpls configuration
    if settings['checks']['phase0_pre']: # phase0_pre is True
        checks_pre_srmpls(connections, settings['parameters']['isis_process_name'], settings['parameters']['sr_blocks'])

    # check mpls reachability
    # check_reachability(connections, hosts2ping)

    











    disconnect_from_devices(connections)


    logger.info("Main finished")

if __name__ == "__main__":
    main()