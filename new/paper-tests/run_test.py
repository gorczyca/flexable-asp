import os, sys
import subprocess
import time
import argparse


import pandas as pd
from alive_progress import alive_bar

HPC = True

if HPC:
    OUTPUTS_PATH = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/new/paper-tests/results'
    PYTHON_PATH = '/data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/python'
else: 
    PYTHON_PATH = '/home/piotr/anaconda3/envs/flexable/bin/python'
    OUTPUTS_PATH = '/home/piotr/Dresden/multishot/flexable-asp/new/paper-tests/results'

TIMEOUT = 300

class CustomParser(argparse.ArgumentParser): 
    def __init__(self):
        super().__init__()
        self.add_argument("-p", dest="problem", type=str) # aba / af
        self.add_argument("-s", dest="solver", type=str) # our / corr

INSTANCES_CONFIG = {
    'aba': {
        'problem_instances': '',
        'problem_instances_goals': '',
    },
    'af': {
        'problem_instances': '/home/piotr/Dresden/multishot/flexable-asp/new/af-test-instances/instances' 
            if not HPC else '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/af-test-instances/instances',
        'problem_instances_goals': '/home/piotr/Dresden/multishot/flexable-asp/new/af-test-instances/instance-goal.csv' 
            if not HPC else '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/new/af-test-instances/instance-goal.csv',
    }
}

SOLVER_CONFIG = {
    'multi-af': {
        'lp': '/home/piotr/Dresden/multishot/flexable-asp/new/paper-tests/test-af/encoding.lp' 
            if not HPC else '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/new/paper-tests/test-af/encoding.lp',
        'control': '/home/piotr/Dresden/multishot/flexable-asp/new/paper-tests/test-af/control.py' 
            if not HPC else '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/new/paper-tests/test-af/control.py'
    },
    'aspartix': {
        'lp': '/home/piotr/Dresden/multishot/flexable-asp/new/paper-tests/aspartix/adm.dl' 
            if not HPC else '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/new/paper-tests/aspartix/adm.dl',
        'control': '/home/piotr/Dresden/multishot/flexable-asp/new/paper-tests/aspartix/control.py' 
            if not HPC else '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/new/paper-tests/aspartix/control.py'
    }
}


def get_flexasp_subprocess_answer(problem, solver, inst_path, goal, timeout):

    command = None

    if problem == 'af' and (solver == 'multi-af' or solver =='aspartix'):
        command = f'{PYTHON_PATH} {SOLVER_CONFIG[solver]["control"]} {inst_path} {goal} {SOLVER_CONFIG[solver]["lp"]}'
    # elif problem == 'af' and solver == 'aspartix':

    start_time = time.time()
    try:
        output = subprocess.check_output(args=[command], shell=True, stderr=subprocess.STDOUT, timeout=timeout)
        time_needed = time.time() - start_time
        res = output.decode().strip().split('\n')[-1]
        # results_split = 
        results_dict = {
            'result': res,
            'duration': round(time_needed, 2),
        }
        return results_dict

    except subprocess.TimeoutExpired:
        results_dict = {
            'result': None,
            'duration': float(timeout),
        }
        return results_dict


def main(problem, solver):    
    problem_instances_goals = pd.read_csv(INSTANCES_CONFIG[problem]['problem_instances_goals'])

    output_dir = f'{OUTPUTS_PATH}'
    os.makedirs(output_dir, exist_ok=True)
    options_string = f'{problem}_{solver}'
    output_path = f'{output_dir}/{options_string}.csv'
    
    if os.path.isfile(output_path):
        # check if a results file already exists
        outputs_df = pd.read_csv(output_path)
    else:
        # otherwise create a DataFrame 
        outputs_df = pd.DataFrame(columns=['id', 'instance', 'goal', 'result'])

    total_size = len(problem_instances_goals)
    inc_count = 0

    with alive_bar(total_size, dual_line=True, title=options_string) as bar:
        for i, (index, row) in enumerate(problem_instances_goals.iterrows(), start=1):

            if ((outputs_df['instance'] == row.instance) & (outputs_df['goal'] == row.goal)).any():
                print(f'Done for: {row.instance}, goal: {row.goal}')
                bar()
                continue

            inst_path = f'{INSTANCES_CONFIG[problem]["problem_instances"]}/{row.instance}'
            # ms_result, ms_duration, ms_steps = get_flexasp_subprocess_answer(inst_path, row.goal, SETTINGS.timeout)
            results_dict = get_flexasp_subprocess_answer(problem, solver, inst_path, row.goal, TIMEOUT)

            # if results_dict['result'] is not None:
            #     results_dict['verdict'] = 'corr' if results_dict['result'] == row.adm_result else 'inc'
            # else:
            #     results_dict['verdict'] = 'TIMEOUT'


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
    problem, solver = None, None
    try:      
        args = CustomParser().parse_args()
        # problem, solver = 'af', 'multi-af'
        # problem, solver = 'af', 'aspartix'
        problem, solver = args.problem, args.solver
    # except Exception as e:
        # pass
        # problem, solver = 'af', 'multi-af'
        # print(f'\033[93m{"Warning, no commandline parameters provided."}\033[0m')

    finally: 
        main(problem, solver)

    
