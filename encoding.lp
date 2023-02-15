#const maxMove = 1. % input parameter
#const goal=g.

goal(goal).

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

% add goals to both: P and B
stateStatement(0, S, "P") :- goal(S).

% add everything from P to O
stateStatement(T, S, "O") :- stateStatement(T, S, "P").
stateRule(T, RId, "O") :- stateRule(T, RId, "P").

% inconsistent assumptions
inconsistentAssumption(A) :- assumption(A), contrary(A, A).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Complete statements / rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% every assumption is a complete statement
completeStateStatement(T, S, P) :- stateStatement(T, S, P), assumption(S).

% incomplete statements (auxiliary), that are in player's sets
incompleteStateStatement(T, S, P) :- stateStatement(T, S, P), not completeStateStatement(T, S, P).

incompleteStateRule(T, RId, P) :- stateRule(T, RId, P), body(RId, B), incompleteStateStatement(T, B, P).

completeStateRule(T, RId, P) :- stateRule(T, RId, P), not incompleteStateRule(T, RId, P).

completeStateStatement(T, S, P):-completeStateRule(T, RId, P), head(RId, S). 

% incomplete statements (not necessarily in players sets)
incompleteStatement(T, S, P) :- moveStep(T), player(P), statement(S), not completeStateStatement(T, S, P).

% fight cycles
% for the opponent, it is possible to have circular dependencies and still win - they just need to create another complete argument without these dependencies. This solution filters out such cases. But at least it should be correct

dependency(T, H, B, P) :- stateRule(T, RId, P), head(RId, H), body(RId, B).
dependency(T, H, B2, P) :- stateRule(T, RId, P), head(RId, H), body(RId, B1), dependency(T, B1, B2, P).
incompleteStateStatement(T, S, P) :- dependency(T, S, S, P). 


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Defences
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
defence(T, D) :- stateStatement(T, D, "P"), assumption(D).
defenceContrary(T, C) :- defence(T, D), contrary(D, C).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Culprits
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
culprit(T, C) :- stateStatement(T, S, "P"), contrary(C, S).
culpritContrary(T, Ctr) :- culprit(T, C), contrary(C, Ctr).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining opponent rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
remainingRule(T, RId, "O") :- moveStep(T), not stateRule(T, RId, "O"), head(RId, _).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining proponent rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% auxiliary rule heads at state T
ruleHead(T, H, P) :- stateRule(T, RId1, P), head(RId1, H), player(P).
remainingRule(T, RId1, "P") :- not ruleHead(T, H, "P"), head(RId1, H), moveStep(T).
remainingRule(T, RId1, "P") :- not stateStatement(T, H, "P"), head(RId1, H), moveStep(T).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining proponent blocked rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   TODO: might be that these rules should be blocked for BOTH players, for now only prop
remainingRuleBlocked(T, RId, "P") :- body(RId, B), head(RId,H), contrary(B,H), moveStep(T). % player(P).
remainingRuleBlocked(T, RId, "P") :- body(RId, B1), body(RId,B2), contrary(B1,B2), moveStep(T). % player(P).
% % remaining rules blocked for the proponent
% %   due to culprit in the body
remainingRuleBlocked(T, RId, "P") :- remainingRule(T, RId, "P"), body(RId, B), culprit(T, B).
% %   due to defence contrary:
% %       in the body of the rule
remainingRuleBlocked(T, RId, "P") :- remainingRule(T, RId, "P"), body(RId, B), defenceContrary(T, B).
% %       in the head of the rule
remainingRuleBlocked(T, RId, "P") :- remainingRule(T, RId, "P"), head(RId, H), defenceContrary(T, H).
% %   due to rule being inconsistent
remainingRuleBlocked(T, RId, "P") :- remainingRule(T, RId, "P"), body(RId, B1), body(RId, B2), contrary(B1, B2).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining proponent blocked rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
remainingRuleBlocked(T, RId, "O") :- remainingRule(T, RId, "O"), body(RId, B), culprit(T, B).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining unblocked rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
remainingUnblockedRule(T, RId, P) :- remainingRule(T, RId, P), not remainingRuleBlocked(T, RId, P).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Unexpanded proponent statements
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
unexpandedStatement(T, S, "P") :- stateStatement(T, S, "P"), not ruleHead(T, S, "P").


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Fully expanded opponents statements
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
stateExpandableStatement(T, S, "O") :- stateStatement(T, S, "O"), remainingUnblockedRule(T, RId, "O"), head(RId, S).
stateFullyExpandedStatement(T, S, "O") :- stateStatement(T, S, "O"), not stateExpandableStatement(T, S, "O").


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Played blocked pieces
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %   statements
playedBlockedStatement(T, S, "O") :- stateStatement(T, S, "O"), culprit(T, S).
% %   rules
playedBlockedRule(T, RId, "O") :- stateRule(T, RId, "O"), body(RId, B), playedBlockedStatement(T, B, _).
% %   statements 2
% %       auxiliaries
stateFullyExpandedStatementNotAssumption(T, S, "O") :- stateFullyExpandedStatement(T, S, "O"), not assumption(S).
% %
playedNonBlockedRule(T, RId, "O") :- stateRule(T, RId, "O"), not playedBlockedRule(T, RId, "O").
% % 

