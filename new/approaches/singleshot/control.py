import sys, os, time, subprocess
from pathlib import Path


sys.path.append(str(Path(__file__).parents[2])) # to import CustomClingoControl from anywhere
from CustomClingoControl import CustomClingoControl
from config import Settings

def get_flex_asp_answer_clingo_control(instance, goal, maxMove, logic_program_path):
    # start_time = time.time()
    ctrl = CustomClingoControl(asp_files=[instance, logic_program_path], cmd_params= ['1', '-c', f'maxMove={maxMove}', '-c', f'argGoal={goal}'])
    ctrl.ground()
    res = ctrl.solve()
    return_value = 'yes' if res.satisfiable else 'no'
    return return_value, None, None, None, None


def get_flex_asp_answer_subprocess(instance, goal, max_move, logic_program_path):


    settings = Settings()

    # clingo /home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl /home/piotr/Dresden/multishot/flexable-asp/new/approaches/singleshot/logicProgram.lp -c argGoal=q4 -c maxMove=30
    command = f'{settings.clingo_path} {instance} {logic_program_path} -c argGoal={goal} -c maxMove={max_move} --quiet'

    # TODO:
    # command = [
    #     settings.clingo_path,
    #     instance,
    #     logic_program_path,
    #     '-c', f'argGoal={goal}',
    #     '-c', f'maxMove={max_move}',
    #     '--quiet',
    # ]
    
    # output = subprocess.check_output(args=[command], shell=True, stderr=subprocess.STDOUT, text=True)
    output = subprocess.run(command, shell=True, capture_output=True, text=True)
    split = output.stdout.split()
    return_value = 'yes' if 'SATISFIABLE' in split else 'no'
    return return_value, None, None, None, None


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

    chosen_instance = instance_4
    max_move = 30

    logic_program_path = '/home/piotr/Dresden/multishot/flexable-asp/new/approaches/singleshot/logicProgram.lp'

    # get_flex_asp_answer(chosen_instance['instance'], chosen_instance['goal'], max_move, logic_program_path)
    answer = get_flex_asp_answer_subprocess(chosen_instance['instance'], chosen_instance['goal'], max_move, logic_program_path)
    

    print(answer)
    # clingo /home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl /home/piotr/Dresden/multishot/flexable-asp/new/approaches/singleshot/logicProgram.lp -c argGoal=q4 -c maxMove=30
