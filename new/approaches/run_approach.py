import sys

from assumptions.control import get_flex_asp_answer as get_flex_asp_answer_assumptions 
from externals.control import get_flex_asp_answer as get_flex_asp_answer_externals


if __name__ == '__main__':
    _, instance, goal, use_constraints, approach, logic_program_path  = sys.argv

    # use_constraints = bool(use_constraints)
    use_constraints = use_constraints == 'True'

    if approach == 'assumptions':
        results = get_flex_asp_answer_assumptions(instance, goal, use_constraints, logic_program_path)
    elif approach == 'externals':
        results = get_flex_asp_answer_externals(instance, goal, use_constraints, logic_program_path)
    
    # res is a tuple, unpack it
    print(" ".join(map(str, results)))