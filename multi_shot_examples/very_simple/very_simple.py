import sys

import clingo


# GOAL = p 
# INSTANCE = './instances/th_ex.lp'
ENCODING = './multi_shot_examples/very_simple/very_simple.lp'



class CustomControl(clingo.Control):
    def __init__(self, *asp_files):
        super().__init__()
        for file in asp_files:
            super().load(file)

    def ground(self, subprogram, *constants):
        constant_symbols = list(map(clingo.symbol.Number, constants))
        super().ground([(subprogram, constant_symbols)])
        # super().ground([(subprogram, constants)])
        
    
    def assign_external_number(self, name, value):
        super().assign_external(clingo.Function(name, [clingo.symbol.Number(value)]), True) 
    
    def release_external_number(self, name, value):
        super().release_external(clingo.Function(name, [value]))

    def add_base(self, code):
        super().add('base', [], code)


def print_res(res):
    if res.satisfiable:
        print('satisfiable')
    elif res.unsatisfiable:
        print('unsatisfiable')
    else:
        print('unknown')


if __name__ == '__main__':
    # _, instance, goal = sys.argv
    
    goal = 1
    ctrl = CustomControl(ENCODING)
    
    # ctrl.add_base(f'goal({goal}).')
    # ctrl.ground('base')
    ctrl.ground('prg', 0)
    res = ctrl.solve()

    print_res(res)
    
    # ctrl.ground('base')

    # step = 0

    # while True:
    #     ctrl.ground('updateState', step)
    #     res = ctrl.solve()
    #     if res.satisfiable: # <- game is still satisfiable
    #         ctrl.ground('check', step)
    #         ctrl.assign_external('query', step)
    #         res = ctrl.solve()
    #         if res.satisfiable:
    #             print('YES')
    #             break
    #         else:             
    #             ctrl.release_external('query', step)
    #             ctrl.cleanup()
    #             step += 1
    #     else:
    #         print('NO')
    #         break

