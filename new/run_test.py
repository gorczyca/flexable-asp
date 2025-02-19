import os
import subprocess
import time

from config import Settings

import pandas as pd
from alive_progress import alive_bar


SETTINGS = Settings()

APPROACH = 'constraints' # TODO: temporary

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_flexasp_subprocess_answer(inst_path, goal, timeout):

    # this has to be now run as a module
    approach_path = f'{SCRIPT_DIR}/{SETTINGS.approaches[APPROACH]}'

    command = f'{SETTINGS.python_path} {approach_path}/control.py {inst_path} {goal} {approach_path}/logicProgram.lp'

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

    corr_results_df = pd.read_csv(SETTINGS.aspforaba_results_path)

    output_dir = f'{SCRIPT_DIR}/{SETTINGS.output_path}'
    os.makedirs(output_dir, exist_ok=True)
    output_path = f'{output_dir}/{APPROACH}.csv'
    
    if os.path.isfile(output_path):
        # check if a results file already exists
        outputs_df = pd.read_csv(output_path)
    else:
        # otherwise create a DataFrame 
        outputs_df = pd.DataFrame(columns=['id', 'instance', 'goal', 'result', 'duration', 'correct_result', 'verdict', 'steps_obtained'])

    total_size = len(corr_results_df)
    inc_count = 0

    with alive_bar(total_size, dual_line=True, title=f'FlexASP: {APPROACH}') as bar:
        for i, (index, row) in enumerate(corr_results_df.iterrows(), start=1):

            if ((outputs_df['instance'] == row.instance) & (outputs_df['goal'] == row.goal)).any():
                print(f'Done for: {row.instance}, goal: {row.goal}')
                bar()
                continue

            inst_path = f'{SETTINGS.instances_path}/{row.instance}'
            ms_result, ms_duration, ms_steps = get_flexasp_subprocess_answer(inst_path, row.goal, SETTINGS.timeout)

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
            outputs_df.to_csv(output_path, index=False)
            bar()
