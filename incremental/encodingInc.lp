#include <incmode>.
#const goal=g.

#program base.
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

% inconsistent assumptions
inconsistentAssumption(A) :- assumption(A), contrary(A, A).

%
nonEmptyBodyRule(RId) :- head(RId, _), body(RId, _).
emptyBodyRule(RId) :- not nonEmptyBodyRule(RId), head(RId, _).

% add goals to both: P and B at T=0
stateStatement(0, S, P) :- goal(S), player(P).
completeStateStatement(0, S, P) :- stateStatement(0, S, P), assumption(S). % the only complete state statements at T0 are goals that are assumptions
incompleteStateStatement(0, S, P) :- stateStatement(0, S, P), not completeStateStatement(0, S, P).

% incomplete statements (possibly, but not necessarily in player's sets)
incompleteStatement(0, S, P) :- player(P), statement(S), not completeStateStatement(0, S, P).

% defences / defences contraries
defence(0, D) :- stateStatement(0, D, "P"), assumption(D).
defenceContrary(0, C) :- defence(0, D), contrary(D, C).

% culprit / culprit contraries
culprit(0, C) :- stateStatement(0, S, "P"), contrary(C, S).
culpritContrary(0, Ctr) :- culprit(0, C), contrary(C, Ctr).

% Remaining rules for both players - at first all of them
remainingRule(0, RId, P) :- head(RId, _), player(P). % all are remaining at first

% Remaining proponent blocked rules - TODO: these should remain blocked and not be recalculated in next steps
%  rules attacking themselves
remainingRuleBlocked(0, RId, "P") :- body(RId, B), head(RId,H), contrary(B,H).
remainingRuleBlocked(0, RId, "P") :- body(RId, B1), body(RId,B2), contrary(B1,B2).
% % remaining rules blocked for the proponent
% %   due to culprit in the body
remainingRuleBlocked(0, RId, "P") :- remainingRule(0, RId, "P"), body(RId, B), culprit(0, B).
% %   due to defence contrary:
% %       in the body of the rule
remainingRuleBlocked(0, RId, "P") :- remainingRule(0, RId, "P"), body(RId, B), defenceContrary(0, B).
% %       in the head of the rule
remainingRuleBlocked(0, RId, "P") :- remainingRule(0, RId, "P"), head(RId, H), defenceContrary(0, H).


% Remaining opponent blocked rules
remainingRuleBlocked(0, RId, "O") :- remainingRule(0, RId, "O"), body(RId, B), culprit(0, B).


% Remaining unblocked rules for both players
remainingUnblockedRule(0, RId, P) :- remainingRule(0, RId, P), not remainingRuleBlocked(0, RId, P).

% Unexpanded proponent statements  TODO: make sure not assumptions in the incremental part?
unexpandedStatement(0, S, "P") :- stateStatement(0, S, "P"), not assumption(S).

% Fully expanded opponents statements
stateExpandableStatement(0, S, "O") :- stateStatement(0, S, "O"), remainingUnblockedRule(0, RId, "O"), head(RId, S).
stateFullyExpandedStatement(0, S, "O") :- stateStatement(0, S, "O"), not stateExpandableStatement(0, S, "O").


% -----------------------

stateFullyExpandedStatementNotAssumption(0, S, "O") :- stateFullyExpandedStatement(0, S, "O"), not assumption(S).

unblockedCompleteStatement(0, S, "O") :- stateStatement(0, S, "O"), assumption(S), not culprit(0, S).

playedNonBlockedStatement(0, S, "O") :- stateStatement(0, S, "O").


% ------------------------
% Possible moves at step 0
% PB1
possibleMove(0, "PB1", RId) :- remainingUnblockedRule(0, RId, "P"), head(RId, H), unexpandedStatement(0, H, "P").

% PB2 - no culprit candidates at T0

% PF1
notPossibleForwardRule(0, RId, "P") :- remainingUnblockedRule(0, RId, "P"), body(RId, B), incompleteStatement(0, B, "P").
possibleForwardRule(0, RId, "P") :- remainingUnblockedRule(0, RId, "P"), not notPossibleForwardRule(0, RId, "P"). 
possibleForwardRule(0, RId, "P") :- remainingUnblockedRule(0, RId, "P"), emptyBodyRule(RId).
possibleMove(0, "PF1", RId) :- possibleForwardRule(0, RId, "P").

% PF2 - no culprit candidate at T0
% OB1 - no statements supporting defence contraries at T0

% OB2
possibleMove(0, "OB2", RId) :- remainingUnblockedRule(0, RId, "O"), head(RId, H), defenceContrary(t, H).

% OF1 - not available for moves, but for termination criteria
notPossibleForwardRule(0, RId, "O") :- remainingUnblockedRule(0, RId, "O"), body(RId, B), not unblockedCompleteStatement(0, B, "O").
possibleForwardRule(0, RId, "O") :- remainingUnblockedRule(0, RId, "O"), not notPossibleForwardRule(0, RId, "O").
possibleMove(0, "OF1", RId) :- possibleForwardRule(0, RId, "O").  

% % OF2
possibleMove(0, "OF2", A) :- defenceContrary(0, A), assumption(A), not stateStatement(0, A, "O"), not culprit(0, A).

% ------------------------------------------
% termination criteria at step 0

% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% termination criteria
incompleteGoal(0, G) :- goal(G), incompleteStateStatement(0, G, "P").

% at step 0 incomplete culprit contrary can be only the incomplete goal

taCondition1Violated1(0) :- incompleteGoal(0, _).
taCondition1(0) :- not taCondition1Violated1(0).
taCondition(0) :- taCondition1(t).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% opp cannot move
oppCanMoveTermination(0) :- possibleMove(0, "OB1", _).
oppCanMoveTermination(0) :- possibleMove(0, "OB2", _).
oppCanMoveTermination(0) :- possibleMove(0, "OF2", _).

% prop cannot move
propCanMoveTermination(0) :- possibleMove(0, "PB1", _).
propCanMoveTermination(0) :- possibleMove(0, "PB2", _).
propCanMoveTermination(0) :- possibleMove(0, "PF2", _).

proponentWon(0) :- taCondition(0), not oppCanMoveTermination(0).
opponentWon(0) :- not taCondition(0), not propCanMoveTermination(0).
 


% ------------------------------------------------
% end static part
% ------------------------------------------------
#program step(t).

% choose 1 move
{ move(t, Type, X) : possibleMove(t-1, Type, X),  advancementMoveType(Type) } = 1.

% add everything from P to O
stateStatement(t, S, "O") :- stateStatement(t, S, "P"). % done - only goals
stateRule(t, RId, "O") :- stateRule(t, RId, "P").       % done - no rules at step 0



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Complete statements / rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% every assumption is a complete statement
completeStateStatement(t, S, P) :- stateStatement(t, S, P), assumption(S).  % done

% incomplete statements (auxiliary), that are in player's sets
incompleteStateStatement(t, S, P) :- stateStatement(t, S, P), not completeStateStatement(t, S, P).  % done

incompleteStateRule(t, RId, P) :- stateRule(t, RId, P), body(RId, B), incompleteStateStatement(t, B, P). % done - no rules at T0

completeStateRule(t, RId, P) :- stateRule(t, RId, P), not incompleteStateRule(t, RId, P).   % done - no rules at T0

completeStateStatement(t, S, P):-completeStateRule(t, RId, P), head(RId, S).  % done - no rules at T0

% incomplete statements (not necessarily in players sets)
incompleteStatement(t, S, P) :- player(P), statement(S), not completeStateStatement(t, S, P). % done

% fight cycles
% for the opponent, it is possible to have circular dependencies and still win - they just need to create another complete argument without these dependencies. This solution filters out such cases. But at least it should be correct

dependency(t, H, B, P) :- stateRule(t, RId, P), head(RId, H), body(RId, B). % done - no rules at T0
dependency(t, H, B2, P) :- stateRule(t, RId, P), head(RId, H), body(RId, B1), dependency(t, B1, B2, P).
incompleteStateStatement(t, S, P) :- dependency(t, S, S, P). 


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Defences
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
defence(t, D) :- stateStatement(t, D, "P"), assumption(D).
defenceContrary(t, C) :- defence(t, D), contrary(D, C).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Culprits
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
culprit(t, C) :- stateStatement(t, S, "P"), contrary(C, S).
culpritContrary(t, Ctr) :- culprit(t, C), contrary(C, Ctr).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining opponent rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
remainingRule(t, RId, "O") :- not stateRule(t, RId, "O"), head(RId, _).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining proponent rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% auxiliary rule heads at state T
ruleHead(t, H, P) :- stateRule(t, RId1, P), head(RId1, H), player(P).
remainingRule(t, RId1, "P") :- not ruleHead(t, H, "P"), head(RId1, H).
remainingRule(t, RId1, "P") :- not stateStatement(t, H, "P"), head(RId1, H).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining proponent blocked rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   TODO: might be that these rules should be blocked for BOTH players, for now only prop
remainingRuleBlocked(t, RId, "P") :- body(RId, B), head(RId,H), contrary(B,H). % player(P).
remainingRuleBlocked(t, RId, "P") :- body(RId, B1), body(RId,B2), contrary(B1,B2). % player(P).   <------------------
% % remaining rules blocked for the proponent                                                                     %  |
% %   due to culprit in the body                                                                                  %  |
remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), body(RId, B), culprit(t, B).                     %  |
% %   due to defence contrary:                                                                                    %  |
% %       in the body of the rule                                                                                 %  |
remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), body(RId, B), defenceContrary(t, B).             %  |
% %       in the head of the rule                                                                                 %  |
remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), head(RId, H), defenceContrary(t, H).             %  |
% %   due to rule being inconsistent TODO: this has already been done above! ---------------------------------------
remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), body(RId, B1), body(RId, B2), contrary(B1, B2).


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
stateFullyExpandedStatement(t, S, "O") :- stateStatement(t, S, "O"), not stateExpandableStatement(t, S, "O").


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Played blocked pieces
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %   statements
playedBlockedStatement(t, S, "O") :- stateStatement(t, S, "O"), culprit(t, S).
% %   rules
playedBlockedRule(t, RId, "O") :- stateRule(t, RId, "O"), body(RId, B), playedBlockedStatement(t, B, _).
% %   statements 2
% %       auxiliaries
stateFullyExpandedStatementNotAssumption(t, S, "O") :- stateFullyExpandedStatement(t, S, "O"), not assumption(S).
% %
playedNonBlockedRule(t, RId, "O") :- stateRule(t, RId, "O"), not playedBlockedRule(t, RId, "O").
% % 

% auxiliary
% statements for which there are unblocked rules
playedUnblockedStatement(t, S, "O") :- stateRule(t, RId, "O"), not playedBlockedRule(t, RId, "O"), head(RId, S).

playedBlockedStatement(t, S, "O") :- stateFullyExpandedStatementNotAssumption(t, S, "O"), not playedUnblockedStatement(t, S, "O"). 

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
stateRule(t, RId, P) :- stateRule(t-1, RId, P).
stateStatement(t, S, P) :- stateStatement(t-1, S, P).

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
 

#program check(t).
:- query(t), not proponentWon(t).

#show move/3.
