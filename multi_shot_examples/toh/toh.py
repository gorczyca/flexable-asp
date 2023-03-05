import clingo


PROGRAMS = ['multi_shot_examples/toh/tohE.lp', 'multi_shot_examples/toh/tohI.lp']


def get(val, default):
    return val if val != None else default


if __name__ == '__main__':

    # load programs
    ctrl = clingo.Control()    
    for prg in PROGRAMS:
        ctrl.load(prg)

    imin = get(ctrl.get_const("imin"), 1)
    imax = ctrl.get_const("imax")
    istop = get(ctrl.get_const("istop"), "SAT")
    
    step, ret = 0, None
    while (
        (imax is None or step < imax) and (step == 0 or step < imin or 
            (istop == 'SAT' and not ret.satisfiable) or 
            (istop == "UNSAT" and not ret.unsatisfiable) or 
            (istop == "UNKNOWN" and not ret.unknown))):
        print(f'step: {step}')
        parts = []
        parts.append(("check", [clingo.symbol.Number(step)]))
        if step > 0:
            ctrl.release_external(clingo.Function("query", [clingo.symbol.Number(step-1)]))
            parts.append(("step", [clingo.symbol.Number(step)]))
            ctrl.cleanup()
        else:
            parts.append(("base", []))
        ctrl.ground(parts)
        ctrl.assign_external(clingo.Function("query", [clingo.symbol.Number(step)]), True)
        ret, step = ctrl.solve(), step+1
