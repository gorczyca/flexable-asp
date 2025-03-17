import sys

import pandas as pd
from alive_progress import alive_bar


CUSTOM_CLINGO_CONTROL_PATH = '/home/piotr/Dresden/multishot/flexable-asp/new'
sys.path.append(CUSTOM_CLINGO_CONTROL_PATH)

from CustomClingoControl import CustomClingoControl

# RELEVANT_LOGIC_PROGRAM_PATH = '/home/piotr/Dresden/multishot/flexable-asp/legacy/toy_examples/relevant_subframework/relevant.lp'
RELEVANT_LOGIC_PROGRAM_PATH = '/home/piotr/Dresden/multishot/flexable-asp/legacy/toy_examples/relevant_subframework/relevant2.lp'

INSTANCES = 'iccma2023'
# INSTANCES = 'asp_for_aba'



INSTANCES_GOAL_PATH = f'/home/piotr/Dresden/multishot/flexable-asp/test_instances/{INSTANCES}_framework_goal.csv'
# only have non trivial ones
INSTANCES_PATH = f'/home/piotr/Dresden/multishot/flexable-asp/test_instances/{INSTANCES}_instances'
OUTPUT_PATH = f'/home/piotr/Dresden/multishot/flexable-asp/legacy/toy_examples/relevant_subframework/{INSTANCES}_relevant2.csv'


def get_relevant_stats(instance_path, instance_name, goal):
    ctrl = CustomClingoControl(asp_files=[instance_path, RELEVANT_LOGIC_PROGRAM_PATH])

    ctrl.add_base(f'goal({goal}).')
    ctrl.simple_ground('base')

    with ctrl.solve(yield_=True) as handle:
        for model in handle:
            model_str = str(model.symbols(shown=True))
            # Remove the square brackets and split into individual components
            components = model_str.strip('[]').split(', ')

            # Use dictionary comprehension to extract key-value pairs
            data = {item.split('(')[0]: int(item.split('(')[1].strip(')')) for item in components}
            data['relevantPerc'] = round(data['worstCaseRelevant']/data['worstCase'], 2)
            
            data['instance'] = instance_name
            data['goal'] = goal
            return data


if __name__ == '__main__':
    
    instance_goal_df = pd.read_csv(INSTANCES_GOAL_PATH)
    total_size = len(instance_goal_df)

    data = []

    with alive_bar(total_size, dual_line=True, title=f'Relevant subframeworks: {INSTANCES}') as bar:
        for i, (_, row) in enumerate(instance_goal_df.iterrows(), start=1):
            inst_path = f'{INSTANCES_PATH}/{row.instance}'
            
            res = get_relevant_stats(inst_path, row.instance, row.goal)
            data.append(res)
            bar()

    df = pd.DataFrame(data)
    df.index = df.index + 1 
    df.to_csv(OUTPUT_PATH, index=True, index_label='id')

    # df.drop(columns=["id"]).describe().round(2)

