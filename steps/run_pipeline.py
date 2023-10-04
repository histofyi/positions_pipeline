from typing import Dict

from pipeline import Pipeline

from steps import steps


def run_pipeline(**kwargs) -> Dict:
    pipeline = Pipeline()

    pipeline.load_steps(steps)

    pipeline.run_step('1') # Creates the folder structure used by the pipeline
    pipeline.run_step('2') # Process the polymorphisms for each locus in the IPD (initially only HLA)

    action_logs = pipeline.finalise()

    return action_logs

def main():

    output = run_pipeline()

if __name__ == '__main__':
    main()