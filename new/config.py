# SETTINGS = {
#     'APPROACHES': {
#         'constraints': 'approaches/constraints',
#     },
#     'PYTHON_PATH': '/home/piotr/anaconda3/envs/flexable/bin/python',
#     'ASPFORABA_RESULTS_PATH': '/home/piotr/Dresden/multishot/flexable-asp/test/aspforaba_results.csv'

# }


class Settings:
    def __init__(self):
        self.approaches = {
            'constraints': 'approaches/constraints',
            'constraints-assumptions': 'approaches/constraints-assumptions'
        }
        self.python_path = '/home/piotr/anaconda3/envs/flexable/bin/python'
        self.aspforaba_results_path = '/home/piotr/Dresden/multishot/flexable-asp/test/aspforaba_results.csv'
        self.output_path = 'results'
        self.instances_path = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/aba-experiments-new/instances/asp_for_aba_instances'
        self.timeout = 600

