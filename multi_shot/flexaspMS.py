import sys
import time
from itertools import groupby
from operator import itemgetter

import clingo


# GOAL = p 
# INSTANCE = './instances/th_ex.lp'
# ENCODING = './multi_shot/encodingMultiShot.lp'
ENCODING = './encodingMultiShot.lp'
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
        super().__init__()
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

    #print(model.symbols(shown=True))


    
    # first sort models
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


    # find the latest move at step STEP
    # latest_moves = list(filter(lambda sym: sym.arguments[0].number == step, symbols))

    # move_symbols = list(filter(lambda sym: sym.name != 'move', latest_moves))

    
    move_type = None
    move_info = None

    # move_symbols = list(filter(lambda sym: sym.name != 'move', latest_moves))
                               


    # rem_prop_rules = [sym for sym in latest_moves if sym.name == 'remainingPropRule']
    # prop_rule_heads = [sym for sym in latest_moves if sym.name == 'propRuleHead']
    # rule_heads_literals = list(map(lambda sym: sym.arguments[1].name, prop_rule_heads))

    # print(f'{step}: Remaining rules: {len(rem_prop_rules)}\tRule heads: {len(prop_rule_heads)} {",".join(rule_heads_literals)}')
    # return

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
        # ctrl.ground('checkGameOn', step)
        # ctrl.assign_external('gameOn', step)
        # res = ctrl.solve(on_model=lambda model: on_model(step, model))
        # with ctrl.solve(on_model=lambda model: on_model(step, model), async_=True) as handle:
        with ctrl.solve(async_=True) as handle:
            while not handle.wait(1.0):
                time_elapsed = time.time() - start_time
                if time_elapsed > timeout:
                    handle.cancel()
                    return None, timeout

            res = handle.get()

        if res.satisfiable: # <- game is still satisfiable
            ctrl.ground('check', step)
            ctrl.assign_external('query', step)
            # res = ctrl.solve(on_model=lambda model: on_model(step, model))
            res = ctrl.solve()
            if res.satisfiable:
                return_value = 'yes'
                break
            else:             
                # ctrl.release_external('gameOn', step)
                ctrl.release_external('query', step)
                ctrl.cleanup()
                step += 1
                ctrl.ground('step', step)
        else:
            return_value = 'no'
            break

    total_time = time.time() - start_time
    return return_value, round(total_time, 2), step


if __name__ == '__main__':
    _, instance, goal = sys.argv
    res, duration = get_flex_asp_answer(instance, goal)
    pass
    


# move(1,"PB1",p1) move(2,"OB2",xa1) move(3,"OB1",v2) move(4,"PB2",xe1) move(5,"PF1",r1) move(6,"OB2",xa2) move(7,"PF1",q1) move(8,"PF1",xf1)


# flexable output
# 01: [PF1: u2 ← ]
# 02: [PF1: t3 ← ]
# 03: [PF1: t4 ← ]
# 04: [PF1: t5 ← ]
# 05: [PF1: y1 ← ]
# 06: [PF1: w2 ← ]
# 07: [PF1: r2 ← ]
# 08: [PF1: w5 ← ]
# 09: [PF1: p2 ← ]
# 10: [PF1: y4 ← ]
# 11: [PF1: p3 ← ]
# 12: [PF1: s3 ← ]
# 13: [PF1: x5 ← p3]
# 14: [PB1: q4 ← c3,a6,v2,u3,y2,d1,p1,w3]
# 15: [OB2: u4 ← a2,f1]
# 16: [PB1: w3 ← t1,t2,v2,x1]
# 17: [PB2: s2 ← a1,p3,q5]
# 18: [OB1: u4 ← s3,q5,s2,x2,w1,s1,p1,y5]
# 19: [PB1: x1 ← b1]

# - flexable at this step - game over

# flexasp output
# 1: "PF1": u2 ←
# 2: "PF1": t3 ←
# 3: "PF1": t4 ←
# 4: "PF1": t5 ←
# 5: "PF1": y1 ←
# 6: "PF1": w2 ←
# 7: "PF1": r2 ←
# 8: "PF1": w5 ←
# 9: "PF1": p2 ←
# 10: "PF1": y4 ←
# 11: "PF1": p3 ←
# 12: "PF1": s3 ←
# 13: "PF1": x5 ← p3
# 14: "PB1": q4 ← u3,c3,y2,p1,v2,d1,a6,w3
# 15: "OB2": u4 ← a2,f1
# 16: "PB1": w3 ← v2,t2,t1,x1
# 17: "PB2": s2 ← p3,q5,a1
# 18: "OB1": u4 ← x2,w1,s1,q5,s2,p1,y5,s3
# 19: "PB1": x1 ← b1
# 20: "PF1": x4 ← b1
# 21: "PF1": z3 ← b1
# 22: "OF2": d3
# 23: "OB2": r1 ← y2
# 24: "OB1": r1 ← a6
# 25: "OB2": x3 ← e2
# 26: "OB1": r1 ← t2,w4
# 27: "OB1": x3 ← x1,d1,e5,p1,p4
# 28: "OB1": u4 ← r4,t5,u1
# 29: "OB1": u4 ← p1,p4,s1
# 30: "PB2": z1 ← v4,r2
# 31: "OB1": x3 ← w3,r4,p2,p5,t1,t5,u3,y5

# ---

# 1: "PF1": y1 ←
# 2: "PF1": p3 ←
# 3: "PF1": p2 ←
# 4: "PF1": r2 ←
# 5: "PF1": w2 ←
# 6: "PF1": t4 ←
# 7: "PF1": x5 ← p3
# 8: "PF1": t5 ←
# 9: "PF1": s3 ←
# 10: "PF1": y4 ←
# 11: "PF1": t3 ←
# 12: "PF1": u2 ←
# 13: "PF1": w5 ←
# 14: "PB1": q4 ← u3,a6,v2,c3,d1,w3,p1,y2
# 15: "OB2": u4 ← a2,f1
# 16: "PB2": s2 ← x5,t2,p5,w3,v2,a2,e1,x1,u3,q5,p3,p1,c2

# a2:s2 <- przyczyna!!!
# c3,a6,d1

#c4,b4,a4,f3,e3,d2,b6,c5,a5
# this rule is not applicable! an error spotted

# 17: "OB2": v4 ← b5,c2
# 18: "OB2": r1 ← x5,x1,d5
# 19: "PB1": w3 ← t1,t2,v2,x1
# 20: "PB2": x4 ← b3,e1,u1,w3
# 21: "PB1": u1 ← p4
# 22: "OB2": z4 ← s2,s4,z3
# 23: "OB2": v1 ← a1,u3,d3,d1,s3,c2,r2,w2
# 24: "PB1": p4 ← u5
# 25: "OB1": z3 ← b1
# 26: "PF2": d3
# 27: "PF1": x2 ← d3
# 28: "OB2": v4 ← w1,b3
# 29: "OB2": r1 ← y2
