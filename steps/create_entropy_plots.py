from typing import Dict
import requests

from pipeline import create_folder

from helpers.files import read_json, write_json
from helpers.text import slugify

from constants.domain_definitions import class_i_domains
from constants.pocket_definitions import pockets, pocket_colours, pocket_letters

import numpy as np
import matplotlib.pyplot as plt


def map_pocket(position:int) -> str:
    for pocket in pockets:
        if str(position) in pockets[pocket]:
            return pocket
    return 'o'


def create_entropy_plot(domain:Dict, variablility:Dict, output_path:str, locus:str):
    positions = []
    entropies = []


    for position in range(domain['start'], domain['end']):
        entropy = variablility[str(position)]['normalised_shannon_entropy']

        entropies.append(entropy)
        positions.append(position)

    fig, ax = plt.subplots(figsize=(25,5))

    bars = plt.bar(positions, entropies)
    residue_list = list(range(domain['start'], domain['end']))

    xticks = []
    yticks = [0,0.2,0.4,0.6,0.8,1.0]
    for residue in residue_list:
        if residue % 10 == 0:
            xticks.append(residue)  

    i = 0
    for bar in bars:
        current_residue = residue_list[i]
        pocket_letter = map_pocket(current_residue)
        bars[i].set_color(pocket_colours[pocket_letter])
        i+= 1

    for index in range(len(positions)):
        if entropies[index] > 0.15:
            ax.text(positions[index], entropies[index], f" {positions[index]}", size=14, ha='center', va='bottom', rotation=90)
    plt.ylim(0, 1)
    plt.xlim(domain['start']-1,domain['end'])
   
    plt.xticks(ticks=xticks, labels=xticks, fontsize=14)
    plt.yticks(ticks=yticks, labels=yticks, fontsize=14)
    plt.xlabel(f"Position in {domain['label']}", labelpad=10, fontsize=16)
    plt.ylabel("Normalised Shannon entropy", labelpad=10, fontsize=16)

    plt.savefig(f"{output_path}/images/entropy/hla_{slugify(locus)}_{domain['name']}.svg", format='svg', bbox_inches='tight')
    plt.savefig(f"{output_path}/images/entropy/hla_{slugify(locus)}_{domain['name']}.png", format='png', bbox_inches='tight')
    pass


def create_entropy_plots(**kwargs) -> Dict:
    """
    This function creates entropy plots for each of the loci in the IPD (initially only HLA)
    
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
        print (locus)
        locus_input_path = f"{output_path}/polymorphisms/loci/{slugify(locus)}_variability.json"
        variability = read_json(locus_input_path)['variability']

        for domain in class_i_domains:
            create_entropy_plot(class_i_domains[domain], variability, output_path, locus)

        locus_count += 1

    action_output = {
        'loci_processed': locus_count    
    }

    return action_output