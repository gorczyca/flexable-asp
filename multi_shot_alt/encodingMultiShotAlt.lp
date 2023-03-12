#program base.
% move types
moveType("PB1";"PB2";"PF1";"OB1";"OB2";"OF1";"PF2";"OF2").
advancementMoveType("PB1";"PB2";"PF1";"OB1";"OB2";"PF2";"OF2"). % no OF1
proponentMove("PB1";"PB2";"PF1";"PF2").
opponentMove("OB1";"OB2";"OF1";"OF2").
ruleMoveType("PB1";"PB2";"PF1";"OB1";"OB2";"OF1").
assMoveType("PF2";"OF2").
% players
player("P";"O").

statement(S) :- assumption(S).
statement(S) :- contrary(S, _).
statement(S) :- contrary(_, S).
statement(S) :- goal(S).
statement(S) :- head(_, S).
statement(S) :- body(_, S).

% inconsistent assumptions
inconsistentAssumption(A) :- assumption(A), contrary(A, A).

%
nonEmptyBodyRule(RId) :- head(RId, _), body(RId, _).
emptyBodyRule(RId) :- not nonEmptyBodyRule(RId), head(RId, _).

stateStatement(0, S, "P") :- goal(S).

%  rules attacking themselves
remainingRuleBlocked(0, RId, "P") :- body(RId, B), head(RId,H), contrary(B,H).
remainingRuleBlocked(0, RId, "P") :- body(RId, B1), body(RId,B2), contrary(B1,B2).


#program updateState(t).
% TODO: here first explicitly rewrite everything monotonic from the previous steps
stateRule(t, RId, P) :- stateRule(t-1, RId, P).
stateStatement(t, S, P) :- stateStatement(t-1, S, P).

completeStateStatement(t, S, P) :- completeStateStatement(t-1, S, P).
completeStateRule(t, RId, P) :- completeStateRule(t-1, RId, P).

defence(t, D) :- defence(t-1, D).
defenceContrary(t, C) :- defenceContrary(t-1, C).
culprit(t, C) :- culprit(t-1, C).
culpritContrary(t, Ctr) :- culpritContrary(t-1, Ctr).

ruleHead(t, H, P) :- ruleHead(t-1, H, P).

stateFullyExpandedStatement(t, S, "O") :- stateFullyExpandedStatement(t-1, S, "O").

playedBlockedStatement(t, S, "O") :- playedBlockedStatement(t-1, S, "O").
playedBlockedRule(t, RId, "O") :- playedBlockedRule(t-1, RId, "O").
stateFullyExpandedStatementNotAssumption(t, S, "O") :- stateFullyExpandedStatementNotAssumption(t-1, S, "O").


move(t) :- move(t, _, _).

% add everything from P to O
stateStatement(t, S, "O") :- stateStatement(t, S, "P"). % copy safely
stateRule(t, RId, "O") :- stateRule(t, RId, "P").  % copy safely

dependency(t, H, B, P) :- dependency(t-1, H, B, P).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Complete statements / rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Defences
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
defence(t, D) :- stateStatement(t, D, "P"), assumption(D). % copy safely
defenceContrary(t, C) :- defence(t, D), contrary(D, C). % copy safely

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Culprits
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
culprit(t, C) :- stateStatement(t, S, "P"), contrary(C, S). % copy safely
culpritContrary(t, Ctr) :- culprit(t, C), contrary(C, Ctr). % copy safely

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining opponent rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
remainingRule(t, RId, "O") :- not stateRule(t, RId, "O"), head(RId, _).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining proponent rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% auxiliary rule heads at state T
ruleHead(t, H, P) :- stateRule(t, RId1, P), head(RId1, H), player(P). % copy safely
remainingRule(t, RId1, "P") :- not ruleHead(t, H, "P"), head(RId1, H).
remainingRule(t, RId1, "P") :- not stateStatement(t, H, "P"), head(RId1, H).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining proponent blocked rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), body(RId, B), culprit(t, B).                     

remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), body(RId, B), defenceContrary(t, B).             
                                                                         
remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), head(RId, H), defenceContrary(t, H).             

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining Opponent blocked rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
remainingRuleBlocked(t, RId, "O") :- remainingRule(t, RId, "O"), body(RId, B), culprit(t, B).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining unblocked rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
remainingUnblockedRule(t, RId, P) :- remainingRule(t, RId, P), not remainingRuleBlocked(t, RId, P).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Unexpanded proponent statements
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
unexpandedStatement(t, S, "P") :- stateStatement(t, S, "P"), not ruleHead(t, S, "P").


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Fully expanded opponents statements
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
stateExpandableStatement(t, S, "O") :- stateStatement(t, S, "O"), remainingUnblockedRule(t, RId, "O"), head(RId, S).
stateFullyExpandedStatement(t, S, "O") :- stateStatement(t, S, "O"), not stateExpandableStatement(t, S, "O"). % copy


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Played blocked pieces
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %   statements
playedBlockedStatement(t, S, "O") :- stateStatement(t, S, "O"), culprit(t, S). % copy
% %   rules
playedBlockedRule(t, RId, "O") :- stateRule(t, RId, "O"), body(RId, B), playedBlockedStatement(t, B, _). % copy
% %   statements 2
% %       auxiliaries
stateFullyExpandedStatementNotAssumption(t, S, "O") :- stateFullyExpandedStatement(t, S, "O"), not assumption(S). % copy
% %
playedNonBlockedRule(t, RId, "O") :- stateRule(t, RId, "O"), not playedBlockedRule(t, RId, "O").
% % 

