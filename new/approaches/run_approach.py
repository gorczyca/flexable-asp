import sys, argparse
from pathlib import Path

# from assumptions.control import get_flex_asp_answer as get_flex_asp_answer_assumptions 
# from externals.control import get_flex_asp_answer as get_flex_asp_answer_externals
import externals.control as externals
import assumptions.control as assumptions
import singleshot.control as singleshot

import aspforaba.control as aspforaba

sys.path.append(str(Path(__file__).parents[1])) # to import CustomArgumentParser from anywhere
from CustomArgumentParser import CustomParser

if __name__ == '__main__':
    parser = CustomParser()
    args = parser.parse_args()

    # _, instance, goal, use_constraints, approach, logic_program_path  = sys.argv

    # use_constraints = bool(use_constraints)
    # use_constraints = use_constraints == 'True'

    if args.approach == 'assumptions':
        results = assumptions.get_flex_asp_answer(args.instance, args.goal, args.constraints, args.logic_program_path)
    elif args.approach == 'externals':
        results = externals.get_flex_asp_answer(args.instance, args.goal, args.constraints, args.logic_program_path)
    elif args.approach == 'singleshot' and args.subprocess:
        results = singleshot.get_flex_asp_answer_subprocess(args.instance, args.goal, args.max_moves, args.logic_program_path)
    elif args.approach == 'singleshot' and not args.subprocess:
        results = singleshot.get_flex_asp_answer_clingo_control(args.instance, args.goal, args.max_moves, args.logic_program_path)
    elif args.approach == 'aspforaba':
        results = aspforaba.get_aspforaba_answer(args.instance, args.goal)
    
    # res is a tuple, unpack it
    print(" ".join(map(str, results)))