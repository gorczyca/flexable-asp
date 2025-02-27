# SETTINGS = {
#     'APPROACHES': {
#         'constraints': 'approaches/constraints',
#     },
#     'PYTHON_PATH': '/home/piotr/anaconda3/envs/flexable/bin/python',
#     'ASPFORABA_RESULTS_PATH': '/home/piotr/Dresden/multishot/flexable-asp/test/aspforaba_results.csv'

# }


class Settings:
    def __init__(self):

        self.approaches_path = 'approaches'
        
        self.clingo_path = '/home/piotr/anaconda3/envs/flexable/bin/clingo'
        # self.clingo_path = '/data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/clingo'
        self.python_path = '/home/piotr/anaconda3/envs/flexable/bin/python'
        # self.python_path = '/data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/python'
        self.aspforaba_results_path = '/home/piotr/Dresden/multishot/flexable-asp/test/aspforaba_results.csv'
        # self.aspforaba_results_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test/aspforaba_results.csv'
        self.instances_path = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances'
        # self.instances_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test_instances/asp_for_aba_instances'
        
        self.output_path = 'results'
        self.timeout = 600

