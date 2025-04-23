import sys

import pandas as pd


TIMED_OUT = '/home/piotr/Dresden/multishot/flexable-asp/create_instances/iccma2023_timeouts.csv'

COMPETITION_INSTANCES_PATH = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/iccma2023_instances'


# additional paths
PATHS = [
  '/home/piotr/Dresden/multishot/flexable-asp/new', # CUSTOM_CLINGO_CONTROL_PATH
  '/home/piotr/Dresden/multishot/flexable-asp/new/approaches/aspforaba' # ASPFORABA_PATH
]

for p in PATHS:
    sys.path.append(p)



from CustomClingoControl import CustomClingoControl
from control import get_aspforaba_answer





def analyse():
    timed_out_df = pd.read_csv(TIMED_OUT)

    outputs_df = pd.DataFrame(columns=['id', 'instance', 'goal', 'result', 'duration', 'verdict'])

    
    for _, (_, row) in enumerate(timed_out_df.iterrows(), start=1):
        
        instance_path = f'{COMPETITION_INSTANCES_PATH}/{row.instance}'
        pass


if __name__ == '__main__':
    analyse()