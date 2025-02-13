import sys
import time
from itertools import groupby


from CustomClingoControl import CustomClingoControl


ENCODING = '/home/piotr/Dresden/multishot/flexable-asp/multi_shot_constraints/encodingMultiShotConstraints.lp'
# ENCODING = '/home/piotr/Dresden/multishot/flexable-asp/multi_shot_alt/encodingMultiShotAlt.lp'


# default solve models is -1

def convert_to_move(step, symbols):
    move_type, move_info = None, None
    
    match list(symbols):
        case []:
            pass
        case [singleElem]:
            # if it's 1-elem thing, then it's either a rule with no body OR an assumption
            if singleElem.name == 'moveAss':
                move_type, assumption = singleElem.arguments[1:]
                move_info = assumption
            else:
                move_type, rule_head = singleElem.arguments[1:]
                move_info = f'{rule_head} ←'
        case more_elems:
            # if it's more than 1-elem, then it' rule with head and body
            rule_head_symbol = [sym for sym in more_elems if sym.name == 'moveRuleHead'][0]
            move_type, rule_head = rule_head_symbol.arguments[1:]
            rule_body_symbols = [sym for sym in more_elems if sym.name == 'moveRuleBody']
            rule_body_literals = list(map(lambda sym: sym.arguments[2].name, rule_body_symbols))
            move_info = f'{rule_head} ← {",".join(rule_body_literals)}'

    print(f'{step}: {move_type}: {move_info}')


def on_model(step, model):
    symbols = model.symbols(shown=True) 

    move_symbols = list(filter(lambda sym: sym.name != 'move' and sym.name.startswith('move'), symbols))
    moves_sorted = sorted(move_symbols, key=lambda symbol: symbol.arguments[0].number)

    print(f'Length: {step}')

    oppWon = list(filter(lambda sym: sym.name == 'opponentWon', symbols))
    if oppWon:
        print('Opponent won!')

    groups = groupby(moves_sorted, key=lambda symbol: symbol.arguments[0].number)
    for gr in groups:
        convert_to_move(*gr)
    print(f'------------------------')
                        

def get_flex_asp_answer(instance, goal):
    # start_time = time.time()
    ctrl = CustomClingoControl(instance, ENCODING)

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

        ##

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


    # total_time = time.time() - start_time
    return return_value, step



if __name__ == '__main__':
    _, instance, goal = sys.argv
    # instance, goal = '/home/piotr/Dresden/multishot/flexable-asp/multi_shot_constraints/simplified2.lp', 'd2'
    # instance, goal = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances/exp_acyclic_depvary_step2_batch_yyy01.pl', 'b2'
    # instance, goal = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl', 'q4'


    res, step = get_flex_asp_answer(instance, goal)
    print(f'{res} {step}')
    pass
    