import sys
from clingo import Control, Number, Function, String


def main(instance, goal, encoding):
  ctl = Control()
  ctl.load(instance)
  ctl.load(encoding)
  ctl.ground([('base', ())])
#   goal = Function('in', [String(goal)])
  goal = Function('in', [Number(int(goal))])
  res = ctl.solve(assumptions=[(goal, True)])
  return res.satisfiable


if __name__ == '__main__':
    try:      
        _, instance, goal, encoding  = sys.argv
    except Exception as e:
        # instance = '/home/piotr/Dresden/multishot/flexable-asp/new/paper-tests/aspartix/test1.lp'
        # goal = '1'
        # goal = '2'
        # encoding = '/home/piotr/Dresden/multishot/flexable-asp/new/paper-tests/aspartix/adm.dl'
        instance = '/home/piotr/Dresden/iccma2023_results/iccma2023_benchmarks/benchmarks/asp-syntax/WS_500_16_70_50.af' 
        goal = '135' 
        encoding = '/home/piotr/Dresden/multishot/flexable-asp/new/paper-tests/aspartix/adm.dl'
    finally: 
        res = main(instance, goal, encoding)
        print(res)
    