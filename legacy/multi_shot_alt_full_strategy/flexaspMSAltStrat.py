import sys
import time
from itertools import groupby
from operator import itemgetter

import clingo


ENCODING = './encodingMultiShotAltStrat.lp'
# ENCODING = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/multi_shot/encodingMultiShot.lp'

# flexASP input
# '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-tests/instances/aspforaba/exp_acyclic_depvary_step10_batch_yyy01.pl'
# 'q4'

# flexable input
# '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/rule_dd_instances/exp_acyclic_depvary_step10_batch_yyy01.pl'
# 'q4

# problematic instance
# flexable /home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/rule_dd_instances/exp_acyclic_depvary_step10_batch_yyy01.pl -i apx -g q4




class CustomControl(clingo.Control):
    def __init__(self, *asp_files):
        super().__init__(['--warn=none'])
        for file in asp_files:
            super().load(file)

    def ground(self, subprogram, *constants):
        constant_symbols = list(map(clingo.symbol.Number, constants))
        super().ground([(subprogram, constant_symbols)])        
    
    def assign_external(self, name, value):
        super().assign_external(clingo.Function(name, [clingo.symbol.Number(value)]), True) 
    
    def release_external(self, name, value):
        super().release_external(clingo.Function(name, [clingo.symbol.Number(value)]))

    def add_base(self, code):
        super().add('base', [], code)


def translate_facts_to_move(symbol):
    pass


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


def get_flex_asp_answer(instance, goal, timeout):
    start_time = time.time()
    ctrl = CustomControl(instance, ENCODING)
    
    ctrl.add_base(f'goal({goal}).')
    ctrl.ground('base')

    step = 0
    return_value = None
    res = None

    while True:
        ctrl.ground('updateState', step)
        ctrl.ground('checkPropWon', step)
        ctrl.assign_external('hasPropWon', step)
        with ctrl.solve(async_=True) as handle:
            while not handle.wait(1.0):
                time_elapsed = time.time() - start_time
                if time_elapsed > timeout:
                    handle.cancel()
                    return None, timeout, step
            res = handle.get()

            if res.satisfiable: # <- the instance is SAT, there is a successful derivation
                return_value = 'yes'
                break
            else: # <- check if the game can still be advanced forward
                ctrl.release_external('hasPropWon', step)
                ctrl.cleanup() # <-  remove the constraint that the prop has to win

                ctrl.ground('checkGameOn', step) # <- check ig the game can still be played
                ctrl.assign_external('gameOn', step)

                with ctrl.solve(async_=True) as handle2:
                    while not handle2.wait(1.0):
                        time_elapsed = time.time() - start_time
                        if time_elapsed > timeout:
                            handle2.cancel()
                            return None, timeout, step
                        
                    res = handle2.get()

                    if res.satisfiable: # game is still on
                        ctrl.release_external('gameOn', step) # remove constraint
                        ctrl.cleanup()

                        step += 1
                        ctrl.ground('step', step)   # perform the next move
                    else:       
                        return_value = 'no'    
                        break

    total_time = time.time() - start_time
    return return_value, round(total_time, 2), step


if __name__ == '__main__':
    _, instance, goal = sys.argv
    res, duration = get_flex_asp_answer(instance, goal)
    pass
    