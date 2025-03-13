class Approach:
    def __init__(self, name, results_path):
        self.name = name
        self.results_path = results_path


APPROACHES = {
    'aspforaba': Approach('aspforaba', '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/analysis/outputs/aspforaba_outputs.csv'),
    # 'abagraph': Approach('abagraph',''),
    'flexable': Approach('flexable', '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/flexable/flexable.csv'),
    # 'assumptions+con': Approach('assumptions+constraints', '/home/piotr/Dresden/multishot/results-assumptions-externals-constraints/assumptions_constr.csv'),
    # 'externals+con': Approach('externals+constraints', '/home/piotr/Dresden/multishot/results-assumptions-externals-constraints/externals_constr.csv'),
    # 'assumptions': Approach('assumptions', '/home/piotr/Dresden/multishot/results-assumptions-externals-constraints/assumptions_noconstr.csv'),
    # 'externals': Approach('externals', '/home/piotr/Dresden/multishot/results-assumptions-externals-constraints/externals_noconstr.csv'),
    # 
    # 'o-5-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=5_s=True.csv'),
    'o-5': Approach('o-5', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=5_s=False.csv'),
    # 'o-10-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=10_s=True.csv'),
    'o-10': Approach('o-10', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=10_s=False.csv'),
    # 'o-15-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=15_s=True.csv'),
    'o-15': Approach('o-15', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=15_s=False.csv'),
    # 'o-20-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=20_s=True.csv'),
    'o-20': Approach('o-20', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=20_s=False.csv'),
    # 'o-25-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=25_s=True.csv'),
    'o-25': Approach('o-25', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=25_s=False.csv'),
    # 'o-30-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=30_s=True.csv'),
    'o-30': Approach('o-30', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=30_s=False.csv'),
    # 'o-50-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=50_s=True.csv'),
    'o-50': Approach('o-50', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=50_s=False.csv'),
    # 'o-75-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=75_s=True.csv'),
    'o-75': Approach('o-75', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=75_s=False.csv'),
    # 'o-100-s': Approach('externals', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=100_s=True.csv'),
    'o-100': Approach('o-100', '/home/piotr/Dresden/multishot/results-singleshot/a=singleshot_c=False_x=100_s=False.csv'),
}


# naive approaches
# on
# APPROACHES = {
#     'on-max=5-check': Approach('on-max=5-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=5_o=True_s=False.csv'),
#     'on-max=5': Approach('on-max=5', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=5_o=False_s=False.csv'),
#     'on-max=10-check': Approach('on-max=10-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=10_o=True_s=False.csv'),
#     'on-max=10': Approach('on-max=10', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=10_o=False_s=False.csv'),
#     'on-max=15-check': Approach('on-max=15-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=15_o=True_s=False.csv'),
#     'on-max=15': Approach('on-max=15', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=15_o=False_s=False.csv'),
#     'on-max=20-check': Approach('on-max=20-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=20_o=True_s=False.csv'),
#     'on-max=20': Approach('on-max=20', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=20_o=False_s=False.csv'),
#     'on-max=25-check': Approach('on-max=25-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=25_o=True_s=False.csv'),
#     'on-max=25': Approach('on-max=25', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=25_o=False_s=False.csv'),
#     'on-max=30-check': Approach('on-max=30-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=30_o=True_s=False.csv'),
#     'on-max=30': Approach('on-max=30', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=30_o=False_s=False.csv'),
#     'on-max=40-check': Approach('on-max=40-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=40_o=True_s=False.csv'),
#     'on-max=40': Approach('on-max=40', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=40_o=False_s=False.csv'),
#     'on-max=50-check': Approach('on-max=50-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=50_o=True_s=False.csv'),
#     'on-max=50': Approach('on-max=50', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=50_o=False_s=False.csv'),
#     'on-max=75-check': Approach('on-max=75-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=75_o=True_s=False.csv'),
#     'on-max=75': Approach('on-max=75', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=75_o=False_s=False.csv'),
#     'on-max=100-check': Approach('on-max=100-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=100_o=True_s=False.csv'),
#     'on-max=100': Approach('on-max=100', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=naive_singleshot_c=False_x=100_o=False_s=False.csv'),
# }

# multi shot assumptions approaches
# ma
# APPROACHES = {
#     'ma-max=5-check': Approach('ma-max=5-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=5_o=True_s=False.csv'),
#     'ma-max=5': Approach('ma-max=5', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=5_o=False_s=False.csv'),
#     'ma-max=10-check': Approach('ma-max=10-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=10_o=True_s=False.csv'),
#     'ma-max=10': Approach('ma-max=10', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=10_o=False_s=False.csv'),
#     'ma-max=15-check': Approach('ma-max=15-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=15_o=True_s=False.csv'),
#     'ma-max=15': Approach('ma-max=15', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=15_o=False_s=False.csv'),
#     'ma-max=20-check': Approach('ma-max=20-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=20_o=True_s=False.csv'),
#     'ma-max=20': Approach('ma-max=20', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=20_o=False_s=False.csv'),
#     'ma-max=25-check': Approach('ma-max=25-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=25_o=True_s=False.csv'),
#     'ma-max=25': Approach('ma-max=25', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=25_o=False_s=False.csv'),
#     'ma-max=30-check': Approach('ma-max=30-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=30_o=True_s=False.csv'),
#     'ma-max=30': Approach('ma-max=30', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=30_o=False_s=False.csv'),
#     'ma-max=40-check': Approach('ma-max=40-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=40_o=True_s=False.csv'),
#     'ma-max=40': Approach('ma-max=40', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=40_o=False_s=False.csv'),
#     'ma-max=50-check': Approach('ma-max=50-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=50_o=True_s=False.csv'),
#     'ma-max=50': Approach('ma-max=50', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=50_o=False_s=False.csv'),
#     'ma-max=75-check': Approach('ma-max=75-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=75_o=True_s=False.csv'),
#     'ma-max=75': Approach('ma-max=75', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=75_o=False_s=False.csv'),
#     'ma-max=100-check': Approach('ma-max=100-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=100_o=True_s=False.csv'),
#     'ma-max=100': Approach('ma-max=100', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=assumptions_c=False_x=100_o=False_s=False.csv'),
# }

# multi shot externals approaches
# me
# APPROACHES = {
#     'me-max=5-check': Approach('me-max=5-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=5_o=True_s=False.csv'),
#     'me-max=5': Approach('me-max=5', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=5_o=False_s=False.csv'),
#     'me-max=10-check': Approach('me-max=10-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=10_o=True_s=False.csv'),
#     'me-max=10': Approach('me-max=10', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=10_o=False_s=False.csv'),
#     'me-max=15-check': Approach('me-max=15-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=15_o=True_s=False.csv'),
#     'me-max=15': Approach('me-max=15', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=15_o=False_s=False.csv'),
#     'me-max=20-check': Approach('me-max=20-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=20_o=True_s=False.csv'),
#     'me-max=20': Approach('me-max=20', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=20_o=False_s=False.csv'),
#     'me-max=25-check': Approach('me-max=25-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=25_o=True_s=False.csv'),
#     'me-max=25': Approach('me-max=25', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=25_o=False_s=False.csv'),
#     'me-max=30-check': Approach('me-max=30-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=30_o=True_s=False.csv'),
#     'me-max=30': Approach('me-max=30', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=30_o=False_s=False.csv'),
#     'me-max=40-check': Approach('me-max=40-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=40_o=True_s=False.csv'),
#     'me-max=40': Approach('me-max=40', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=40_o=False_s=False.csv'),
#     'me-max=50-check': Approach('me-max=50-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=50_o=True_s=False.csv'),
#     'me-max=50': Approach('me-max=50', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=50_o=False_s=False.csv'),
#     'me-max=75-check': Approach('me-max=75-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=75_o=True_s=False.csv'),
#     'me-max=75': Approach('me-max=75', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=75_o=False_s=False.csv'),
#     'me-max=100-check': Approach('me-max=100-check', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=100_o=True_s=False.csv'),
#     'me-max=100': Approach('me-max=100', '/home/piotr/Dresden/multishot/results-naive-no-2nd-check/a=externals_c=False_x=100_o=False_s=False.csv'),
# }







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
