import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2])) # to import CustomClingoControl from anywhere
from CustomClingoControl import CustomClingoControl
    

def get_flex_asp_answer(instance, goal, logic_program_path):
    # start_time = time.time()
    ctrl = CustomClingoControl(instance, logic_program_path)

    ctrl.add_base(f'goal({goal}).')
    ctrl.simple_ground('base')

    step = 0
    return_value = None

    constraints = []

    while True:
        # print(f'step {step}')
        ctrl.simple_ground('updateState', step)

        ## here add the constraints
        if constraints:
            ctrl.add('constraints', [], ' '.join(constraints))
            ctrl.simple_ground('constraints')

        if not ctrl.is_safisfiable('checkGameOn', 'gameOn', step):
            return_value='no'
            break

        if ctrl.is_safisfiable('checkPropWon', 'hasPropWon', step):
            return_value='yes'
            break

        
        new_constr = ctrl.get_constraints('addConstraints', 'extractConstraints', step, ['propRule', 'propAss'])
        
        constraints += new_constr

        step += 1
        ctrl.simple_ground('step', step)
        # if ctrl.is_safisfiable('checkBranching', 'checkNonBranchingMoves', step-1):
            # there are nonBranchingMoves possible
            # ctrl.simple_ground('stepNonBranching', step)
        # else:
            # ctrl.simple_ground('stepBranching', step)

    return return_value, step


if __name__ == '__main__':
    # for debugging

    try:      
        _, instance, goal, logic_program_path  = sys.argv
    except Exception as e:
        instance = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl'
        goal = 'q4'
        logic_program_path = '/home/piotr/Dresden/multishot/flexable-asp/new/approaches/constraints/logicProgram.lp'
        
        print(f'\033[93mWarning, working on test instance, because no commandline parameters provided')

    finally: 
        res, step = get_flex_asp_answer(instance, goal, logic_program_path)
        print(f'{res} {step}')
    


