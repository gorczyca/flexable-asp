import sys, os, time, subprocess
from pathlib import Path


sys.path.append(str(Path(__file__).parents[2])) # to import config
sys.path.append(str(Path(__file__).parents[0].joinpath('aspforaba_repo', 'src', 'aspforaba'))) # to import ABASolver

# from CustomClingoControl import CustomClingoControl
from config import Settings
from aba_solver import ABASolver


def get_aspforaba_answer(instance, goal):
    # print('im here')
    s = ABASolver(from_file=instance)
    result = s.decide_credulous('AD', goal)
    res =  'yes' if result else 'no'
    return res, None, None, None, None


if __name__ == '__main__':
    # for debugging
    try:      
        _, instance, goal  = sys.argv
    except Exception as e:
        # instance = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl'
        # goal = 'q4'
        # instance = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy05.pl'
        # goal = 'c3'
        # goal = 'w2'
        # instance = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/iccma2023_instances/aba_500_0.1_5_5_2.aba'
        # goal = 's278'

        # print(f'\033[93m{"Warning, working on test instance, because no commandline parameters provided"}\033[0m')

        # PROBLEMATIC
        # instance = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/problematic_instance.aba'
        # goal = 's3055'
        # goal = 'trivial'
        instance = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy07.pl'
        goal = 'u2' 
        # encoding = '/home/piotr/Dresden/multishot/flexable-asp/new/approaches/assumptions/logicProgram.lp'
    finally: 
        res = get_aspforaba_answer(instance, goal)
        print(res)
    