% clingo logicProgram.lp -c maxMove=100 -c argGoal=s

step(1..maxMove). % # provide max move by 
goal(argGoal).


% #program base. <- remove the program directives

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Definitions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Move types
moveType("PB1";"PB2";"PF1";"OB1";"OB2";"OF1";"PF2";"OF2").
advancementMoveType("PB1";"PB2";"PF1";"OB1";"OB2";"PF2";"OF2"). % no OF1
proponentMove("PB1";"PB2";"PF1";"PF2").
opponentMove("OB1";"OB2";"OF1";"OF2").
ruleMoveType("PB1";"PB2";"PF1";"OB1";"OB2";"OF1").
assMoveType("PF2";"OF2").
% Players
player("P";"O").
% Mark moves that result in branching
branchingMove("PB1";"PB2";"PF2").
nonBranchingMove("PF1";"OB1";"OB2";"OF1";"OF2").

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Framework pre-processing
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Extract statements
statement(S) :- assumption(S).
statement(S) :- contrary(S, _).
statement(S) :- contrary(_, S).
statement(S) :- goal(S).
statement(S) :- head(_, S).
statement(S) :- body(_, S).
% Mark inconsistent assumptions
inconsistentAssumption(A) :- assumption(A), contrary(A, A).
% Mark empty-body rules
nonEmptyBodyRule(RId) :- head(RId, _), body(RId, _).
emptyBodyRule(RId) :- not nonEmptyBodyRule(RId), head(RId, _).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Initialize dispute derivation
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

stateStatement(0, S, "P") :- goal(S).

%  rules attacking themselves
remainingRuleBlocked(0, RId, "P") :- body(RId, B), head(RId,H), contrary(B,H).
remainingRuleBlocked(0, RId, "P") :- body(RId, B1), body(RId,B2), contrary(B1,B2).


% #program updateState(t).
% TODO: here first explicitly rewrite everything monotonic from the previous steps
% now the difference is, you have to write the steps into every predicate manually


stateRule(T, RId, P) :- stateRule(T-1, RId, P), step(T).
stateStatement(T, S, P) :- stateStatement(T-1, S, P), step(T) .

completeStateStatement(T, S, P) :- completeStateStatement(T-1, S, P), step(T).
completeStateRule(T, RId, P) :- completeStateRule(T-1, RId, P), step(T).

defence(T, D) :- defence(T-1, D), step(T).
defenceContrary(T, C) :- defenceContrary(T-1, C), step(T).
culprit(T, C) :- culprit(T-1, C), step(T).
culpritContrary(T, Ctr) :- culpritContrary(T-1, Ctr), step(T).

ruleHead(T, H, P) :- ruleHead(T-1, H, P), step(T).

stateFullyExpandedStatement(T, S, "O") :- stateFullyExpandedStatement(T-1, S, "O"), step(T).

playedBlockedStatement(T, S, "O") :- playedBlockedStatement(T-1, S, "O"), step(T).
playedBlockedRule(T, RId, "O") :- playedBlockedRule(T-1, RId, "O"), step(T).
stateFullyExpandedStatementNotAssumption(T, S, "O") :- stateFullyExpandedStatementNotAssumption(T-1, S, "O"), step(T).


move(T) :- move(T, _, _).

% add everything from P to O
stateStatement(T, S, "O") :- stateStatement(T, S, "P"). % copy safely
stateRule(T, RId, "O") :- stateRule(T, RId, "P").  % copy safely

dependency(T, H, B, P) :- dependency(T-1, H, B, P), step(T).

remainingRuleBlocked(T, RId, P) :- remainingRuleBlocked(T-1, RId, P), step(T-1).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Complete statements / rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% every assumption is a complete statement
completeStateStatement(T, S, P) :- stateStatement(T, S, P), assumption(S). % copy safely

% incomplete statements (auxiliary), that are in player's sets
incompleteStateStatement(T, S, P) :- stateStatement(T, S, P), not completeStateStatement(T, S, P). 

incompleteStateRule(T, RId, P) :- stateRule(T, RId, P), body(RId, B), incompleteStateStatement(T, B, P). 

completeStateRule(T, RId, P) :- stateRule(T, RId, P), not incompleteStateRule(T, RId, P). % copy safely

completeStateStatement(T, S, P):-completeStateRule(T, RId, P), head(RId, S). % copy safely

% incomplete statements (not necessarily in players sets)
incompleteStatement(T, S, P) :- player(P), statement(S), not completeStateStatement(T, S, P), step(T). 

% fight cycles
% for the opponent, it is possible to have circular dependencies and still win - they just need to create another complete argument without these dependencies. This solution filters out such cases. But at least it should be correct

dependency(T, H, B, P) :- stateRule(T, RId, P), head(RId, H), body(RId, B). % copy safely
dependency(T, H, B2, P) :- stateRule(T, RId, P), head(RId, H), body(RId, B1), dependency(T, B1, B2, P). % copy safely
incompleteStateStatement(T, S, P) :- dependency(T, S, S, P). % incomplete if depends on itself - should be fixed for the opp % copy safely

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Defences
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
defence(T, D) :- stateStatement(T, D, "P"), assumption(D). % copy safely
defenceContrary(T, C) :- defence(T, D), contrary(D, C). % copy safely

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Culprits
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
culprit(T, C) :- stateStatement(T, S, "P"), contrary(C, S). % copy safely
culpritContrary(T, Ctr) :- culprit(T, C), contrary(C, Ctr). % copy safely

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining opponent rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
remainingRule(T, RId, "O") :- not stateRule(T, RId, "O"), head(RId, _), step(T).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining proponent rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% auxiliary rule heads at state T
ruleHead(T, H, P) :- stateRule(T, RId1, P), head(RId1, H), player(P). % copy safely
remainingRule(T, RId1, "P") :- not ruleHead(T, H, "P"), head(RId1, H), step(T).
remainingRule(T, RId1, "P") :- not stateStatement(T, H, "P"), head(RId1, H), step(T).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining proponent blocked rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

