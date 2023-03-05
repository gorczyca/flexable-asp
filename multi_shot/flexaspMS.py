import sys
import time

import clingo


# GOAL = p 
# INSTANCE = './instances/th_ex.lp'
ENCODING = './multi_shot/encodingMultiShot.lp'



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


def get_flex_asp_answer(instance, goal):
    start_time = time.time()
    ctrl = CustomControl(instance, ENCODING)
    
    ctrl.add_base(f'goal({goal}).')
    ctrl.ground('base')

    step = 0
    return_value = None

    while True:
        ctrl.ground('updateState', step)
        res = ctrl.solve()
        if res.satisfiable: # <- game is still satisfiable
            ctrl.ground('check', step)
            ctrl.assign_external('query', step)
            res = ctrl.solve()
            if res.satisfiable:
                return_value = 'yes'
                break
            else:             
                ctrl.release_external('query', step)
                ctrl.cleanup()
                step += 1
                ctrl.ground('step', step)
        else:
            return_value = 'no'
            break

    total_time = time.time() - start_time
    return return_value, round(total_time, 2)


if __name__ == '__main__':
    _, instance, goal = sys.argv
    res, duration = get_flex_asp_answer(instance, goal)
    pass
    


# move(1,"PB1",p1) move(2,"OB2",xa1) move(3,"OB1",v2) move(4,"PB2",xe1) move(5,"PF1",r1) move(6,"OB2",xa2) move(7,"PF1",q1) move(8,"PF1",xf1)