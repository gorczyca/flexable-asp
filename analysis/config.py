class Approach:
    def __init__(self, name, results_path):
        self.name = name
        self.results_path = results_path


APPROACHES = {
    'aspforaba': Approach('aspforaba', '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/analysis/outputs/aspforaba_outputs.csv'),
    # 'abagraph': Approach('abagraph',''),
    'flexable': Approach('flexable', '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/flexable/flexable.csv'),
    'flexASP': Approach('flexASP', '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/multi_shot/multi_shot_1.csv'),
    # 'flexASP1': Approach('flexable',''),
    # 'flexASP2': Approach('flexable',''),
    # 'flexASPAlt': Approach('flexable',''),
    'flexASPAlt1': Approach('flexASPAlt1', '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/multi_shot_alt/multi_shot_alt.csv'),
    'flexASPAlt2': Approach('flexASPAlt2', '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/multi_shot_alt_full_strategy/multi_shot_alt_strat.csv'),
}

COLORS = [
    '#6EB5FF',
    '#612700',
    '#FFB5E8',
    '#DCD3FF',
    '#B28DFF',
    '#AFF8D8',
    # 'black',
    '#612700',
]

MARKERS = [
    '1',
    '2',
    '3',
    '4',
    'x',
    'o'
]
