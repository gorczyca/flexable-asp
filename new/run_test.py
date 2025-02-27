import os, sys
import subprocess
import time

from config import Settings
from CustomArgumentParser import CustomParser

import pandas as pd
from alive_progress import alive_bar


SETTINGS = Settings()

# APPROACH = 'assumptions' # TODO: temporary
APPROACH = 'externals' # TODO: temporary

# USE_CONSTRAINTS = False
USE_CONSTRAINTS = True

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_flexasp_subprocess_answer(inst_path, goal, args, timeout):

    approach_path = f'{SCRIPT_DIR}/{SETTINGS.approaches_path}'

    # command = f'{SETTINGS.python_path} {approach_path}/run_approach.py {inst_path} {goal} {use_constraints} {approach} {approach_path}/{approach}/logicProgram.lp'
    command = f'{SETTINGS.python_path} {approach_path}/run_approach.py -i {inst_path} -g {goal} -a {args.approach} {"-c" if args.constraints else ""} {"-s" if args.subprocess else ""} -x {args.max_moves} -l {approach_path}/{args.approach}/logicProgram.lp'

    start_time = time.time()
    try:
        output = subprocess.check_output(args=[command], shell=True, stderr=subprocess.STDOUT, timeout=timeout)
        time_needed = time.time() - start_time
        split = output.decode().split('\n')
        results_split = split[0].split()
        results_dict = {
            'result': results_split[0],
            'steps': results_split[1],
            'constraints_no': results_split[2],
            'constraints_max': results_split[3],
            'constraints_min': results_split[4],
            'duration': round(time_needed, 2),
        }
        return results_dict

    except subprocess.TimeoutExpired:
        results_dict = {
            'result': None,
            'steps': None,
            'constraints_no': None,
            'constraints_max': None,
            'constraints_min': None,
            'duration': float(timeout),
        }
        return results_dict


def main():

    parser = CustomParser()
    args = parser.parse_args()
    
    corr_results_df = pd.read_csv(SETTINGS.aspforaba_results_path)

    output_dir = f'{SCRIPT_DIR}/{SETTINGS.output_path}'
    os.makedirs(output_dir, exist_ok=True)

    options_string = f'a={args.approach}_c={args.constraints}_x={args.max_moves}_s={args.subprocess}'
    # use_constraints_substr  = 'constr' if use_constraints else 'noconstr'
    output_path = f'{output_dir}/{options_string}.csv'
    
    if os.path.isfile(output_path):
        # check if a results file already exists
        outputs_df = pd.read_csv(output_path)
    else:
        # otherwise create a DataFrame 
        outputs_df = pd.DataFrame(columns=['id', 'instance', 'goal', 'result', 'duration', 'correct_result', 'verdict', 'steps_obtained', 'constraints_no', 'constraints_max', 'constraints_min'])

    total_size = len(corr_results_df)
    inc_count = 0

    with alive_bar(total_size, dual_line=True, title=f'FlexASP: {options_string}') as bar:
        for i, (index, row) in enumerate(corr_results_df.iterrows(), start=1):

            if ((outputs_df['instance'] == row.instance) & (outputs_df['goal'] == row.goal)).any():
                print(f'Done for: {row.instance}, goal: {row.goal}')
                bar()
                continue

            inst_path = f'{SETTINGS.instances_path}/{row.instance}'
            # ms_result, ms_duration, ms_steps = get_flexasp_subprocess_answer(inst_path, row.goal, SETTINGS.timeout)
            results_dict = get_flexasp_subprocess_answer(inst_path, row.goal, args, SETTINGS.timeout)

            if results_dict['result'] is not None:
                results_dict['verdict'] = 'corr' if results_dict['result'] == row.adm_result else 'inc'
            else:
                results_dict['verdict'] = 'TIMEOUT'


            row_to_append = pd.DataFrame({
                'id': [int(i)],
                'instance': [row.instance],
                'goal': [row.goal],
                'result': [results_dict['result']],
                'duration': [results_dict['duration']],
                'correct_result': [row.adm_result],
                'verdict': [results_dict['verdict']],
		        'steps_obtained': [results_dict['steps']],
		        'constraints_no': [results_dict['constraints_no']],
		        'constraints_max': [results_dict['constraints_max']],
		        'constraints_min': [results_dict['constraints_min']],
                             
            })

            outputs_df = pd.concat([outputs_df, row_to_append], ignore_index=True)
            outputs_df.to_csv(output_path, index=False)
            bar()


if __name__ == '__main__':
    main()
    # try:      
    #     parser = CustomParser()

    #     _, approach, use_constraints  = sys.argv
    #     use_constraints = use_constraints == 'True'
    # except Exception as e:
    #     # instance = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl'
    #     approach, use_constraints = APPROACH, USE_CONSTRAINTS
    #     print(f'\033[93m{"Warning, no commandline parameters provided."}\033[0m')

    # finally: 
    #     main(approach, use_constraints)

    
