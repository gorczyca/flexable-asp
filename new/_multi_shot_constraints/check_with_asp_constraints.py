import os
import subprocess
import argparse
import time

import pandas as pd
from alive_progress import alive_bar

# from flexaspMSAltTest import get_flex_asp_answer


# ASPFORABA_RESULTS_PATH = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/test/aspforaba_results.csv'
ASPFORABA_RESULTS_PATH = '/home/piotr/Dresden/multishot/flexable-asp/test/aspforaba_results.csv'

# OUTPUT_PATH = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/multi_shot/multi_shot_1.csv'
OUTPUT_PATH = '/home/piotr/Dresden/multishot/flexable-asp/multi_shot_constraints/multi_shot_constraints.csv'

#INSTANCES_DIR="/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-tests/instances/aspforaba"
# INSTANCES_DIR="/scratch/ws/0/pigo271b-flexASP-workspace/flexABleASP/instances"

# INSTANCES_DIR="/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances"
INSTANCES_DIR="/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances"


TIMEOUT = 600
#TIMEOUT = 50


def get_flexasp_subprocess_answer(inst_path, goal, timeout):
    python_path = '/home/piotr/anaconda3/envs/flexable/bin/python'
    script_path = '/home/piotr/Dresden/multishot/flexable-asp/multi_shot_constraints/flexaspMSConstraints.py'

    command = f'{python_path} {script_path} {inst_path} {goal}'

    print(command)

    start_time = time.time()
    try:
        output = subprocess.check_output(args=[command], shell=True, stderr=subprocess.STDOUT, timeout=timeout)
        time_needed = time.time() - start_time
        split = output.decode().split('\n')
        [result, steps] = split[0].split()
        return result, round(time_needed, 2), steps

    except subprocess.TimeoutExpired:
        return None, float(timeout), None



if __name__ == '__main__':


    corr_results_df = pd.read_csv(ASPFORABA_RESULTS_PATH)
    
    if os.path.isfile(OUTPUT_PATH):
        # check if a results file already exists
        outputs_df = pd.read_csv(OUTPUT_PATH)
    else:
        outputs_df = pd.DataFrame(columns=['id', 'instance', 'goal', 'result', 'duration', 'correct_result', 'verdict', 'steps_obtained'])

    total_size = len(corr_results_df)
    inc_count = 0

    with alive_bar(total_size, dual_line=True, title=f'Testing flexABleASP Multi-Shot ') as bar:
        for i, (index, row) in enumerate(corr_results_df.iterrows(), start=1):

            if ((outputs_df['instance'] == row.instance) & (outputs_df['goal'] == row.goal)).any():
                print(f'Already checked instance: {row.instance} with goal: {row.goal}')
                bar()
                continue

            inst_path = f'{INSTANCES_DIR}/{row.instance}'
            ms_result, ms_duration, ms_steps = get_flexasp_subprocess_answer(inst_path, row.goal, TIMEOUT)

            if ms_result is not None:
                verdict = 'corr' if ms_result == row.adm_result else 'inc'
            else: 
                verdict = 'TIMEOUT'

            row_to_append = pd.DataFrame({
                'id': [int(i)],
                'instance': [row.instance],
                'goal': [row.goal],
                'result': [ms_result],
                'duration': [ms_duration],
                'correct_result': [row.adm_result],
                'verdict': [verdict],
		        'steps_obtained': [ms_steps]
                             
            })

            outputs_df = pd.concat([outputs_df, row_to_append], ignore_index=True)
            outputs_df.to_csv(OUTPUT_PATH, index=False)
            bar()
