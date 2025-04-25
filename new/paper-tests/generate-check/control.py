from clingo import Control, Number, Function
import sys


def main(instance, goal, encoding):
  ctl = Control(['--warn=none'])
  ctl.load(instance)
  ctl.load(encoding)
  ctl.add('base', [], f'g({goal}).')
  ctl.ground([('base', ())])
  step = 0
  while True:
    ctl.ground([('updateState', [Number(step)])])
    p_win = Function('end', [Number(step), Function("p")])
    res = ctl.solve(assumptions=[(p_win, True)])
    if res.satisfiable:
        return True, step
    o_win = Function('end', [Number(step), Function("o")])
    res = ctl.solve(assumptions=[(o_win, False)])
    if res.unsatisfiable:
        return False, step
    step += 1
    ctl.ground([('step', [Number(step)])])


if __name__ == '__main__':
    try:      
        _, instance, goal, _, encoding  = sys.argv
        # print(instance, goal, encoding)
    except Exception as e:
        instance = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy07.pl'
        goal = 'u2' 
        encoding = '/home/piotr/Dresden/multishot/flexable-asp/new/approaches/assumptions/logicProgram.lp'
    finally: 
        res, step = main(instance, goal, encoding)
        print(res, step, None, None, None)
    