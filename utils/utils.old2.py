#!/usr/bin/python3


from pathlib import Path
from argparse import ArgumentParser, Namespace
import sys

current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))
from utils import csv2list, yaml2dict, get_filnames_in_folder




def get_input_parameters():
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent

    parser = ArgumentParser()

    parser.add_argument(
                        '-c', '--config_file',
                        help='yaml config file in input folder'
                        )

    args: Namespace = parser.parse_args()

    yaml_config: Path = parent_dir / 'input' / args.config_file
    mydict = yaml2dict(yaml_config)
    return mydict





if __name__ == "__main__":
    main()