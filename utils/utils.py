
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import re
import csv
import yaml
import pprint


current_dir = Path(__file__).parent
parent_dir = current_dir.parent

logger = logging.getLogger(__name__)
logger.info(f"Running utils module")


def get_filnames_in_folder(myfolder: Path) -> list[str]:
    """Return a list of filenames (base names) for all files in folder.

    Args:
        folder: Path to the directory to list (can be a str or path-like string).

    Returns:
        A list of filenames (e.g., ['a.txt', 'b.py']). If the folder does not exist
        or is not a directory, an empty list is returned.
    """
    # Convert the input to a Path object for convenient filesystem operations
    # myfolder = Path(folder)

    # If the given path is not a directory, return an empty list.
    # Alternatively, you could raise FileNotFoundError or NotADirectoryError here.
    if not myfolder.exists() or not myfolder.is_dir():
        return []

    result: list[str] = []  # Prepare an empty list with a type annotation

    # Iterate over directory entries (non-recursive). Path.iterdir() yields Path objects.
    for entry in myfolder.iterdir():
        # is_file() ensures we include only regular files (not directories or symlinks-to-dirs).
        if entry.is_file():
            # .name gives the base filename (without the directory path)
            result.append(entry.name)

    return result



def text2list(file_with_output: str)->list[str]:
    """
    parse text lines (separated by end of line) and return list with text of each line
    """
    with open(file_with_output, 'r') as file:
        content: list[str] = file.read().splitlines()
        cleaned_content: list[str] = []
        for line in content:
            cleaned_line: str = line.rstrip()
            cleaned_content.append(cleaned_line)
    logger.info(f"Detected {len(cleaned_content)} lines in input file")
    return cleaned_content



def list2file(content: list, path: Path, filename: str)->None:
    mypath: Path = path / filename
    with mypath.open(mode='w', encoding="utf-8") as f:
        f.write('\n'.join(content))
        f.write('\n')
    print(f"Content has been written to file {filename}")



def yaml2dict(filename: str|Path) -> dict:
    """Loads data from a YAML file and returns it as a Python dictionary."""
    try:
        with open(filename, 'r') as file:
            # yaml.safe_load() parses the YAML file into Python objects
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return {}




def yaml2data (yaml_filename: Path)-> dict[str, str|int]:
    with open(yaml_filename, 'r') as file:
        data = yaml.safe_load(file)
        # repacements = data['repacements']
    return data



def csv2list (csv_file: Path) -> list[list[str]]:
    result: list[list[str]] = []
    with csv_file.open(mode='r', encoding="utf-8") as f:
        for index, row in enumerate(csv.reader(f)):
            # if index == 0:
            #     continue
            result.append(row)
    return result





if __name__ == "__main__": 

    log_filepath = parent_dir / 'logs' / 'utils.log'
    logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(log_filepath, maxBytes=5*1024*1024, backupCount=3),
    ])

    current_dir: Path = Path(__file__).parent
    parent_dir: Path = current_dir.parent

    csv_file_path: Path = parent_dir / 'input' / 'acpt_ac.csv'
    result: list[list[str]] = csv2list(csv_file_path)
    pprint.pprint(result)


    # myfolder_path = parent_dir / 'input'
    # filenames: list[str] = get_filnames_in_folder(myfolder_path)
    # print(filenames)
    # print('-' * 30)

    # for filename in filenames:
    #     result = text2list(parent_dir / 'input' / filename)
    #     print(result)
    #     print('-' * 30)
    
    # yaml_filename = parent_dir / 'input' / 'replacements.yaml'
    # result = yaml2data(yaml_filename)
    # pprint.pprint(result)


