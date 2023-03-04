import os
import subprocess
import argparse

import pandas as pd
from alive_progress import alive_bar


BASH_SCRIPT_PATH = './run_flexABleASP.sh'
ASPFORABA_RESULTS_PATH = './aspforaba_results.csv'


def get_cmd_args():
    parser = argparse.ArgumentParser(description='Python script to check the flexABle ASP implementation agains the results from ASPFORABA')

    parser.add_argument('-i', '--incremental', action='store_true', help='Use this to select the incremental (incmode) version.')
    parser.add_argument('-l', '--local', action='store_true', help='Use this when running locally.')
    parser.add_argument('timeout', help='Maximal number of seconds per instance.')
    parser.add_argument('max_moves', help='Maximal number moves (steps, turns) of a dispute.')

    return parser.parse_args()


def get_asp_output(file, query, timeout, max_moves, use_inc, local):
    command = f'bash {BASH_SCRIPT_PATH} {"-i" if use_inc else ""} {"-l" if local else ""} {file} {query} {max_moves}'
    try:
        output = subprocess.check_output(args=[command],shell=True, stderr=subprocess.STDOUT, timeout=timeout)
        split = output.decode().split()
        # verdict = 'yes' if split[0] == 'SATISFIABLE' else 'no'
        verdict = 'yes' if 'SATISFIABLE' in split else 'no'
        duration = float(split[-1][:-1])
        return verdict, duration
    except subprocess.TimeoutExpired:
        return None, float(timeout)


if __name__ == '__main__':

    args = get_cmd_args()

    timeout, max_moves, use_inc, local = int(args.timeout), args.max_moves, args.incremental, args.local

    output_path = f'{"inc" if use_inc else "def"}_{max_moves}_{timeout}.csv'

    corr_results_df = pd.read_csv(ASPFORABA_RESULTS_PATH)
    
    if os.path.isfile(output_path):
        # check if a results file already exists
        outputs_df = pd.read_csv(output_path)
    else:
        outputs_df = pd.DataFrame(columns=['instance', 'goal', 'result', 'duration', 'correct_result', 'verdict'])

    total_size = len(corr_results_df)
    inc_count = 0

    with alive_bar(total_size, dual_line=True, title=f'Testing flexABleASP{" (incremental version)" if use_inc else ""}') as bar:
        for i, (index, row) in enumerate(corr_results_df.iterrows(), start=1):

            if ((outputs_df['instance'] == row.instance) & (outputs_df['goal'] == row.goal)).any():
                print(f'Already checked instance: {row.instance} with goal: {row.goal}')
                bar()
                continue

            flex_asp_result, flex_asp_duration = get_asp_output(row.instance, row.goal, timeout, max_moves, use_inc, local)

            if flex_asp_result is None:
                verdict = 'TIMEOUT'    
            else:
                verdict = 'corr' if flex_asp_result == row.adm_result else 'inc'

            row_to_append = pd.DataFrame({
                'instance': [row.instance],
                'goal': [row.goal],
                'result': [flex_asp_result],
                'duration': [flex_asp_duration],
                'correct_result': [row.adm_result],
                'verdict': [verdict]
                             
            })

            outputs_df = pd.concat([outputs_df, row_to_append], ignore_index=True)
            outputs_df.to_csv(output_path, index=False)
            bar()


