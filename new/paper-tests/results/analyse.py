import pandas as pd

AF_ASPARTIX = '/home/piotr/Dresden/multishot/flexable-asp/new/paper-tests/results/af_aspartix.csv'
AF_MULTI = '/home/piotr/Dresden/multishot/flexable-asp/new/paper-tests/results/af_multi-af.csv'


if __name__ == '__main__':
    df_aspartix = pd.read_csv(AF_ASPARTIX)
    df_multi = pd.read_csv(AF_MULTI)

    df_a = df_aspartix[df_aspartix['result'].notna()]  # Rows where 'value' is NOT NaN
    df_m = df_multi[df_multi['result'].notna()]  # Rows where 'value' is NOT NaN


    merged = pd.merge(df_aspartix, df_multi, on='id', how='inner', suffixes=('_aspartix', '_multi'))

    merged_solved = merged[merged['result_aspartix'].notna() & merged['result_multi'].notna()]

    merged_solved_diff = merged_solved[merged_solved['result_aspartix'] == merged_solved['result_multi']]
    # merged_solved_diff = merged_solved[merged_solved['result_aspartix'] != merged_solved['result_multi']]

    pass