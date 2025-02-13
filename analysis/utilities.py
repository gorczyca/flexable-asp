# todo: should've used kwargs

import config
import pandas as pd

def filter_timeouts(df, column_name='verdict', timeout_val='TIMEOUT'):
    return df[df[column_name] != timeout_val]

def sort(df, column_name='duration', index_column='int_index'):
    df = df.sort_values(by=column_name)
    df[index_column] = range(len(df))
    return df, index_column, column_name




def get_meaningful_instances():
    df = pd.read_csv(config.APPROACHES['flexable'].results_path)
    return df[df['steps_obtained'].notna()]