% auxiliary
% statements for which there are unblocked rules
playedUnblockedStatement(t, S, "O") :- stateRule(t, RId, "O"), not playedBlockedRule(t, RId, "O"), head(RId, S).

playedBlockedStatement(t, S, "O") :- stateFullyExpandedStatementNotAssumption(t, S, "O"), not playedUnblockedStatement(t, S, "O"). % copy

% %  Unblocked complete opponet pieces
% % 1
unblockedCompleteStatement(t, S, "O") :- stateStatement(t, S, "O"), assumption(S), not culprit(t, S).

% % 2
incompleteNonBlockedRule(t, RId, "O") :- playedNonBlockedRule(t, RId, "O"), body(RId, B), not unblockedCompleteStatement(t, B, "O").

unblockedCompleteRule(t, RId, "O") :- playedNonBlockedRule(t, RId, "O"), not incompleteNonBlockedRule(t, RId, "O").

% % 3
unblockedCompleteStatement(t, H, "O") :- unblockedCompleteRule(t, RId, "O"), head(RId, H).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Played non-blocked pieces
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% % supporting defence contraries
% % auxiliary
playedNonBlockedStatement(t, S, "O") :- stateStatement(t, S, "O"), not playedBlockedStatement(t, S, "O").
% % 1.
unblockedStatementSupportingDefenceContraries(t, S, "O") :- defenceContrary(t, S), playedNonBlockedStatement(t, S, "O").
% % 2.
unblockedStatementSupportingDefenceContraries(t, S, "O") :- playedNonBlockedStatement(t, S, "O"), unblockedRuleSupportingDefenceContraries(t, RId, "O"), body(RId, S).
% % 3.
unblockedRuleSupportingDefenceContraries(t, RId, "O") :- playedNonBlockedRule(t, RId, "O"), head(RId, H), unblockedStatementSupportingDefenceContraries(t, H, "O").

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Culprit candidates 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
culpritCandidate(t, C) :- assumption(C), unblockedStatementSupportingDefenceContraries(t, C, "O").


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Propagate from the previous step
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% stateRule(t, RId, P) :- stateRule(t-1, RId, P).
% stateStatement(t, S, P) :- stateStatement(t-1, S, P).

% add more things that you can safely copy

% %%%%%%%%%%%%%%%%
% % possible move
% %%%%%%%%%%%%%%%%

% % the parametrized moves would have to be split among more files to obtain other semantics. Ideally we would do sth like:
% % clingo general_encoding_file.lp advancement_type.lp termination_criteria.lp 
% % TODO: for now only admissible

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Possible moves
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% % PB1
possibleMove(t, "PB1", RId) :- remainingUnblockedRule(t, RId, "P"), head(RId, H), unexpandedStatement(t, H, "P").

% % PB2
culpritCandidateContrary(t, Ctr) :- culpritCandidate(t, Cul), contrary(Cul, Ctr).

possibleMove(t, "PB2", RId) :- remainingUnblockedRule(t, RId, "P"), head(RId, Ctr), culpritCandidateContrary(t, Ctr), not stateStatement(t, Ctr, "P"), not defenceContrary(t, Ctr).

% % PF1
notPossibleForwardRule(t, RId, "P") :- remainingUnblockedRule(t, RId, "P"), body(RId, B), incompleteStatement(t, B, "P").

possibleForwardRule(t, RId, "P") :- remainingUnblockedRule(t, RId, "P"), not notPossibleForwardRule(t, RId, "P"). 

possibleForwardRule(t, RId, "P") :- remainingUnblockedRule(t, RId, "P"), emptyBodyRule(RId).
possibleMove(t, "PF1", RId) :- possibleForwardRule(t, RId, "P").

% % PF2
possibleMove(t, "PF2", A) :- culpritCandidateContrary(t, A), assumption(A), not stateStatement(t, A, "P"), not inconsistentAssumption(A), not culprit(t, A), not defenceContrary(t, A).


% % OB1
possibleMove(t, "OB1", RId) :- remainingUnblockedRule(t, RId, "O"), head(RId, H), unblockedStatementSupportingDefenceContraries(t, H, "O").

