import clingo


INSTANCE = 'multi_shot_examples/domino/instance.lp'
ENCODING = 'multi_shot_examples/domino/encodingMultiShot.lp'



class CustomControl(clingo.Control):
    def __init__(self, *asp_files):
        super().__init__()
        for file in asp_files:
            super().load(file)

    def ground(self, subprogram, *constants):
        constant_symbols = list(map(clingo.Symbol, constants))
        super().ground([(subprogram, constant_symbols)])
        
    
    def assign_external(self, name, value):
        super().assign_external(clingo.Function(name, [clingo.Symbol(value)]), True) 
    
    def release_external(self, name, value):
        super().release_external(clingo.Function(name, [value]))



if __name__ == '__main__':
    
    ctrl = CustomControl(ENCODING, INSTANCE)
    
    step, ret = 0, None


    # ctrl.ctrl.ground(('base', []))
    # pass
    ctrl.ground('base')

    ctrl.ground('updateMoves', step)
    ctrl.ground('checkIfNotOver', step)
    ctrl.assign_external('notOver', step)
    furtherMovesPossible = ctrl.solve() # know if further moves possible at T+1
    ctrl.release_external('notOver', step)
    ctrl.cleanup()

    ctrl.ground('checkIfWon', step)
    ctrl.assign_external('winning', step)
    result = ctrl.solve() # know if proponent won with T steps

    if result:
        print('SAT')
    elif not furtherMovesPossible:
        print('UNSAT')
    else: 
        ctrl.release_external('winning', step)
        ctrl.cleanup()
        step += 1 
        ctrl.ground('step', step)
        # goto line 39
    
    

    pass



    # ctrl.ground('updateMoves', step)

    #pass

