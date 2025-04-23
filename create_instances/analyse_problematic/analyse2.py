import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


ASP_FOR_ABA_INSTANCES = '/home/piotr/Dresden/multishot/flexable-asp/new/results/problematic_a=aspforaba_c=False_x=-1_o=False_s=False.csv'

TOTAL_RESULTS = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/aspforaba_results.csv'


def scatter_plots():
    categories_dict = {
        'atoms': lambda row: row.instance.split('_')[1],
        'axioms': lambda row: row.instance.split('_')[2],
        'atoms+axioms': lambda row: row.instance.split('_')[1] + '+' + row.instance.split('_')[2],
        'rules': lambda row: row.instance.split('_')[3],
        'body': lambda row: row.instance.split('_')[4],
        'rules+body': lambda row: row.instance.split('_')[3] + '+' + row.instance.split('_')[4],
    }

    for key, lambd in categories_dict.items():
        df = pd.read_csv(TOTAL_RESULTS) # start new
        df = df.sort_values(by='duration')
        df['category'] = df.apply(lambd, axis=1) # what is axis doing? 
        df['X'] = range(len(df))

        # Scatter plot with color distinction
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x='X', y='duration', hue='category', palette='Set1', s=100)

        # Labels and title
        plt.xlabel("ordinal")
        plt.ylabel("duration")
        plt.title(key)
        plt.legend(title=key)

        plt.show()
    pass



if __name__ == '__main__':
    scatter_plots()
    # df = pd.read_csv(ASP_FOR_ABA_INSTANCES)
    df = pd.read_csv(TOTAL_RESULTS)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.max_rows", None)

    # x = df[df['result'] == 'yes'][['instance', 'goal', 'result', 'duration']]
    x = df[['instance', 'goal', 'result', 'duration']]
    x = x.sort_values(by='duration')
    pass