remainingRuleBlocked(T, RId, "P") :- remainingRule(T, RId, "P"), body(RId, B), culprit(T, B).                     

remainingRuleBlocked(T, RId, "P") :- remainingRule(T, RId, "P"), body(RId, B), defenceContrary(T, B).             
                                                                         
remainingRuleBlocked(T, RId, "P") :- remainingRule(T, RId, "P"), head(RId, H), defenceContrary(T, H).             

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Remaining Opponent blocked rules
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
stateFullyExpandedStatement(T, S, "O") :- stateStatement(T, S, "O"), not stateExpandableStatement(T, S, "O"). % copy


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Played blocked pieces
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %   statements
playedBlockedStatement(T, S, "O") :- stateStatement(T, S, "O"), culprit(T, S). % copy
% %   rules
playedBlockedRule(T, RId, "O") :- stateRule(T, RId, "O"), body(RId, B), playedBlockedStatement(T, B, _). % copy
% %   statements 2
% %       auxiliaries
stateFullyExpandedStatementNotAssumption(T, S, "O") :- stateFullyExpandedStatement(T, S, "O"), not assumption(S). % copy
% %
playedNonBlockedRule(T, RId, "O") :- stateRule(T, RId, "O"), not playedBlockedRule(T, RId, "O").
% % 

% auxiliary
% statements for which there are unblocked rules
playedUnblockedStatement(T, S, "O") :- stateRule(T, RId, "O"), not playedBlockedRule(T, RId, "O"), head(RId, S).

playedBlockedStatement(T, S, "O") :- stateFullyExpandedStatementNotAssumption(T, S, "O"), not playedUnblockedStatement(T, S, "O"). % copy

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
% stateRule(T, RId, P) :- stateRule(T-1, RId, P).
% stateStatement(T, S, P) :- stateStatement(T-1, S, P).

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
possibleMove(T, "PB1", RId) :- remainingUnblockedRule(T, RId, "P"), head(RId, H), unexpandedStatement(T, H, "P").

% % PB2
culpritCandidateContrary(T, Ctr) :- culpritCandidate(T, Cul), contrary(Cul, Ctr).

possibleMove(T, "PB2", RId) :- remainingUnblockedRule(T, RId, "P"), head(RId, Ctr), culpritCandidateContrary(T, Ctr), not stateStatement(T, Ctr, "P"), not defenceContrary(T, Ctr).

% % PF1
notPossibleForwardRule(T, RId, "P") :- remainingUnblockedRule(T, RId, "P"), body(RId, B), incompleteStatement(T, B, "P").

possibleForwardRule(T, RId, "P") :- remainingUnblockedRule(T, RId, "P"), not notPossibleForwardRule(T, RId, "P"). 

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

taCondition1(T) :- not taCondition1Violated1(T), not taCondition1Violated2(T), step(T).

taCondition2Violated(T) :- defenceContrary(T, C), unblockedCompleteStatement(T, C, "O").

taCondition2(T) :- not taCondition2Violated(T), step(T).
taCondition(T) :- taCondition1(T), taCondition2(T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

nonBranchingMovePossible(T) :- possibleMove(T, Type, _), nonBranchingMove(Type), step(T).
onlyBranchingMovesPossible(T) :- not nonBranchingMovePossible(T), step(T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% opp cannot move
oppCanMoveTermination(T) :- possibleMove(T, "OB1", _).
oppCanMoveTermination(T) :- possibleMove(T, "OB2", _).
oppCanMoveTermination(T) :- possibleMove(T, "OF2", _).

% prop cannot move
propCanMoveTermination(T) :- possibleMove(T, "PB1", _).
propCanMoveTermination(T) :- possibleMove(T, "PB2", _).
propCanMoveTermination(T) :- possibleMove(T, "PF2", _).

proponentWon(T) :- taCondition(T), not oppCanMoveTermination(T), step(T).
opponentWon(T) :- not taCondition(T), not propCanMoveTermination(T), step(T).


% just for easier presentation

moveAss(T, Type, A) :- move(T, Type, A), assMoveType(Type).
moveRuleHead(T, Type, H) :- move(T, Type, RId), ruleMoveType(Type), head(RId, H).
moveRuleBody(T, Type, B) :- move(T, Type, RId), ruleMoveType(Type), body(RId, B).

% 
remainingPropRule(T, H) :- remainingRule(T, RId, "P"), head(RId, H).
propRuleHead(T, H) :- ruleHead(T, H, "P").

pf1Possible(T) :- possibleMove(T, "PF1", _).
pf1NotPossible(T) :- not pf1Possible(T), step(T).


% IF there are possible non-branching moves, perform them all
move(T, Type, X) :- possibleMove(T-1, Type, X), nonBranchingMove(Type), step(T). % continue here should not be that important, but should not harm
% ELSE chooes a single branching move 
{ move(T, Type, X) : possibleMove(T-1, Type, X),  advancementMoveType(Type), branchingMove(Type)  } = 1 :- onlyBranchingMovesPossible(T-1), step(T).
