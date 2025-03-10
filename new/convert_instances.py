from pathlib import Path
import pandas as pd


INPUT_INSTANCES_PATH = '/home/piotr/Dresden/iccma2023_results/iccma2023_benchmarks/benchmarks/aba'
OUTPUT_INSTANCES_PATH = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/iccma2023_instances'
OUTPUT_CSV_PATH = '/home/piotr/Dresden/multishot/flexable-asp/test_instances/iccma2023.csv'


def convert_instance(instance_path):
    with open(instance_path, 'r') as f:

        rules_count = 0

        converted = []

        for line in f:
            parts = line.split()

            if not parts:
                continue

            if parts[0] == 'p':
                # problem line
                continue
            elif parts[0] == 'a':
                converted.append(f'assumption(s{parts[1]}).')
            elif parts[0] == 'c':
                converted.append(f'contrary(s{parts[1]}, s{parts[2]}).')
            elif parts[0] == 'r':
                head = parts[1]
                body = parts[2:] if len(parts) > 2 else []
                rules_count += 1
                converted.append(f'head({rules_count}, s{head}).')
                for s in body:
                    converted.append(f'body({rules_count}, s{s}).')

        return '\n'.join(converted)
            
            
if __name__ == '__main__':
    directory = Path(INPUT_INSTANCES_PATH)

    data = []
    file_count = 0
    for file in directory.glob('*.aba'):
        file_count += 1
        print(f'File: {file_count}')
        # convert file
        with open(Path(OUTPUT_INSTANCES_PATH).joinpath(f'{file.name}'), 'w') as output_file:
            instance_converted = convert_instance(str(file))
            output_file.write(instance_converted)

        # get query 
        query_file_path = file.with_name(file.name + '.asm')
        with open(query_file_path, 'r') as query_file:
            query  = query_file.read().strip()
            data.append({ 'instance': file.name, 'goal': f's{query}' })


    df = pd.DataFrame(data)
    df.index = df.index + 1
    df.to_csv(OUTPUT_CSV_PATH, index=True, index_label='id')