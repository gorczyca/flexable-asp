import pandas as pd

from alive_progress import alive_bar



TRIVIAL_COUNT = 0
NON_TRIVIAL_MAX_STEP = 5
NON_TRIVIAL_COUNT = 10

INSTANCES_WITH_TRIVIAL = '/home/piotr/Dresden/multishot/flexable-asp/create_instances/instances_with_trivial.csv'
SOME_RESULTS = '/home/piotr/Dresden/multishot/flexable-asp/create_instances/some_results.csv'
# INSTANCES_WITH_TRIVIAL = '/home/piotr/Dresden/multishot/flexable-asp/remove_trivial/instances_with_trivial.csv'

ASPFORABA_HARD_INSTANCES = '/home/piotr/Dresden/multishot/flexable-asp/create_instances/iccma2023_timeouts.csv'

OUTPUT_PATH = '/home/piotr/Dresden/multishot/flexable-asp/create_instances/instances'
OUTPUT_CSV = '/home/piotr/Dresden/multishot/flexable-asp/create_instances/stats.csv'

HARD_INSTANCES_PATH = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/iccma2023_instances'
EASY_INSTANCES_PATH = 'test_instances/asp_for_aba_instances'

def replace_ambiguous(string):
    return string.replace(',s',',sn').replace('(s','(sn')


def merge_files_contents(file1_path, file2_path, separator=f'%%%%%%%%%%%%%%%%%%%%%'):
    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        easy = f1.read() 
        hard = f2.read()

        easy = replace_ambiguous(easy)

        # replace duplicates in body
        easy = easy.replace('head(', 'head(xxx').replace('body(', 'body(xxx')
        

        return '\n'.join([easy,separator,hard])



def run():
    some_df = pd.read_csv(SOME_RESULTS)

    trivials_df = some_df[some_df['is_trivial']=='yes']
    non_trivials_df = some_df[some_df['is_trivial']=='no']
    # trivial_pos = trivials_df[trivials_df['correct_result'] =='yes'].sample(TRIVIAL_COUNT)
    trivial_neg = trivials_df[trivials_df['correct_result'] =='no'].sample(TRIVIAL_COUNT)


    nt_df = non_trivials_df[non_trivials_df['steps_obtained'] <= NON_TRIVIAL_MAX_STEP].sample(n=NON_TRIVIAL_COUNT)
    # some_df.set_index('id')
    # trivial_df = pd.read_csv(INSTANCES_WITH_TRIVIAL)
    # trivial_df.set_index('id')


    # concatenate the chosen trivial ones with nontrivial ones
    concat_df =  trivial_neg.append(nt_df, ignore_index=True)

    hard_df = pd.read_csv(ASPFORABA_HARD_INSTANCES)

    outputs_df = pd.DataFrame(columns=['instance', 'goal', 'easy_instance', 'hard_instance', 'correct_result', 'is_trivial', 'steps_needed'])

    total_size = len(hard_df) * len(concat_df)

    with alive_bar(total_size, dual_line=True, title=f'Creating hard') as bar:

        for _, (_, hard_row) in enumerate(hard_df.iterrows(), start=1):
            for _, (_, easy_row) in enumerate(concat_df.iterrows(), start=1):
                output_str = merge_files_contents(f'{EASY_INSTANCES_PATH}/{easy_row.instance}', f'{HARD_INSTANCES_PATH}/{hard_row.instance}')

                instance_name = f'{easy_row.instance}+{hard_row.instance}'

                with open(f'{OUTPUT_PATH}/{instance_name}', 'w') as outfile:
                    outfile.write(output_str)

                row_to_append = pd.DataFrame({
                    'instance': [instance_name],
                    'goal': [replace_ambiguous(easy_row.goal)],
                    'easy_instance': [easy_row.instance],
                    'hard_instance': [hard_row.instance],
                    'correct_result': [easy_row.correct_result],
                    'is_trivial': [easy_row.is_trivial],
                    'steps_needed': [easy_row.steps_obtained],
                })


                outputs_df = pd.concat([outputs_df, row_to_append])
                bar()

    outputs_df.to_csv(OUTPUT_CSV, index=False)

            


if __name__ == '__main__':
    run()
    pass