% % OB2
possibleMove(t, "OB2", RId) :- remainingUnblockedRule(t, RId, "O"), head(RId, H), defenceContrary(t, H).

% % OF1 - not available for moves, but for termination criteria

notPossibleForwardRule(t, RId, "O") :- remainingUnblockedRule(t, RId, "O"), body(RId, B), not unblockedCompleteStatement(t, B, "O").

possibleForwardRule(t, RId, "O") :- remainingUnblockedRule(t, RId, "O"), not notPossibleForwardRule(t, RId, "O").
possibleMove(t, "OF1", RId) :- possibleForwardRule(t, RId, "O").  

% % OF2
possibleMove(t, "OF2", A) :- defenceContrary(t, A), assumption(A), not stateStatement(t, A, "O"), not culprit(t, A).

% update states after performing moves
stateStatement(t, S, P) :- move(t, Type, RId), ruleMoveType(Type), proponentMove(Type), body(RId, S), player(P).

stateStatement(t, S, P) :- move(t, Type, RId), ruleMoveType(Type), proponentMove(Type), head(RId, S), player(P).

stateStatement(t, A, P) :- move(t, Type, A), assMoveType(Type), proponentMove(Type), assumption(A), player(P).

stateRule(t, RId, P) :- move(t, Type, RId), ruleMoveType(Type), proponentMove(Type), player(P).


stateStatement(t, S, "O") :- move(t, Type, RId), ruleMoveType(Type), opponentMove(Type), body(RId, S).

stateStatement(t, S, "O") :- move(t, Type, RId), ruleMoveType(Type), opponentMove(Type), head(RId, S).

stateStatement(t, A, "O") :- move(t, Type, A), assMoveType(Type), opponentMove(Type), assumption(A).

stateRule(t, RId, "O") :- move(t, Type, RId), ruleMoveType(Type), opponentMove(Type).


% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% termination criteria
incompleteGoal(t, G) :- goal(G), incompleteStateStatement(t, G, "P").

incompleteCulpritContrary(t, Ctr) :- culpritContrary(t, Ctr), incompleteStateStatement(t, Ctr, "P").

taCondition1Violated1(t) :- incompleteGoal(t, _).
taCondition1Violated2(t) :- incompleteCulpritContrary(t, _).

taCondition1(t) :- not taCondition1Violated1(t), not taCondition1Violated2(t).

taCondition2Violated(t) :- defenceContrary(t, C), unblockedCompleteStatement(t, C, "O").

taCondition2(t) :- not taCondition2Violated(t).
taCondition(t) :- taCondition1(t), taCondition2(t).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% opp cannot move
oppCanMoveTermination(t) :- possibleMove(t, "OB1", _).
oppCanMoveTermination(t) :- possibleMove(t, "OB2", _).
oppCanMoveTermination(t) :- possibleMove(t, "OF2", _).

% prop cannot move
propCanMoveTermination(t) :- possibleMove(t, "PB1", _).
propCanMoveTermination(t) :- possibleMove(t, "PB2", _).
propCanMoveTermination(t) :- possibleMove(t, "PF2", _).

proponentWon(t) :- taCondition(t), not oppCanMoveTermination(t).
opponentWon(t) :- not taCondition(t), not propCanMoveTermination(t).


% just for easier presentation

moveAss(t, Type, A) :- move(t, Type, A), assMoveType(Type).
moveRuleHead(t, Type, H) :- move(t, Type, RId), ruleMoveType(Type), head(RId, H).
moveRuleBody(t, Type, B) :- move(t, Type, RId), ruleMoveType(Type), body(RId, B).

% 
remainingPropRule(t, H) :- remainingRule(t, RId, "P"), head(RId, H).
propRuleHead(t, H) :- ruleHead(t, H, "P").

pf1Possible(t) :- possibleMove(t, "PF1", _).
pf1NotPossible(t) :- not pf1Possible(t).


#program checkPropWon(t).
#external hasPropWon(t).
:- hasPropWon(t), not proponentWon(t).
% if this is satisfiable, return SAT, else check the following

#program checkGameOn(t).
#external gameOn(t).
:- opponentWon(t), gameOn(t).



#program step(t).
% choose 1 move

% encofce using PF1 moves whenever possible

{ move(t, Type, X) : possibleMove(t-1, Type, X),  advancementMoveType(Type)  } = 1 :- pf1NotPossible(t-1).
{ move(t, "PF1", X) : possibleMove(t-1, "PF1", X) } = 1 :- pf1Possible(t-1).

% #show possibleMove/3.

% ------------- debugging errors
% #show remainingRule/3.
% #show remainingPropRule/2.
% #show propRuleHead/2.

% ------------- nice output
#show moveAss/3.
#show moveRuleHead/3.
#show moveRuleBody/3.
#show opponentWon/1.
% #show move/3.