% auxiliary
% statements for which there are unblocked rules
playedUnblockedStatement(T, S, "O") :- stateRule(T, RId, "O"), not playedBlockedRule(T, RId, "O"), head(RId, S).

playedBlockedStatement(T, S, "O") :- stateFullyExpandedStatementNotAssumption(T, S, "O"), not playedUnblockedStatement(T, S, "O"). 

% %  Unblocked complete opponet pieces
% % 1
unblockedCompleteStatement(T, S, "O") :- stateStatement(T, S, "O"), assumption(S), not culprit(T, S).

% % 2
incompleteNonBlockedRule(T, RId, "O") :- playedNonBlockedRule(T, RId, "O"), body(RId, B), not unblockedCompleteStatement(T, B, "O").

unblockedCompleteRule(T, RId, "O") :- playedNonBlockedRule(T, RId, "O"), not incompleteNonBlockedRule(T, RId, "O").

% % 3
unblockedCompleteStatement(T, H, "O") :- unblockedCompleteRule(T, RId, "O"), head(RId, H).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Played non-blocked pieces
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% % supporting defence contraries
% % auxiliary
playedNonBlockedStatement(T, S, "O") :- stateStatement(T, S, "O"), not playedBlockedStatement(T, S, "O").
% % 1.
unblockedStatementSupportingDefenceContraries(T, S, "O") :- defenceContrary(T, S), playedNonBlockedStatement(T, S, "O").
% % 2.
unblockedStatementSupportingDefenceContraries(T, S, "O") :- playedNonBlockedStatement(T, S, "O"), unblockedRuleSupportingDefenceContraries(T, RId, "O"), body(RId, S).
% % 3.
unblockedRuleSupportingDefenceContraries(T, RId, "O") :- playedNonBlockedRule(T, RId, "O"), head(RId, H), unblockedStatementSupportingDefenceContraries(T, H, "O").

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Culprit candidates 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
culpritCandidate(T, C) :- assumption(C), unblockedStatementSupportingDefenceContraries(T, C, "O").


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Propagate from the previous step
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
stateRule(T1, RId, P) :- moveStep(T1), stateRule(T2, RId, P), T1 >= T2.
stateStatement(T1, S, P) :- moveStep(T1), stateStatement(T2, S, P), T1 >= T2.

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
possibleMove(T, "PB1", RId) :- remainingUnblockedRule(T, RId, "P"), head(RId, H), unexpandedStatement(T, H, "P").

% % PB2
culpritCandidateContrary(T, Ctr) :- culpritCandidate(T, Cul), contrary(Cul, Ctr).

possibleMove(T, "PB2", RId) :- remainingUnblockedRule(T, RId, "P"), head(RId, Ctr), culpritCandidateContrary(T, Ctr), not stateStatement(T, Ctr, "P"), not defenceContrary(T, Ctr).

% % PF1
notPossibleForwardRule(T, RId, "P") :- remainingUnblockedRule(T, RId, "P"), body(RId, B), incompleteStatement(T, B, "P").

possibleForwardRule(T, RId, "P") :- remainingUnblockedRule(T, RId, "P"), not notPossibleForwardRule(T, RId, "P"). 
nonEmptyBodyRule(RId) :- head(RId, _), body(RId, _).
emptyBodyRule(RId) :- not nonEmptyBodyRule(RId), head(RId, _).
possibleForwardRule(T, RId, "P") :- remainingUnblockedRule(T, RId, "P"), emptyBodyRule(RId).
possibleMove(T, "PF1", RId) :- possibleForwardRule(T, RId, "P").

