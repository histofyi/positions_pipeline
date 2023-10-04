from typing import Dict
import requests

from pipeline import create_folder

from helpers.files import read_json, write_json
from helpers.text import slugify


import numpy as np

rarities = {
    'highly_conserved': 95.0,
    'conserved': 87.0,
    'majority': 51.0,
    'regular': 30.0,
    'common':20.0,
    'often':15.0,
    'occasional':10.0,
    'unusual':5.0,
    'rare':2.5,
    'very_rare':1.0,
    'extremely_rare':0.5
}


def fetch_locus_data(config:Dict, locus:str) -> Dict:
    """
    This function fetches the locus data from the IPD.
    
    Args:
        config (Dict): The config dictionary.
        locus (str): The locus to fetch.
    
    Returns:
        Dict: The locus data.


    """
    url = f"{config['CONSTANTS']['LOCUS_BASE_URL']}/{slugify(locus)}.json"
    
    r = requests.get(url)
    locus_data = r.json()
    
    return locus_data


def build_locus_variability_dict(sequences:str) -> Dict:
    '''
    This function builds a dictionary of the variability for each position in the locus.
    '''
    raw_variability = {}

    for sequence in sequences:
        position = 1
        for residue in sequence:
            if position not in raw_variability:
                raw_variability[position] = {}
            if residue != '-':
                if residue not in raw_variability[position]:
                    raw_variability[position][residue] = 0
                raw_variability[position][residue] += 1

            position += 1

    variability = {}
    for position in raw_variability:
        variability[position] = process_position(raw_variability, position)
    return variability


def classify_rarity(percentage:float, item_count:int) -> str:
    '''
    This function classifies the rarity of a position based on the percentage of residues at that position.
    '''
    if item_count == 1:
        return 'unique'
    elif item_count == 2:
        return 'only_two'
    elif item_count == 3:
        return 'only_three'
    elif item_count == 4:
        return 'only_four'
    elif item_count == 5:
        return 'only_five'
    else:
        rarity = None
        for rarity in rarities:
            if percentage >= rarities[rarity]:
                break 
        return rarity


def process_position(variability:Dict, position:int) -> Dict:

    positional_variability = variability[position]
    values = list(positional_variability.values())

    total = sum(values)

    percentages = [round(value*100/total, 2) for value in values]

    labels = list(positional_variability.keys())

    counts = np.array(values)
    probabilities = (counts / total)


    shannon_entropy = -np.sum(probabilities * np.log2(probabilities))

    normalised_shannon_entropy = 1/np.log2(20) * shannon_entropy

    rarities = []

    i = 0
    for percentage in percentages:
        rarity = classify_rarity(percentage, counts[i])
        rarities.append(rarity)
        i += 1


    position_information = {
        'variability': variability[position],
        'percentages': percentages,
        'values': values,
        'rarities': rarities,
        'labels': labels,
        'shannon_entropy': float(shannon_entropy),
        'normalised_shannon_entropy': float(normalised_shannon_entropy)
    }

    return position_information


def process_loci_polymorphisms(**kwargs) -> Dict:
    """
    This function processes the polymorphisms for each position for the loci in the IPD (initially only HLA)
    
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

    locus_count = 0

    all_variability = {}

    for locus in config['CONSTANTS']['LOCI']:
        cytoplasmic_sequences = fetch_locus_data(config, locus)
        print (locus)
        print (len(cytoplasmic_sequences))
        locus_count += 1

        variability = build_locus_variability_dict(cytoplasmic_sequences)

        test_positions = [3, 24, 45, 67, 68, 71, 7, 9, 11]

        for position in test_positions: 
            print (f"Position {position}")
            print (dict(zip(variability[position]['percentages'],variability[position]['rarities'])))
            print (variability[position]['normalised_shannon_entropy'])
            print ('')

        locus_output_path = f"{output_path}/polymorphisms/{slugify(locus)}_variability.json"
        write_json(locus_output_path, variability, pretty=True)

        all_variability[locus] = variability
    
    all_variability_output_path = f"{output_path}/polymorphisms/hla_loci.json"

    write_json(all_variability_output_path, all_variability, pretty=True)

    action_output = {
        'loci_processed': locus_count    
    }

    return action_output