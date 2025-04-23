

% every assumption is a complete statement
completeStateStatement(t, S, P) :- stateStatement(t, S, P), assumption(S). % copy safely

% incomplete statements (auxiliary), that are in player's sets
incompleteStateStatement(t, S, P) :- stateStatement(t, S, P), not completeStateStatement(t, S, P). 

incompleteStateRule(t, RId, P) :- stateRule(t, RId, P), body(RId, B), incompleteStateStatement(t, B, P). 

completeStateRule(t, RId, P) :- stateRule(t, RId, P), not incompleteStateRule(t, RId, P). % copy safely

completeStateStatement(t, S, P):-completeStateRule(t, RId, P), head(RId, S). % copy safely

% incomplete statements (not necessarily in players sets)
incompleteStatement(t, S, P) :- player(P), statement(S), not completeStateStatement(t, S, P). 

% fight cycles
% for the opponent, it is possible to have circular dependencies and still win - they just need to create another complete argument without these dependencies. This solution filters out such cases. But at least it should be correct

dependency(t, H, B, P) :- stateRule(t, RId, P), head(RId, H), body(RId, B). % copy safely
dependency(t, H, B2, P) :- stateRule(t, RId, P), head(RId, H), body(RId, B1), dependency(t, B1, B2, P). % copy safely
incompleteStateStatement(t, S, P) :- dependency(t, S, S, P). % incomplete if depends on itself - should be fixed for the opp % copy safely
