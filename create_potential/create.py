import random


FRAMEWORK_NUMBERS = 10000


def create_subframework_string(sub_id, rule_id, ass_id, stmt_id, attacked_id):
    return f'''
    assumption(f{sub_id}_a{ass_id}).
    head(f{sub_id}_{rule_id},f{sub_id}_s{stmt_id}).
    body(f{sub_id}_{rule_id},f{sub_id}_a{ass_id}).
    contrary(f{sub_id}_a{attacked_id},f{sub_id}_s{stmt_id}).
    '''
    


def create_subframework(sub_id):
    # subframework size
    size = random.randrange(1, 9, 2)
    framework_str = f'% framework f{sub_id}, size={size} '
    for i in range(1, size+1):
        if i == size:
            framework_str += create_subframework_string(sub_id=sub_id, rule_id=size, ass_id=size, stmt_id=size, attacked_id=1)
        else:
            framework_str += create_subframework_string(sub_id=sub_id, rule_id=i, ass_id=i, stmt_id=i, attacked_id=i+1)
        framework_str += '%'
    return framework_str


def add_satisfiable():
    return f'''
    % start with the satisfiable subframework, goal is sat1_s

    assumption(sat1_a).
    contrary(sat1_a, sat1_b).
    head(sat1_1, sat1_s).
    body(sat1_1, sat1_a).
    
    '''


if __name__ == '__main__':
    # total_str = ''
    total_str = add_satisfiable()
    for i in range(1, FRAMEWORK_NUMBERS+1):
        total_str += create_subframework(i)
    
    with open('/home/piotr/Dresden/multishot/flexable-asp/create_potential/instance.lp', 'w') as f:
        f.write(total_str)
            
        