% % PF2
possibleMove(T, "PF2", A) :- culpritCandidateContrary(T, A), assumption(A), not stateStatement(T, A, "P"), not inconsistentAssumption(A), not culprit(T, A), not defenceContrary(T, A).


% % OB1
possibleMove(T, "OB1", RId) :- remainingUnblockedRule(T, RId, "O"), head(RId, H), unblockedStatementSupportingDefenceContraries(T, H, "O").

% % OB2
possibleMove(T, "OB2", RId) :- remainingUnblockedRule(T, RId, "O"), head(RId, H), defenceContrary(T, H).

% % OF1 - not available for moves, but for termination criteria

notPossibleForwardRule(T, RId, "O") :- remainingUnblockedRule(T, RId, "O"), body(RId, B), not unblockedCompleteStatement(T, B, "O").

possibleForwardRule(T, RId, "O") :- remainingUnblockedRule(T, RId, "O"), not notPossibleForwardRule(T, RId, "O").
possibleMove(T, "OF1", RId) :- possibleForwardRule(T, RId, "O").  

% % OF2
possibleMove(T, "OF2", A) :- defenceContrary(T, A), assumption(A), not stateStatement(T, A, "O"), not culprit(T, A).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Moves
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
moveStep(0).
moveStep(T) :- move(T, _, _).
% % get max possible move number
haveGreater(X) :- moveStep(X), moveStep(Y), Y > X.
maxStep(X) :- moveStep(X), not haveGreater(X).

% for debugging - check possible moves at maxMoves step
maxStepPosMove(T, Type, X) :- possibleMove(T, Type, X), maxStep(T), advancementMoveType(Type).
gameOver(maxMove).

% choose 1 move
1 { move(T+1,Type,X) : possibleMove(T, Type, X),  advancementMoveType(Type) } 1 :- moveStep(T), not gameOver(T). 


% update states after performing moves
stateStatement(T, S, P) :- move(T, Type, RId), ruleMoveType(Type), proponentMove(Type), body(RId, S), player(P).

stateStatement(T, S, P) :- move(T, Type, RId), ruleMoveType(Type), proponentMove(Type), head(RId, S), player(P).

stateStatement(T, A, P) :- move(T, Type, A), assMoveType(Type), proponentMove(Type), assumption(A), player(P).

stateRule(T, RId, P) :- move(T, Type, RId), ruleMoveType(Type), proponentMove(Type), player(P).


stateStatement(T, S, "O") :- move(T, Type, RId), ruleMoveType(Type), opponentMove(Type), body(RId, S).

stateStatement(T, S, "O") :- move(T, Type, RId), ruleMoveType(Type), opponentMove(Type), head(RId, S).

stateStatement(T, A, "O") :- move(T, Type, A), assMoveType(Type), opponentMove(Type), assumption(A).

stateRule(T, RId, "O") :- move(T, Type, RId), ruleMoveType(Type), opponentMove(Type).


% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% termination criteria
incompleteGoal(T, G) :- goal(G), incompleteStateStatement(T, G, "P").

incompleteCulpritContrary(T, Ctr) :- culpritContrary(T, Ctr), incompleteStateStatement(T, Ctr, "P").

taCondition1Violated1(T) :- incompleteGoal(T, _).
taCondition1Violated2(T) :- incompleteCulpritContrary(T, _).

taCondition1(T) :- moveStep(T), not taCondition1Violated1(T), not taCondition1Violated2(T).

taCondition2Violated(T) :- defenceContrary(T, C), unblockedCompleteStatement(T, C, "O").

taCondition2(T) :- moveStep(T), not taCondition2Violated(T).
taCondition(T) :- taCondition1(T), taCondition2(T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% opp cannot move
oppCanMoveTermination(T) :- possibleMove(T, "OB1", _).
oppCanMoveTermination(T) :- possibleMove(T, "OB2", _).
oppCanMoveTermination(T) :- possibleMove(T, "OF2", _).

% prop cannot move
propCanMoveTermination(T) :- possibleMove(T, "PB1", _).
propCanMoveTermination(T) :- possibleMove(T, "PB2", _).
propCanMoveTermination(T) :- possibleMove(T, "PF2", _).

proponentWon(T) :- moveStep(T), taCondition(T), not oppCanMoveTermination(T).
opponentWon(T) :- moveStep(T), not taCondition(T), not propCanMoveTermination(T).
 
gameOver(T) :- proponentWon(T).
gameOver(T) :- opponentWon(T).

:- maxStep(T), not proponentWon(T).

% debugging
% :-maxStep(T), T!=maxMove.
