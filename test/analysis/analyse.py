import pandas as pd


DEFAULT_ENCODING_RESULTS = 'test/def_15_600.csv'
INCREMENTAL_ENCODING_RESULTS = 'test/inc_15_600.csv'


if __name__ == '__main__':
    d = pd.read_csv(DEFAULT_ENCODING_RESULTS)
    i = pd.read_csv(INCREMENTAL_ENCODING_RESULTS)

    pass