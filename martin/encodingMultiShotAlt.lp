%%%%%%%%
%%%%%%%%
%PROGRAM UPDATESTATE(t)
%%%%%%%%
%%%%%%%%


#program updateState(t).

% Here first explicitly rewrite everything monotonic from the previous steps
%%%§§§ I think most of this can be avoided 

%%%§§§ Might need this to make rules safe
%%%§§§ state(t).


%%%&&& Now predicates ending with I are incremental, so e.g. stateStatementI(t,S,P) means S becomes a *new* state-statement at step t, so in addition state statements at previous states t'«t 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Complete statements / rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

completeStateStatementI(t, S, P) :- stateStatementI(t, S, P), assumption(S). % copy safely

% incomplete statements (auxiliary), that are in player's sets
%%%§§§ A statement either was already incomplete (at state t-1) and was not completed (at state t)
%%%§§§ OR is a new state statement (at state t) and is not complete (at state t)
%%%§§§ Analogous for rules
%%%§§§ NON-MONOTONIC
incompleteStateStatement(t, S, P) :- incompleteStateStatement(t-1, S, P), not completeStateStatementI(t, S, P).
incompleteStateStatement(t, S, P) :- stateStatementI(t, S, P), not completeStateStatementI(t, S, P).
incompleteStateRule(t, RId, P) :- incompleteStateRule(t-1,RId,P), not completeStateRuleI(t,RId,P).
incompleteStateRule(t, RId, P) :- stateRuleI(t, RId, P), body(RId, B), incompleteStateStatement(t, B, P).

%%%%§§§Alternative for incompleteStateRule in case recursion is bad:
%%%%§§§ incompleteStateRule(t, RId, P) :- stateRuleI(_, RId, P), body(RId, B), incompleteStateStatement(t, B, P). 

completeStateRuleI(t, RId, P) :- stateRuleI(_, RId, P), not incompleteStateRule(t, RId, P). % copy safely

completeStateStatementI(t, S, P):-completeStateRuleI(t, RId, P), head(RId, S). % copy safely



%%%&&& NOT SURE ABOUT THIS PART SO COMMENTED OUT FOR THE TIME BEING
% fight cycles
% for the opponent, it is possible to have circular dependencies and still win - they just need to create another complete argument without these dependencies. This solution filters out such cases. But at least it should be correct

%dependency(t, H, B, P) :- stateRule(t, RId, P), head(RId, H), body(RId, B). % copy safely
%dependency(t, H, B2, P) :- stateRule(t, RId, P), head(RId, H), body(RId, B1), dependency(t, B1, B2, P). % copy safely
%incompleteStateStatement(t, S, P) :- dependency(t, S, S, P). % incomplete if depends on itself - should be fixed for the opp % copy safely

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Defences
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
defenceI(t, D) :- stateStatementI(t, D, "P"), assumption(D). % copy safely
defenceContraryI(t, C) :- defenceI(t, D), contraryI(D, C). % copy safely

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Culprits
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
culpritI(t, C) :- stateStatementI(t, S, "P"), contrary(C, S). % copy safely
culpritContraryI(t, Ctr) :- culpritI(t, C), contrary(C, Ctr). % copy safely

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining opponent rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%remainingRule(t, RId, "O") :- not stateRule(t, RId, "O"), head(RId, _).

usedRuleI(t, RId, "O") :- stateRuleI(t, RId, "O"), head(RId, _).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining proponent rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% auxiliary rule heads at state T
ruleHeadI(t, H, P) :- stateRuleI(t, RId1, P), head(RId1, H), player(P). % copy safely
%remainingRule(t, RId1, "P") :- not ruleHead(t, H, "P"), head(RId1, H).
%remainingRule(t, RId1, "P") :- not stateStatement(t, H, "P"), head(RId1, H).

usedRuleI(t, RId1, "P") :- ruleHeadI(t, H, "P"), head(RId1, H).
usedRuleI(t, RId1, "P") :- stateStatementI(t, H, "P"), head(RId1, H).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining proponent blocked rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), body(RId, B), culprit(t, B).                     

%remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), body(RId, B), defenceContrary(t, B).             
                                                                         
%remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), head(RId, H), defenceContrary(t, H).             


ruleBlockedI(t,RId,P) :- body(RId, B), culpritI(t, B),player(P).
ruleBlockedI(t,RId,"P") :- body(RId, B), defenceContraryI(t, B).
ruleBlockedI(t,RId,"P") :- head(RId, H), defenceContraryI(t, H).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining Opponent blocked rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%remainingRuleBlocked(t, RId, "O") :- remainingRule(t, RId, "O"), body(RId, B), culprit(t, B).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining unblocked rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%remainingUnblockedRule(t, RId, P) :- remainingRule(t, RId, P), not remainingRuleBlocked(t, RId, P).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Unexpanded proponent statements
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%unexpandedStatement(t, S, "P") :- stateStatement(t, S, "P"), not ruleHead(t, S, "P").

expandedStatementI(t,S,"P"):-stateStatementI(t,S,"P"), ruleHeadI(t,S,"P").


