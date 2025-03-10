import sys, os
from pathlib import Path

from clingo import Function, Number

sys.path.append(str(Path(__file__).parents[2])) # to import CustomClingoControl from anywhere
from CustomClingoControl import CustomClingoControl


def get_flex_asp_answer(instance, goal, use_constraints, max_move, game_over_check, logic_program_path):
    # start_time = time.time()
    ctrl = CustomClingoControl(asp_files=[instance, logic_program_path])

    ctrl.add_base(f'goal({goal}).')
    ctrl.simple_ground('base')

    step = 0
    return_value = None

    constraints = []
    constraints_no, constraints_max, constraints_min = None, None, None

    # if max_move == -1, continue until game_over_check or proponent won
    horizon = max_move != -1 

    while True:
        # print(f'step {step}')
        ctrl.simple_ground('updateState', step)

        ## here add the constraints
        if use_constraints: # do it ONLY if set constraints set to True
            if constraints:
                ctrl.add('constraints', [], ' '.join(constraints))
                ctrl.simple_ground('constraints')


        # check if proponent won
        if ctrl.is_satisfiable_assumptions(assumptions=[(Function('proponentWon', [Number(step)]), True)]):
            return_value='yes'
            break


        if game_over_check: # check only if you should check
            # check if game can stil continue
            if not ctrl.is_satisfiable_assumptions(assumptions=[(Function('opponentWon', [Number(step)]), False)]):
                return_value='no'
                break

        
        if use_constraints:
            new_constr = ctrl.get_constraints('addConstraints', 'extractConstraints', step, ['propRule', 'propAss'])
            constraints += new_constr

        if horizon and step >= max_move:
            return_value='no'
            break

        step += 1
        ctrl.simple_ground('step', step)

    if use_constraints and constraints:
        constraints_stats = list(map(lambda constraint: len(constraint.split('prop'))-1, constraints))
        constraints_no, constraints_max, constraints_min = len(constraints_stats), max(constraints_stats), min(constraints_stats)

    return return_value, step, constraints_no, constraints_max, constraints_min


if __name__ == '__main__':
    try:      
        _, instance, goal, use_constraints, logic_program_path  = sys.argv
    except Exception as e:
        # instance = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl'
        # goal = 'q4'
        instance = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy05.pl'
        goal = 'u3'
        logic_program_path = '/home/piotr/Dresden/multishot/flexable-asp/new/approaches/assumptions/logicProgram.lp'
        use_constraints = True

        max_move = 5
        game_over_check = False

        print(f'\033[93m{"Warning, working on test instance, because no commandline parameters provided"}\033[0m')

    finally: 
        res, step, const_no, const_max, const_min = get_flex_asp_answer(instance, goal, use_constraints, max_move, game_over_check, logic_program_path)
        print(f'{res} {step} {const_no} {const_max} {const_min}')
    