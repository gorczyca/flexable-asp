import sys, os
from pathlib import Path

from clingo import Function, Number

sys.path.append(str(Path(__file__).parents[2])) # to import CustomClingoControl from anywhere
from CustomClingoControl import CustomClingoControl


def build_assumptions(prop_won, step):

    #     assumptions = [(Function('x', [Number(2)], True), False)]

    # % Set:
    # %  hasPropWon(t) -> True to switch this on
    # %  hasPropWon(t) -> False to switch this off
    # :- hasPropWon(t), not proponentWon(t).
    # % if this is satisfiable, return SAT, else check the following

    # % Set:
    # %  gameOn(t) -> True to switch this on
    # %  gameOn(t) -> False to switch this off
    # :- gameOn(t), opponentWon(t).
    return  [
        (Function('hasPropWon', [Number(step)]), prop_won),
        (Function('gameOn', [Number(step)]), not prop_won),
    ]


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

        # if not ctrl.is_safisfiable('checkGameOn', 'gameOn', step):
        #     return_value='no'
        #     break

        tmp = build_assumptions(prop_won=True, step=step)

        # if not ctrl.is_satisfiable_assumptions(assumptions=build_assumptions(prop_won=False, step=step)):
        #     return_value='no'
        #     break

        if ctrl.is_satisfiable_assumptions(assumptions=build_assumptions(prop_won=True, step=step)):
            return_value='yes'
            break




        
        new_constr = ctrl.get_constraints('addConstraints', 'extractConstraints', step, ['propRule', 'propAss'])
        
        constraints += new_constr

        step += 1
        ctrl.simple_ground('step', step) # this should be somehow combined with the next simple_ground
        # if ctrl.is_safisfiable('checkBranching', 'checkNonBranchingMoves', step-1):
            # there are nonBranchingMoves possible
            # ctrl.simple_ground('stepNonBranching', step)
        # else:
            # ctrl.simple_ground('stepBranching', step)

    return return_value, step


if __name__ == '__main__':
    _, instance, goal, logic_program_path  = sys.argv

    # instance = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl'
    # goal = 'w2'
    # logic_program_path = '/home/piotr/Dresden/multishot/flexable-asp/new/approaches/constraints-assumptions/logicProgram.lp'
    
    # raise Exception

    res, step = get_flex_asp_answer(instance, goal, logic_program_path)
    print(f'{res} {step}')
    