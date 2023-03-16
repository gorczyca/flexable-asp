import pandas as pd

import config as cfg
import utilities as ut


OUTPUT_PATH = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/analysis/comparison.csv'


def get_data(df):
    timeouts = len(df[df['verdict'] == 'TIMEOUT'])
    time_total = df.duration.sum() / 3600
    idx_95_percentile = int(len(df) * .95)
    time_95 = df.sort_values(by='duration').iloc[:idx_95_percentile].duration.sum() / 3600

    not_timed_out = df[df['verdict'] != 'TIMEOUT']
    min_ = not_timed_out.duration.min()
    median_ = not_timed_out.duration.median()
    mean_ = not_timed_out.duration.mean()
    max_ = not_timed_out.duration.max()

    # return [timeouts, time_total, time_95, min_, median_, mean_, max_]
    return ['{:.2f}'.format(float(num)) for num in [timeouts, time_total, time_95, min_, median_, mean_, max_]]
    


if __name__ == '__main__':
    solvers_dfs = {approach: get_data(pd.read_csv(
        approach_obj.results_path)) for approach, approach_obj in cfg.APPROACHES.items()}
    df = pd.DataFrame(solvers_dfs)
    df.index = ['timeouts', 'time_tot [h]', 'time_95 [h]', 'min [s]', 'median [s]', 'mean [s]', 'max [s]' ]
    df.to_csv(OUTPUT_PATH)
    print(df.to_markdown())
    
    
