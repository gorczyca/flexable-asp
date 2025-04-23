import sys, os
from pathlib import Path

from clingo import Function, Number, String

sys.path.append(str(Path(__file__).parents[2])) # to import CustomClingoControl from anywhere
from CustomClingoControl import CustomClingoControl


def get_flex_asp_answer(instance, goal, logic_program_path):
    # start_time = time.time()
    ctrl = CustomClingoControl(asp_files=[instance, logic_program_path])

    ctrl.add_base(f'goal({goal}).')
    ctrl.simple_ground('base')

    step = 0
    return_value = None

    while True:
        print(f'STEP: {step}')

        ctrl.enumerate_answer_sets()
        print('UPDATE step')


        ctrl.simple_ground('updateState', step)

        # check if proponent won
        if ctrl.is_satisfiable_assumptions(assumptions=[(Function('gameOver', [Number(step), String("P")]), True)]):
            return_value='yes'
            break


        if not ctrl.is_satisfiable_assumptions(assumptions=[(Function('gameOver', [Number(step), String("O")]), False)]):
            return_value='no'
            break

        ctrl.enumerate_answer_sets()

        step += 1
        ctrl.simple_ground('step', step)

    return return_value, step

if __name__ == '__main__':
    try:      
        _, instance, goal, logic_program_path  = sys.argv
    except Exception as e:
        # instance = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl'
        # goal = 'q4'
        instance = '/home/piotr/Dresden/multishot/flexable-asp/new/approaches/af-as-aba/inst1.lp'
        goal = 'a1'
        logic_program_path = '/home/piotr/Dresden/multishot/flexable-asp/new/approaches/af-as-aba/prog.lp'

        # print(f'\033[93m{"Warning, working on test instance, because no commandline parameters provided"}\033[0m')

    finally: 
        res, step = get_flex_asp_answer(instance, goal, logic_program_path)
        print(f'{res} {step}')
    