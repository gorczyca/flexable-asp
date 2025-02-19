from CustomClingoControl import CustomClingoControl

ENCODING = '/home/piotr/Dresden/multishot/flexable-asp/multi_shot_alt_test/simple.lp'

if __name__ == '__main__':
    ctrl = CustomClingoControl(ENCODING)

    ctrl.simple_ground('base')
    ctrl.set_models(0)

    while True:
        with ctrl.solve(yield_=True) as hnd:
            for j, m in enumerate(hnd):
                print(f'{j+1}: {m}')    
        pass

        # ctrl.add('subprog', [], ':- x(a), x(b).')
        ctrl.add('subprog', [], ':- x(_).')
        ctrl.simple_ground('subprog')