def convert_to_move(step, symbols):
    move_type, move_info = None, None
    
    match list(symbols):
        case []:
            pass
        case [singleElem]:
            # if it's 1-elem thing, then it's either a rule with no body OR an assumption
            if singleElem.name == 'moveAss':
                move_type, assumption = singleElem.arguments[1:]
                move_info = assumption
            else:
                move_type, rule_head = singleElem.arguments[1:]
                move_info = f'{rule_head} ←'
        case more_elems:
            # if it's more than 1-elem, then it' rule with head and body
            rule_head_symbol = [sym for sym in more_elems if sym.name == 'moveRuleHead'][0]
            move_type, rule_head = rule_head_symbol.arguments[1:]
            rule_body_symbols = [sym for sym in more_elems if sym.name == 'moveRuleBody']
            rule_body_literals = list(map(lambda sym: sym.arguments[2].name, rule_body_symbols))
            move_info = f'{rule_head} ← {",".join(rule_body_literals)}'

    print(f'{step}: {move_type}: {move_info}')


def on_model(step, model):
    symbols = model.symbols(shown=True) 

    move_symbols = list(filter(lambda sym: sym.name != 'move' and sym.name.startswith('move'), symbols))
    moves_sorted = sorted(move_symbols, key=lambda symbol: symbol.arguments[0].number)

    print(f'Length: {step}')

    oppWon = list(filter(lambda sym: sym.name == 'opponentWon', symbols))
    if oppWon:
        print('Opponent won!')

    groups = groupby(moves_sorted, key=lambda symbol: symbol.arguments[0].number)
    for gr in groups:
        convert_to_move(*gr)
    print(f'------------------------')