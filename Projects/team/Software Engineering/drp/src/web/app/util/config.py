""" Utility File For Accessing DRP Config """
from typing import Dict, Any
from json import load
from os import path, getcwd

def load_config() -> Dict[str, Any]:
    """ Function To Load Config """
    config_path = path.join(path.abspath(getcwd()), '..', 'drp-config.json')
    with open(config_path, 'r', encoding='UTF-8') as config_file:
        config = load(config_file)
    return config
