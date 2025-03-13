import pandas as pd

import config as cfg
import utilities as ut


OUTPUT_PATH = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/analysis/comparison.csv'
OUTPUT_PATH_TABLE = '/home/piotr/Dresden/multishot/flexable-asp/analysis/table.tex'

NON_TRIVIAL_INSTANCES_PATH = '/home/piotr/Dresden/multishot/flexable-asp/remove_trivial/instances_with_trivial.csv'


FILTER_TRIVIAL = True

def get_data(df):

    if FILTER_TRIVIAL:
        # mn = ut.get_meaningful_instances()
        nt = pd.read_csv(NON_TRIVIAL_INSTANCES_PATH)
        df = df[nt['is_trivial'] == 'no']
        pass

    total = len(df)

    timeouts = len(df[df['verdict'] == 'TIMEOUT'])
    solved = len(df) - timeouts
    incorrect = len(df[df['verdict'] == 'inc'])
    accuracy = ((solved - incorrect) / solved) * 100 # in percent
    accuracy_t = ((total - incorrect - timeouts) / total) * 100 # in percent
    time_total = df.duration.sum() / 3600
    idx_95_percentile = int(len(df) * .95)
    time_95 = df.sort_values(by='duration').iloc[:idx_95_percentile].duration.sum() / 3600


    not_timed_out = df[df['verdict'] != 'TIMEOUT']
    min_ = not_timed_out.duration.min()
    median_ = not_timed_out.duration.median()
    mean_ = not_timed_out.duration.mean()
    max_ = not_timed_out.duration.max()

    # return [timeouts, time_total, time_95, min_, median_, mean_, max_]
    return ['{:.2f}'.format(float(num)) for num in [solved, timeouts, incorrect, accuracy, accuracy_t, time_total, time_95, min_, median_, mean_, max_]]
    


if __name__ == '__main__':
    solvers_dfs = {approach: get_data(pd.read_csv(
        approach_obj.results_path)) for approach, approach_obj in cfg.APPROACHES.items()}
    df = pd.DataFrame(solvers_dfs)
    df.index = ['solved', 'timeouts', 'incorrect', 'accuracy [%]', 'accuracy t [%]', 'time_tot [h]', 'time_95 [h]', 'min [s]', 'median [s]', 'mean [s]', 'max [s]' ]
    df.to_csv(OUTPUT_PATH)
    print('Without' if FILTER_TRIVIAL else 'With', 'trivial instances')
    print(df.to_markdown())
    df.to_latex(OUTPUT_PATH_TABLE)
    
    
