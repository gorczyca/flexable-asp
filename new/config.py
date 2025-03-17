
# INSTANCE_GOAL_CSV = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/iccma2023.csv'
# OUTPUT_PATH = '/home/piotr/Dresden/multishot/flexable-asp/test_instances'
# OUTPUT_FILENAME = 'aspforaba_results.csv'

class Settings:
    def __init__(self):

        self.approaches_path = 'approaches'

        self.output_path = 'results'
        self.timeout = 600

        # self.hpc = True
        self.hpc = False
        # self.iccma_instances = True
        # self.instances = 'iccma' # 'easy' 'problematic'
        # self.instances = 'iccma' # 'easy' 'problematic'
        # self.instances = 'problematic' # 'easy' 'problematic' 'loosely_connected'
        self.instances = 'loosely_connected' # 'easy' 'problematic' 'loosely_connected'

        if self.hpc:
        ### HPC
            self.clingo_path = '/data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/clingo'
            self.python_path = '/data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/python'
            # self.correct_results_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test/aspforaba_results.csv'

            self.initial_instance_goal_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test_instances/iccma2023.csv'
            self.initial_outputs_paths = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test_instances/aspforaba_results.csv'

            if self.instances == 'iccma':
                # iccma instances
                # TODO
                self.correct_results_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test/aspforaba_results.csv'
                self.instances_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test_instances/iccma2023_instances'
            elif self.instances == 'easy': 
                # easy instances
                # TODO
                self.correct_results_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test/aspforaba_results.csv'
                self.instances_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/test_instances/asp_for_aba_instances'
            elif self.instances == 'problematic':
                self.correct_results_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/create_instances/stats.csv'
                self.instances_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/create_instances/instances'
            elif self.instances == 'loosely_connected':
                self.correct_results_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/create_big_instances/inst_goal.csv'
                self.instances_path = '/data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/create_big_instances/instances'
                

        else:
            ######## local
            self.clingo_path = '/home/piotr/anaconda3/envs/flexable/bin/clingo'
            self.python_path = '/home/piotr/anaconda3/envs/flexable/bin/python'

            self.initial_instance_goal_path = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/iccma2023.csv'
            self.initial_outputs_paths = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/aspforaba_results.csv'

            if self.instances == 'iccma':
                # iccma instances
                # TODO 
                self.correct_results_path = '/home/piotr/Dresden/multishot/flexable-asp/test/aspforaba_results.csv'
                self.instances_path = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/iccma2023_instances'
            elif self.instances == 'easy': 
                # easy instances
                # TODO 
               self.correct_results_path = '/home/piotr/Dresden/multishot/flexable-asp/test/aspforaba_results.csv'                
               self.instances_path = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances'
            elif self.instances == 'problematic':
                self.correct_results_path = '/home/piotr/Dresden/multishot/flexable-asp/create_instances/stats.csv'
                self.instances_path = '/home/piotr/Dresden/multishot/flexable-asp/create_instances/instances'
                
            elif self.instances == 'loosely_connected':
                self.correct_results_path = '/home/piotr/Dresden/multishot/flexable-asp/create_big_instances/inst_goal.csv'
                self.instances_path = '/home/piotr/Dresden/multishot/flexable-asp/create_big_instances/instances'
                


