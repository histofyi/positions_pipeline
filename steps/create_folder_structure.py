from typing import Dict
import requests

from pipeline import create_folder

from helpers.files import read_json, write_json


def create_folder_structure(**kwargs) -> Dict:
    """
    This function creates the folder structure used by the pipeline.
    
    Args:
        **kwargs: Arbitrary keyword arguments.
    
    Returns:
        Dict: A dictionary of action outputs.
    
    Keyword Args:
        verbose (bool): Whether to print verbose output.
        output_path (str): The output folder.
        config (dict): The config dictionary.
    """
    verbose = kwargs['verbose']
    output_path = kwargs['output_path']
    config = kwargs['config']

    i = 0
    for folder in ['images/positions', 'images/entropy', 'polymorphisms/loci', 'polymorphisms/allele_group']:
        create_folder(f"{output_path}/{folder}", verbose)
        i += 1

    action_output = {
        'folders_created': i
    }

    return action_output