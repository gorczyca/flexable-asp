from CustomClingoControl import CustomClingoControl
from clingo import PropagateControl

INSTANCE = '/home/piotr/Dresden/multishot/flexable-asp/multi_shot_alt_test/addingConstraints.lp'

FAKE_CONSTRAINTS = [
    [], 
    ['b', 'c', 'd'], # :- at(3, b), at(_, c), at(_, d). at(_, b), at(3, c), at(_, d). at(_, b), at(_, c), at(3, d).
    ['a'],
    ['d','e'],
    ['b','d'],
    ['c']
    # propAss(_,at(3, b), at(_, c), at(_, d). A)
    #propRule(_,at(3, b), at(_, c), at(_, d). RId)

]

def get_constraints(id):
    chunk = FAKE_CONSTRAINTS[:id]
    for cstr in chunk:
        if cstr:
            yield ':- ' + ", ".join([f'at(_, {x})' for x in cstr]) + '.'

def get_flex_asp_answer():
    # start_time = time.time()
    ctrl = CustomClingoControl(INSTANCE)



    ctrl.simple_ground('base')

    step = 1
    return_value = None

    # ctrl.add('constraint', [], f':- at(_, a).') ## how to ground it then?
    # ctrl.simple_ground('constraint')

    ctrl.set_models(0) # enumerate all

    while True:
        print(f'step {step}')
        ctrl.simple_ground('updateState', step)

        constraints = list(get_constraints(step))
        if constraints:
            print('cstr:\n' + "\n".join(constraints))
        if len(constraints) > 0:
            ctrl.add('someConstr', [], ' '.join(constraints))
            ctrl.simple_ground('someConstr')

        # important: ground the constraints with a wildcard BEFORE grounding new step, that the wildcard should also cover!
         

        with ctrl.solve(yield_=True) as hnd:
            for m in hnd:
                print(m)                



        step += 1



        # if step == 1:
        #     # ctrl.add('constraint', [], f':- at(_, i), at(_, a).') 
        #     # ctrl.ground('constraint')
        #     ctrl.add('someConstr', [], ':- used(_, i), used(_, a).')
        #     ctrl.simple_ground('someConst')



if __name__ == '__main__':
    get_flex_asp_answer()
    pass