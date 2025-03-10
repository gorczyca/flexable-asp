import os, sys
import subprocess
import time

from config import Settings
from CustomArgumentParser import CustomParser

import pandas as pd
from alive_progress import alive_bar


SETTINGS = Settings()

# run ASPFORABA

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))




def get_aspforaba_result(inst_path, goal, args, timeout):

    approach_path = f'{SCRIPT_DIR}/{SETTINGS.approaches_path}'

    command = f'{SETTINGS.python_path} {approach_path}/run_approach.py -i {inst_path} -g {goal} -a {args.approach}'

    start_time = time.time()
    try:
        output = subprocess.check_output(args=[command], shell=True, stderr=subprocess.STDOUT, timeout=timeout)
        time_needed = time.time() - start_time
        split = output.decode().split('\n')
        results_split = split[0].split()
        results_dict = {
            'result': results_split[0],
            'duration': round(time_needed, 2)
        }
        return results_dict

    except subprocess.TimeoutExpired:
        results_dict = {
            'result': None,
            'duration': float(timeout)
        }
        return results_dict


def main():

    parser = CustomParser()
    args = parser.parse_args()
    
    instance_goal_df = pd.read_csv(SETTINGS.initial_instance_goal_path)

    # output_dir = f'{SCRIPT_DIR}/{SETTINGS.output_path}'
    # os.makedirs(output_dir, exist_ok=True)

    output_path = SETTINGS.initial_outputs_paths
    
    if os.path.isfile(output_path):
        # check if a results file already exists
        outputs_df = pd.read_csv(output_path)
    else:
        # otherwise create a DataFrame 
        outputs_df = pd.DataFrame(columns=['id', 'instance', 'goal', 'result', 'duration'])

    total_size = len(instance_goal_df)

    with alive_bar(total_size, dual_line=True, title=f'ASPforABA') as bar:
        for i, (_, row) in enumerate(instance_goal_df.iterrows(), start=1):

            if ((outputs_df['instance'] == row.instance) & (outputs_df['goal'] == row.goal)).any():
                print(f'Done for: {row.instance}, goal: {row.goal}')
                bar()
                continue

            inst_path = f'{SETTINGS.instances_path}/{row.instance}'
            results_dict = get_aspforaba_result(inst_path, row.goal, args, SETTINGS.timeout)

            row_to_append = pd.DataFrame({
                'id': [int(i)],
                'instance': [row.instance],
                'goal': [row.goal],
                'result': [results_dict['result']],
                'duration': [results_dict['duration']]
                             
            })

            outputs_df = pd.concat([outputs_df, row_to_append], ignore_index=True)
            outputs_df.to_csv(output_path, index=False)
            bar()


if __name__ == '__main__':
    main()


    
