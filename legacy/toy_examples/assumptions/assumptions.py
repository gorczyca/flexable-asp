import sys

from clingo import Function, Number

CUSTOM_CLINGO_CONTROL_PATH = '/home/piotr/Dresden/multishot/flexable-asp/new'
sys.path.append(CUSTOM_CLINGO_CONTROL_PATH)

from CustomClingoControl import CustomClingoControl

# ENCODING_PATH = '/home/piotr/Dresden/multishot/flexable-asp/legacy/toy_examples/assumptions/assumptions.lp'
ENCODING_PATH = '/home/piotr/Dresden/multishot/flexable-asp/legacy/toy_examples/assumptions/assumptions-2.lp'

if __name__ == '__main__':
    ctrl = CustomClingoControl(ENCODING_PATH)

    ctrl.simple_ground('base')
    ctrl.set_models(0)


    assumptions = []
    # assumptions = [(Function('a', [], True), True)]
    # assumptions = [(Function('x', [Function('b', [], True)], True), False)]
    # assumptions = [(Function('x', [Function('b')]), True)]

    # assumptions-2
    # assumptions = [(Function('x', [Number(2)], True), False)]
    assumptions = [(Function('x', [Number(2)]), False)]
    # assumptions = [(Function('x', [Number(2)], True), False)]
    while True:
        # with ctrl.solve(yield_=True, assumptions=assumptions) as hnd:
        with ctrl.solve(yield_=True, assumptions=assumptions) as hnd:
            for j, m in enumerate(hnd):
                print(f'{j+1}: {m}')    
        # pass
        break

        # ctrl.add('subprog', [], ':- x(a), x(b).')
        # ctrl.add('subprog', [], ':- x(_).')
        # ctrl.simple_ground('subprog')

    pass



