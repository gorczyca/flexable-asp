
# INSTANCE_GOAL_CSV = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/iccma2023.csv'
# OUTPUT_PATH = '/home/piotr/Dresden/multishot/flexable-asp/test_instances'
# OUTPUT_FILENAME = 'aspforaba_results.csv'

class Settings:
    def __init__(self):

        self.approaches_path = 'approaches'

        self.output_path = 'results'
        self.timeout = 600

        self.hpc = True
        # self.hpc = False
        self.iccma_instances = True

        if self.hpc:
        ### HPC
            self.clingo_path = '/data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/clingo'
            self.python_path = '/data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/python'
            self.aspforaba_results_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test/aspforaba_results.csv'

            self.initial_instance_goal_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test_instances/iccma2023.csv'
            self.initial_outputs_paths = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test_instances/aspforaba_results.csv'

            if self.iccma_instances:
                # iccma instances
                self.instances_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test_instances/iccma2023_instances'
            else: 
                # easy instances
                self.instances_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test_instances/asp_for_aba_instances'

        else:
            ######## local
            self.clingo_path = '/home/piotr/anaconda3/envs/flexable/bin/clingo'
            self.python_path = '/home/piotr/anaconda3/envs/flexable/bin/python'
            self.aspforaba_results_path = '/home/piotr/Dresden/multishot/flexable-asp/test/aspforaba_results.csv'

            self.initial_instance_goal_path = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/iccma2023.csv'
            self.initial_outputs_paths = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/aspforaba_results.csv'

            if self.iccma_instances:
                # iccma instances
                self.instances_path = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/iccma2023_instances'
            else:
                # easy instances
               self.instances_path = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances'



