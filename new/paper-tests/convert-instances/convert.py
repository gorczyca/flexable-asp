from pathlib import Path
import pandas as pd

INSTANCES_PATH = '/home/piotr/Dresden/iccma2023_results/iccma2023_benchmarks/benchmarks/main'

OUTPUT_PATH = '/home/piotr/Dresden/iccma2023_results/iccma2023_benchmarks/benchmarks/asp-syntax'

OUTPUT_GOALS_PATH = '/home/piotr/Dresden/iccma2023_results/iccma2023_benchmarks/benchmarks/instance-goal.csv'

def get_files_with_extension(directory, extension):
    return [f.name for f in Path(directory).iterdir() if f.is_file() and f.suffix == extension]


def convert_to_asp(file_path):
    arguments = set()
    attacks = []
    first_line_skipped = False

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()

            # Skip the first line starting with "p af"
            if not first_line_skipped:
                first_line_skipped = True
                continue

            if line.startswith("#"):
                # Argument line: e.g., "# a1"
                arg_id = line[1:].strip()
                if arg_id:
                    arguments.add(arg_id)
            elif line:
                # Attack line: e.g., "a1 a2"
                parts = line.split()
                if len(parts) == 2:
                    a, b = parts
                    attacks.append((a, b))
                    arguments.update([a, b])

    asp_lines = [f"arg({a})." for a in sorted(arguments)]
    asp_lines += [f"att({a},{b})." for a, b in attacks]
    return "\n".join(asp_lines)


def get_goals():
    goals_files = get_files_with_extension(INSTANCES_PATH, '.arg')
    file_goal = []
    for f in goals_files:
        with open(f'{INSTANCES_PATH}/{f}') as file:
            goal = file.read().strip()
            file_goal.append((f[:-4],goal))
    
    df = pd.DataFrame(file_goal, columns=['instance','goal'])
    df.to_csv(OUTPUT_GOALS_PATH)


def save_file(file_name, file_contents):
    full_path = f'{OUTPUT_PATH}/{file_name}'
    with open(full_path, 'w') as f:
        f.write(file_contents)


def convert_instances():
    instances_files = get_files_with_extension(INSTANCES_PATH, '.af')

    all_files_len = len(instances_files)

    for i, f in enumerate(instances_files):
        print(f'{i+1}/{all_files_len}')
        full_path = f'{INSTANCES_PATH}/{f}'
        asp_encoding = convert_to_asp(full_path)
        save_file(f, asp_encoding)



if __name__ == '__main__':
    # convert_instances() 
    get_goals()   

