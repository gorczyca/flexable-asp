import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2])) # to import CustomClingoControl from anywhere
from CustomClingoControl import CustomClingoControl
    

def get_flex_asp_answer(instance, goal, use_constraints, logic_program_path):
    # start_time = time.time()
    ctrl = CustomClingoControl(instance, logic_program_path)

    ctrl.add_base(f'goal({goal}).')
    ctrl.simple_ground('base')

    step = 0
    return_value = None

    constraints = []
    constraints_no, constraints_max, constraints_min = None, None, None

    while True:
        # print(f'step {step}')
        ctrl.simple_ground('updateState', step)

        ## here add the constraints
        if use_constraints: # do it ONLY if set constraints set to True
            if constraints:
                ctrl.add('constraints', [], ' '.join(constraints))
                ctrl.simple_ground('constraints')

        if not ctrl.is_safisfiable('checkGameOn', 'gameOn', step):
            return_value='no'
            break

        if ctrl.is_safisfiable('checkPropWon', 'hasPropWon', step):
            return_value='yes'
            break

        if use_constraints:
            new_constr = ctrl.get_constraints('addConstraints', 'extractConstraints', step, ['propRule', 'propAss'])
            constraints += new_constr

        step += 1
        ctrl.simple_ground('step', step)

    if use_constraints and constraints:
        constraints_stats = list(map(lambda constraint: len(constraint.split('prop'))-1, constraints))
        constraints_no, constraints_max, constraints_min = len(constraints_stats), max(constraints_stats), min(constraints_stats)

    return return_value, step, constraints_no, constraints_max, constraints_min


if __name__ == '__main__':
    # for debugging

    try:      
        _, instance, goal, use_constraints, logic_program_path  = sys.argv
    except Exception as e:
        # instance = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl'
        # goal = 'q4'
        instance = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy05.pl'
        goal = 'c3'
        logic_program_path = '/home/piotr/Dresden/multishot/flexable-asp/new/approaches/externals/logicProgram.lp'
        use_constraints = True

        print(f'\033[93m{"Warning, working on test instance, because no commandline parameters provided"}\033[0m')

    finally: 
        res, step, const_no, const_max, const_min = get_flex_asp_answer(instance, goal, use_constraints, logic_program_path)
        print(f'{res} {step} {const_no} {const_max} {const_min}')
    


