
import re
from itertools import combinations
from scipy.stats import truncnorm
import numpy as np
import os
import random

import pandas as pd


SOME_INSTANCES_PATH = '/home/piotr/Dresden/multishot/flexable-asp/create_instances/some_results.csv'

INSTANCES_PATH = '/home/piotr/Dresden/multishot/flexable-asp/test/asp_for_aba_instances'

OUTPUT_INSTANCES = '/home/piotr/Dresden/multishot/flexable-asp/create_big_instances/instances'
OUTPUT_CSV = '/home/piotr/Dresden/multishot/flexable-asp/create_big_instances/inst_goal.csv'

MERGE_N_FRAMEWORKS = 500

CHOOSE_NO_GOAL_STATEMENTS = 10

DISTRIBUTION_MEAN_MAX = 1
BATCHES_NO = 10
# DISTRIBUTION_STD_DEV = 1

assumption_pattern = re.compile(r"assumption\((\w+)\)\.")
contrary_pattern = re.compile(r"contrary\((\w+),(\w+)\)\.")
body_pattern = re.compile(r"body\((\d+),(\w+)\)\.")
head_pattern = re.compile(r"head\((\d+),(\w+)\)\.")




def load_framework_string_and_statements(instance_path, fr_id):
    statements = set()
    assumptions = set()

    rule_ids = set()
    
    with open(instance_path, 'r') as file:
        # framework_string = file.read()
        framework_string = file.read()
        framework_lines = framework_string.split('\n')
        for line in framework_lines:
            line = line.strip()  # Remove leading/trailing whitespace

            added_statements = set()
            added_assumptions = set()

            rule_id = None

            # Match assumptions
            assumption_match = assumption_pattern.match(line)
            if assumption_match:
                added_assumptions.add(assumption_match.group(1))

            # Match contraries
            contrary_match = contrary_pattern.match(line)
            if contrary_match:
                added_assumptions.add(contrary_match.group(1))
                added_statements.add(contrary_match.group(2))
                # statements += [contrary_match.group(1), contrary_match.group(2)]

            # Match bodies
            body_match = body_pattern.match(line)
            if body_match:
                added_statements.add(body_match.group(2))
                rule_id = body_match.group(1)


            # Match heads
            head_match = head_pattern.match(line)
            if head_match:
                added_statements.add(head_match.group(2))
                rule_id = head_match.group(1)


            ######################

            added_statements = added_statements - added_assumptions


            if added_statements.intersection(added_assumptions):
                pass


            for st in added_statements.union(added_assumptions):
                new_st = f'fr{fr_id}_{st}'
                # added_statements.remove(st)
                # added_statements.add(new_st)

                if new_st in assumptions or st in added_assumptions:
                    assumptions.add(new_st)
                else:
                    statements.add(new_st)


                if statements.intersection(assumptions):
                    pass


                framework_string = framework_string.replace(f'({st}',f'({new_st}').replace(f',{st}',f',{new_st}')
                # print(framework_string.split('\n')[0])

            # added_statements = added_statements - added_assumptions

            # for st 


            if rule_id:
                new_rule_id = f'r_fr{fr_id}_{rule_id}'
                framework_string = framework_string.replace(f'head({rule_id}', f'head({new_rule_id}').replace(f'body({rule_id}', f'body({new_rule_id}')
                rule_ids.add(new_rule_id)

        
        # framework_string.replace('head')
        # change rules to IDs again


        if statements.intersection(assumptions):
            pass

        return framework_string, statements-assumptions, assumptions, rule_ids
        # pass
    



def get_framework_statements(framework_string):
    pass


def create_framework_string(frameworks_dict, distribution_mean, batch_no):

    # all_rule_ids = set()
    # for i in frameworks_dict:
        # all_rule_ids = all_rule_ids.union(frameworks_dict[i]['framework_rule_ids'])
    

    # rule_id_map = { rule_id: i for (i, rule_id) in enumerate(all_rule_ids, start=1) }



    output = '' # otherwise ASPFORABA complains 
    # output = f'% distribution mean={distribution_mean}\n\n'
    for i in frameworks_dict:
        # output += f'% {frameworks_dict[i]["instance"]}\n'
        
        fram_string = frameworks_dict[i]["framework_string"]

        # for rule_id, int_i in rule_id_map.items():
            # fram_string = fram_string.replace(rule_id, str(int_i))

        output += fram_string + '\n'
    
    return output, f'instance_n={MERGE_N_FRAMEWORKS}_m={distribution_mean}_b={batch_no}.lp'


