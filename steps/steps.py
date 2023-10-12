from create_folder_structure import create_folder_structure
from process_loci_polymorphisms import process_loci_polymorphisms
from create_entropy_plots import create_entropy_plots
from create_positional_polymorphism_plots import create_positional_polymorphism_plots

def stub_function():
    pass


steps = {
    '1':{
        'function':create_folder_structure,
        'title_template':'the folder structure used by the pipeline.',
        'title_verb':['Creating','Creates'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '2':{
        'function':process_loci_polymorphisms,
        'title_template':'the locus files produced by the allele pipeline, which are in turn derived from the IPD.',
        'title_verb':['Processing','Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '3':{
        'function':create_entropy_plots,
        'title_template':'the entropy plots for each locus.',
        'title_verb':['Creating','Creates'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '4':{
        'function':create_positional_polymorphism_plots,
        'title_template':'the positional polymorphism plots for each position per locus.',
        'title_verb':['Creating','Creates'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    }
}