from typing import Dict

from pipeline import create_folder

from helpers.files import read_json, write_json
from helpers.text import slugify

import matplotlib.pyplot as plt
import numpy as np


def create_positional_polymorphism_plot(position_information_dict:Dict, output_path:str, locus:str, position:int, target:str='card'):
    significant_residues = []
    significant_percentages = []

    filename = f"{output_path}/images/positions/{target}/{slugify(locus)}_{position}"
    
    j = 0

    labels = []

    for percentage in position_information_dict['percentages']:

        if percentage >= 5.0:
            labels.append(f"{position_information_dict['labels'][j]} [{round(percentage, 1)}%]")
            significant_residues.append(position_information_dict['labels'][j])
            significant_percentages.append(percentage)
        j += 1


    figsize = 15

    values = significant_percentages

    fig = plt.figure()
    fig.set_figwidth(figsize+4)
    fig.set_figheight(figsize-3)
    ax = fig.subplots()
    bbox_props = dict(boxstyle="square,pad=0.2", fc="w", ec="k", lw=0)
    wedges, texts = ax.pie(values, textprops={'fontsize': 30}, wedgeprops=dict(width=0.3), startangle=-260, counterclock=False)

    kw = dict(arrowprops=dict(arrowstyle="-",linewidth=3), bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        if format=='png':
            ax.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),horizontalalignment=horizontalalignment, **kw, size=60)
        else:
            ax.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),horizontalalignment=horizontalalignment, **kw, size=30)

    if target=='card':
        plt.savefig(f"{filename}.png", format='png', bbox_inches='tight')
    else:
        plt.savefig(f"{filename}.svg", format='svg', bbox_inches='tight')
    plt.close()
    pass

def create_positional_polymorphism_plots(**kwargs) -> Dict:
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

        for position in variability:
            create_positional_polymorphism_plot(variability[position], output_path, locus, position, target='page')
            create_positional_polymorphism_plot(variability[position], output_path, locus, position, target='card')

    action_output = {
        'loci_processed': locus_count    
    }

    return action_output