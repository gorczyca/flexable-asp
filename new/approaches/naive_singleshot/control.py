import sys, os, time, subprocess
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2])) # to import CustomClingoControl from anywhere
from CustomClingoControl import CustomClingoControl


def get_flex_asp_answer_clingo_control(instance, goal, max_move, game_over_check, logic_program_path):

    folder = Path(logic_program_path).parent
    proponent_won_check = str(folder.joinpath('proponent_won_check.lp'))
    opponent_won_check = str(folder.joinpath('opponent_won_check.lp'))

    step = 1
    horizon = max_move != -1

    while True:

        if horizon and step >= max_move:
            return 'no', None, None, None, None

        else:
            # first check if proponent won
            ctrl = CustomClingoControl(asp_files=[instance, logic_program_path, proponent_won_check], cmd_params= ['1', '-c', f'maxMove={step}', '-c', f'argGoal={goal}'])
            ctrl.ground()
            res = ctrl.solve()

            if res.satisfiable:
                return 'yes', None, None, None, None
            
            if game_over_check:
                # otherwise, check if game can be continued
                ctrl = CustomClingoControl(asp_files=[instance, logic_program_path, opponent_won_check], cmd_params= ['1', '-c', f'maxMove={step}', '-c', f'argGoal={goal}'])
                ctrl.ground()
                res = ctrl.solve()

                if not res.satisfiable:
                    return 'no', None, None, None, None
            
        step += 1



# TODO: add this option also at some point
# def get_flex_asp_answer_subprocess(instance, goal, max_move,  game_over_check, logic_program_path):
#     settings = Settings()

#     # clingo /home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl /home/piotr/Dresden/multishot/flexable-asp/new/approaches/singleshot/logicProgram.lp -c argGoal=q4 -c maxMove=30
#     command = f'{settings.clingo_path} {instance} {logic_program_path} -c argGoal={goal} -c maxMove={max_move} --quiet'

#     output = subprocess.run(command, shell=True, capture_output=True, text=True)
#     split = output.stdout.split()
#     return_value = 'yes' if 'SATISFIABLE' in split else 'no'
#     return return_value, None, None, None, None


if __name__ == '__main__':

    # this instance is satisfiable
    instance_1 = {
        'instance': '/home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl',
        'goal': 'v4' 
    }
    # unsatisfiable
    instance_2 = {
        'instance': '/home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl',
        'goal': 'c4' 
    }
    # unsatisfiable 2, takes longer
    instance_3 = {
        'instance': '/home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl',
        'goal': 'q4' 
    }
    # timeout
    instance_4 = {
        'instance': '/home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl',
        'goal': 'u3' 
    }

    # this instance is unsatisfiable

    chosen_instance = instance_2
    max_move = 30
    game_over_check = False

    logic_program_path = '/home/piotr/Dresden/multishot/flexable-asp/new/approaches/naive_singleshot/logicProgram.lp'


    answer = get_flex_asp_answer_clingo_control(chosen_instance['instance'], chosen_instance['goal'], max_move, game_over_check, logic_program_path)

    print(answer)

    # clingo /home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl /home/piotr/Dresden/multishot/flexable-asp/new/approaches/naive_singleshot/proponent_won_check.lp /home/piotr/Dresden/multishot/flexable-asp/new/approaches/naive_singleshot/logicProgram.lp 1 -c maxMove=3 -c argGoal=u3
