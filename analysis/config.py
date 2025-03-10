class Approach:
    def __init__(self, name, results_path):
        self.name = name
        self.results_path = results_path


APPROACHES = {
    'aspforaba': Approach('aspforaba', '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/analysis/outputs/aspforaba_outputs.csv'),
    # 'abagraph': Approach('abagraph',''),
    'flexable': Approach('flexable', '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/flexable/flexable.csv'),
    'assumptions+con': Approach('assumptions+constraints', '/home/piotr/Dresden/multishot/results-assumptions-externals-constraints/assumptions_constr.csv'),
    'externals+con': Approach('externals+constraints', '/home/piotr/Dresden/multishot/results-assumptions-externals-constraints/externals_constr.csv'),
    'assumptions': Approach('assumptions', '/home/piotr/Dresden/multishot/results-assumptions-externals-constraints/assumptions_noconstr.csv'),
    'externals': Approach('externals', '/home/piotr/Dresden/multishot/results-assumptions-externals-constraints/externals_noconstr.csv'),
    # 
    # 'single-5-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=5_s=True.csv'),
    'single-5': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=5_s=False.csv'),
    # 'single-10-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=10_s=True.csv'),
    'single-10': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=10_s=False.csv'),
    # 'single-15-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=15_s=True.csv'),
    'single-15': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=15_s=False.csv'),
    # 'single-20-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=20_s=True.csv'),
    'single-20': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=20_s=False.csv'),
    # 'single-25-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=25_s=True.csv'),
    'single-25': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=25_s=False.csv'),
    # 'single-30-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=30_s=True.csv'),
    'single-30': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=30_s=False.csv'),
    # 'single-50-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=50_s=True.csv'),
    'single-50': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=50_s=False.csv'),
    # 'single-75-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=75_s=True.csv'),
    'single-75': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=75_s=False.csv'),
    # 'single-100-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=100_s=True.csv'),
    'single-100': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=100_s=False.csv'),
}

COLORS = [
    "#1f77b4",  # Blue
    "#ff7f0e",  # Orange
    "#2ca02c",  # Green
    "#d62728",  # Red
    "#9467bd",  # Purple
    "#8c564b",  # Brown
    "#e377c2",  # Pink
    "#7f7f7f",  # Gray
    "#bcbd22",  # Yellow-Green
    "#17becf",  # Cyan
    "#ff5733",  # Deep Orange
    "#5e3c99",  # Dark Purple
    "#1a85ff",  # Vivid Blue
    "#d41159",  # Magenta-Red
    "#44aa99",  # Teal
]


MARKERS = [
    '1',
    '2',
    '3',
    '4',
    'x',
    'o'
]
