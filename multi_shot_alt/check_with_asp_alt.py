import os
import subprocess
import argparse

import pandas as pd
from alive_progress import alive_bar

from flexaspMSAlt import get_flex_asp_answer


# ASPFORABA_RESULTS_PATH = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/test/aspforaba_results.csv'
ASPFORABA_RESULTS_PATH = '../test/aspforaba_results.csv'

# OUTPUT_PATH = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/multi_shot/multi_shot_1.csv'
OUTPUT_PATH = 'multi_shot_alt.csv'

#INSTANCES_DIR="/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-tests/instances/aspforaba"
INSTANCES_DIR="/scratch/ws/0/pigo271b-flexASP-workspace/flexABleASP/instances"

TIMEOUT = 600
#TIMEOUT = 50

if __name__ == '__main__':

    corr_results_df = pd.read_csv(ASPFORABA_RESULTS_PATH)
    
    if os.path.isfile(OUTPUT_PATH):
        # check if a results file already exists
        outputs_df = pd.read_csv(OUTPUT_PATH)
    else:
        outputs_df = pd.DataFrame(columns=['instance', 'goal', 'result', 'duration', 'correct_result', 'verdict', 'steps_obtained'])

    total_size = len(corr_results_df)
    inc_count = 0

    with alive_bar(total_size, dual_line=True, title=f'Testing flexABleASP Multi-Shot ') as bar:
        for i, (index, row) in enumerate(corr_results_df.iterrows(), start=1):

            if ((outputs_df['instance'] == row.instance) & (outputs_df['goal'] == row.goal)).any():
                print(f'Already checked instance: {row.instance} with goal: {row.goal}')
                bar()
                continue

            inst_path = f'{INSTANCES_DIR}/{row.instance}'
            ms_result, ms_duration, ms_steps = get_flex_asp_answer(inst_path, row.goal, TIMEOUT)

            if ms_result is not None:
                verdict = 'corr' if ms_result == row.adm_result else 'inc'
            else: 
                verdict = 'TIMEOUT'

            row_to_append = pd.DataFrame({
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
