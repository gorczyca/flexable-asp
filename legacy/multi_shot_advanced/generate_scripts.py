import os


POSSIBLE_OPTIONS = ['varScores', 'signs', 'lemmaScores', 'lemmas', *list(range(16))]
TEMPLATE_FILE = './script_template.sh'
BASE_SCRIPT_NAME = 'ms_adv_{}.sh'
OUTPUT_PATH = './scripts'
REPLACE_TOKEN = '{{}}'


def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def save_file(file_contents, file_path):
    with open(file_path, 'w') as file:
        file.write(file_contents)


if __name__ == '__main__':
    file_template = read_file(TEMPLATE_FILE)
    for opt in POSSIBLE_OPTIONS:
        script_contents = file_template.replace(REPLACE_TOKEN, str(opt))
        save_file(script_contents, os.path.join(OUTPUT_PATH, BASE_SCRIPT_NAME.format(opt)))