def main(distribution_mean, batch_no):
    some_df = pd.read_csv(SOME_INSTANCES_PATH)
    # filter out the timed outs
    some_df = some_df[some_df['verdict'] != 'TIMEOUT']
    # choose random sample of frameworks
    chosen_df = some_df.sample(n=MERGE_N_FRAMEWORKS)

    # load the frameworks
    frameworks_dict = { i: { 'id': f'fr{i}', 'instance': row.instance } for i, (index, row) in enumerate(chosen_df.iterrows(), start=1) }
  
    for i in frameworks_dict:
        
        #
        instance = frameworks_dict[i]['instance']
        instance_path = f'{INSTANCES_PATH}/{instance}'
        
        # 
        framework_string, statements, assumptions, rule_ids = load_framework_string_and_statements(instance_path, i)
        frameworks_dict[i]['framework_string'] = framework_string
        frameworks_dict[i]['framework_statements'] = statements
        frameworks_dict[i]['framework_assumptions'] = assumptions
        frameworks_dict[i]['framework_rule_ids'] = rule_ids


    pairs = list(combinations(frameworks_dict, 2))
    random.shuffle(pairs)
    
    for pair in pairs:
        pair_list = list(pair)
        random.shuffle(pair_list)
        [id_1, id_2] = pair_list

        # for each pair, decide how many statements/assumptions should be shared
        statements_no = np.random.poisson(distribution_mean, 1)[0]
        for i in range(statements_no):
            # pass
            # decide if an assumption or a statement should be shared

            fram_1_ass_no = len(frameworks_dict[id_1]['framework_assumptions'])
            fram_1_stmt_no = len(frameworks_dict[id_1]['framework_statements'])
            total_no = fram_1_stmt_no + fram_1_ass_no

            probabilities = [fram_1_ass_no/total_no, fram_1_stmt_no/total_no]
            share_assumption = random.choices([True, False], weights=probabilities, k=1)[0]
            # choose randomly a ass/statement from the first framework
            if share_assumption:
                from_1 = np.random.choice(list(frameworks_dict[id_1]['framework_assumptions']))
                # choose randomly a assumptions from the 2nd framework
                from_2 = np.random.choice(list(frameworks_dict[id_2]['framework_assumptions']))
                # replace in EVERY framework, the assumption "from_2" with "from_1"
                for fr_id in frameworks_dict:
                    if from_2 in frameworks_dict[fr_id]['framework_assumptions']:
                        # replace it in the set of assumptions
                        frameworks_dict[fr_id]['framework_assumptions'].remove(from_2)
                        frameworks_dict[fr_id]['framework_assumptions'].add(from_1)
                        # replace it in the framework string
                        fram_2_string = frameworks_dict[fr_id]['framework_string']
                        frameworks_dict[fr_id]['framework_string'] = fram_2_string.replace(f'({from_2}',f'({from_1}').replace(f',{from_2}',f',{from_1}')
            # do the same for statements
            else:
                from_1 = np.random.choice(list(frameworks_dict[id_1]['framework_statements']))
                # choose randomly a assumptions from the 2nd framework
                from_2 = np.random.choice(list(frameworks_dict[id_2]['framework_statements']))
                # replace in EVERY framework, the assumption "from_2" with "from_1"
                for fr_id in frameworks_dict:
                    if from_2 in frameworks_dict[fr_id]['framework_statements']:
                        # replace it in the set of assumptions
                        frameworks_dict[fr_id]['framework_statements'].remove(from_2)
                        frameworks_dict[fr_id]['framework_statements'].add(from_1)
                        # replace it in the framework string
                        fram_2_string = frameworks_dict[fr_id]['framework_string']
                        frameworks_dict[fr_id]['framework_string'] = fram_2_string.replace(f'({from_2}',f'({from_1}').replace(f',{from_2}',f',{from_1}')


            # shared = np.random.choice(frameworks_dict[id_1]['framework_assumptions'] if share_assumption else frameworks_dict[id_1]['framework_assumptions'])


    # pass
    framework_string, framework_name = create_framework_string(frameworks_dict, distribution_mean, batch_no)

    with open(f'{OUTPUT_INSTANCES}/{framework_name}', 'w') as out_file:
        out_file.write(framework_string)
    
    # choose 
    # CHOOSE_NO_GOAL_STATEMENTS
    all_framework_statements = set()
    for i in frameworks_dict:
        all_framework_statements = all_framework_statements.union(frameworks_dict[i]['framework_statements']) 
        all_framework_statements = all_framework_statements.union(frameworks_dict[i]['framework_assumptions']) 

    selected_goals = random.sample(list(all_framework_statements), CHOOSE_NO_GOAL_STATEMENTS)

    ## debug
    for g in selected_goals:
        if g not in framework_string:
            pass
    ## 


    # instance,goal,correct_result

    outs = []
    for g in selected_goals:
        outs.append({
            'instance': framework_name,
            'goal': g,
            'adm_result': None
        })
    
    return pd.DataFrame(outs)



if __name__ == '__main__':

    if not os.path.exists(OUTPUT_INSTANCES):
        os.makedirs(OUTPUT_INSTANCES)

    outputs_df = pd.DataFrame(columns=['instance', 'goal',  'adm_result'])

    for mean in range(DISTRIBUTION_MEAN_MAX):
        for i in range(BATCHES_NO):
            print(f'mean={mean}, batch={i}')
            outs = main(mean, i)

            outputs_df = pd.concat([outputs_df, outs], ignore_index=True)

    outputs_df.index = outputs_df.index+1
    # df.index = df.index + 1
    # df.to_csv(OUTPUT_CSV_PATH, index=True, index_label='id')
    outputs_df.to_csv(OUTPUT_CSV, index=True, index_label='id')
    # pass