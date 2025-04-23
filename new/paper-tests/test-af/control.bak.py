import sys
from clingo import Control, Number, Function

def on_model(model):
    print("Answer:")
    for atom in model.symbols(shown=True):
        print(f"  {atom}")


def main(instance, goal, encoding):
  ctl = Control(['--warn=none'])
  ctl.load(instance)
  ctl.load(encoding)
  ctl.add('base', [], f'g({goal}).')
  ctl.ground([('base', ())])
  step = 0
  while True:
    ctl.ground([('updateState', [Number(step)])])
    ctl.solve(on_model=on_model)
    p_win = Function('end', [Number(step), Function("p")])
    res = ctl.solve(assumptions=[(p_win, True)], on_model=on_model)
    if res.satisfiable:
        return True
    o_win = Function('end', [Number(step), Function("o")])
    res = ctl.solve(assumptions=[(o_win, False)], on_model=on_model)
    if res.unsatisfiable:
        return False
    step += 1
    ctl.ground([('step', [Number(step)])])


if __name__ == '__main__':
    try:      
        _, instance, goal, encoding  = sys.argv
    except Exception as e:

        instance = '/home/piotr/Dresden/multishot/flexable-asp/new/af-test-instances/instances/Medium-result_b22.af'
        goal = '1014'
        encoding = '/home/piotr/Dresden/multishot/flexable-asp/new/paper-tests/test-af/encoding.lp'

        # 4,Medium-result_b22.af,1014,True,4.46 should be true, is False

        pass
    finally: 
        res = main(instance, goal, encoding)
        print(res)
    

