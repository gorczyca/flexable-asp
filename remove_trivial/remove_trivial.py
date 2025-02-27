import pandas as pd
from alive_progress import alive_bar



from CustomClingoControl import CustomClingoControl

ASPFORABA_RESULTS_PATH = '/home/piotr/Dresden/multishot/flexable-asp/test/aspforaba_results.csv'

INSTANCES_DIR="/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances"

OUTPUT_PATH = '/home/piotr/Dresden/multishot/flexable-asp/remove_trivial/instances_with_trivial.csv'


def get_is_trivial(instance_path, goal):
    ctrl = CustomClingoControl(asp_files=[instance_path])
    ctrl.simple_ground('base')



    
    program = f"""goal({goal}).
    trivial :- goal({goal}), not head(_, {goal}), not assumption({goal}).
    :- not trivial.
    """
            

    ctrl.add('goalSpecific', [], program)
    ctrl.simple_ground('goalSpecific')

    return 'yes' if ctrl.solve().satisfiable else 'no'


def check_all():
    corr_results_df = pd.read_csv(ASPFORABA_RESULTS_PATH)

    is_trivial = []

    total_size = len(corr_results_df)


    with alive_bar(total_size, dual_line=True, title=f'Checking if instance is trivial...') as bar:
        for i, (index, row) in enumerate(corr_results_df.iterrows(), start=1):

            instance_path = f'{INSTANCES_DIR}/{row.instance}'
            goal = row.goal


            is_instance_trivial = get_is_trivial(instance_path, goal)
            is_trivial.append(is_instance_trivial)

            bar()


        
    corr_results_df['is_trivial'] = is_trivial
    corr_results_df.to_csv(OUTPUT_PATH)



if __name__ == '__main__':

    # instance, goal = '/home/piotr/Dresden/multishot/non_trivial.lp', 's'
    # instance, goal = '/home/piotr/Dresden/multishotflexable-asp/remove_trivial/non_trivial2.lp', 's'
    # is_trivial = get_is_trivial(instance, goal)
    # pass


    check_all()






