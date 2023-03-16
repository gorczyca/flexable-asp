import pandas as pd
import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from cycler import cycler

# plt.style.use('seaborn')
matplotlib.rcParams['font.family'] = 'serif'

import config as cfg
import utilities as ut

# OUTPUT_PATH = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/analysis/cactus_plot.pdf'
OUTPUT_PATH = '/home/piotr/test/newest_ubuntu_data/Dresden/flexABle/flexable_asp/repo/analysis/cactus_plot.png'



# DURATION_COLUMN = 'duration_sec'
# INDEX_COLUMN = 'int_index'


def plot_cactus_plot_reversed(solvers_dfs):

    ax = None
    for i, (solver, solver_df) in enumerate(solvers_dfs.items()):
        df, id_col, val_col = ut.sort(solver_df)

        # connect with line
        ax = df.plot(y=id_col, x=val_col, color=cfg.COLORS[i], marker='o', ax=ax, label=solver)
        # ax = df.plot(y=id_col, x=val_col, color=cfg.COLORS[i], marker=cfg.MARKERS[i], ax=ax, label=solver)
        # just a scatter plot
        #MARKERS = group_df.plot(kind='scatter', y=INDEX_COLUMN, x=DURATION_COLUMN, color=ct.COLORS_DICT[solver], marker=ct.MARKERS_DICT[solver], ax=ax, label=solver)


        # Add grid
        ax.grid(color='grey', linestyle=':')

    ax.set_ylabel('')
    ax.set_xlabel('')

    handles, labels = ax.get_legend_handles_labels()

    # Sort by #solved instances, but always keep vbest
    handles, labels = zip(
        *sorted([*zip(handles, labels)], key=lambda handle_label: solvers_dfs[handle_label[1]].shape[0], reverse=True))

    ax.legend(handles=handles, labels=labels)

    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)

    plt.tight_layout()

    # these x, y values are dependant on the size of graph
    plt.text(-12, -100, 'n[#]/t[s]')
    plt.savefig(OUTPUT_PATH)
    plt.show()



if __name__ == '__main__':
    # entire dataframe


    solvers_dfs = {approach: ut.filter_timeouts(pd.read_csv(approach_obj.results_path)) for approach, approach_obj in cfg.APPROACHES.items()}

    plot_cactus_plot_reversed(solvers_dfs)
    

