#program base. % -5 lines
moveType("PB1";"PB2";"PF1";"OB1";"OB2";"OF1";"PF2";"OF2").
advancementMoveType("PB1";"PB2";"PF1";"OB1";"OB2";"PF2";"OF2"). 
proponentMove("PB1";"PB2";"PF1";"PF2").
opponentMove("OB1";"OB2";"OF1";"OF2").
ruleMoveType("PB1";"PB2";"PF1";"OB1";"OB2";"OF1").
assMoveType("PF2";"OF2").
player("P";"O").
branchingMove("PB1";"PB2";"PF2").
nonBranchingMove("PF1";"OB1";"OB2";"OF1";"OF2").
statement(S) :- assumption(S) ; contrary(S, _) ; contrary(_, S) ; goal(S) ; head(_, S) ; body(_, S).
inconsistentAssumption(A) :- assumption(A), contrary(A, A).
emptyBodyRule(RId) :- head(RId, _), not body(RId, _). % <-
stateStatement(0, S, "P") :- goal(S).
remainingRuleBlocked(0, RId, "P") :- body(RId, B), head(RId,H), contrary(B,H).
remainingRuleBlocked(0, RId, "P") :- body(RId, B1), body(RId,B2), contrary(B1,B2).
#program updateState(t).
stateRule(t, RId, P) :- stateRule(t-1, RId, P). % <- copying from previous
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
stateStatement(t, S, "O") :- stateStatement(t, S, "P"). 
stateRule(t, RId, "O") :- stateRule(t, RId, "P"). 
dependency(t, H, B, P) :- dependency(t-1, H, B, P).
remainingRuleBlocked(t, RId, P) :- remainingRuleBlocked(t-1, RId, P).
completeStateStatement(t, S, P) :- stateStatement(t, S, P), assumption(S). 
% incompleteStateStatement(t, S, P) :- stateStatement(t, S, P), not completeStateStatement(t, S, P). 
% incompleteStateRule(t, RId, P) :- stateRule(t, RId, P), body(RId, B), incompleteStateStatement(t, B, P). 
% completeStateRule(t, RId, P) :- stateRule(t, RId, P), not incompleteStateRule(t, RId, P). 
% completeStateStatement(t, S, P):-completeStateRule(t, RId, P), head(RId, S). 
completeStateStatement(t, S, P) :- head(RId, S), player(P), move(t), completeStateStatement(t, S, P) : body(RId, S).  
% incompleteStatement(t, S, P) :- player(P), statement(S), not completeStateStatement(t, S, P). 
dependency(t, H, B, P) :- stateRule(t, RId, P), head(RId, H), body(RId, B).
dependency(t, H, B2, P) :- stateRule(t, RId, P), head(RId, H), body(RId, B1), dependency(t, B1, B2, P).
incompleteStateStatement(t, S, P) :- dependency(t, S, S, P).  % ???? what is this doing??? somehow prevents circular dependency
defence(t, D) :- stateStatement(t, D, "P"), assumption(D).
defenceContrary(t, C) :- defence(t, D), contrary(D, C). 
culprit(t, C) :- stateStatement(t, S, "P"), contrary(C, S).
culpritContrary(t, Ctr) :- culprit(t, C), contrary(C, Ctr). 
remainingRule(t, RId, "O") :- not stateRule(t, RId, "O"), head(RId, _).
ruleHead(t, H, P) :- stateRule(t, RId1, P), head(RId1, H), player(P). 
remainingRule(t, RId1, "P") :- not ruleHead(t, H, "P"), head(RId1, H).
remainingRule(t, RId1, "P") :- not stateStatement(t, H, "P"), head(RId1, H). % ???
remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), body(RId, B), culprit(t, B).                     
remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), body(RId, B), defenceContrary(t, B).                                                                                     
remainingRuleBlocked(t, RId, "P") :- remainingRule(t, RId, "P"), head(RId, H), defenceContrary(t, H).             
remainingRuleBlocked(t, RId, "O") :- remainingRule(t, RId, "O"), body(RId, B), culprit(t, B).
remainingUnblockedRule(t, RId, P) :- remainingRule(t, RId, P), not remainingRuleBlocked(t, RId, P).
unexpandedStatement(t, S, "P") :- stateStatement(t, S, "P"), not ruleHead(t, S, "P").
stateExpandableStatement(t, S, "O") :- stateStatement(t, S, "O"), remainingUnblockedRule(t, RId, "O"), head(RId, S).
stateFullyExpandedStatement(t, S, "O") :- stateStatement(t, S, "O"), not stateExpandableStatement(t, S, "O").
playedBlockedStatement(t, S, "O") :- stateStatement(t, S, "O"), culprit(t, S). 
playedBlockedRule(t, RId, "O") :- stateRule(t, RId, "O"), body(RId, B), playedBlockedStatement(t, B, _). 
stateFullyExpandedStatementNotAssumption(t, S, "O") :- stateFullyExpandedStatement(t, S, "O"), not assumption(S). 
playedNonBlockedRule(t, RId, "O") :- stateRule(t, RId, "O"), not playedBlockedRule(t, RId, "O").
playedUnblockedStatement(t, S, "O") :- stateRule(t, RId, "O"), not playedBlockedRule(t, RId, "O"), head(RId, S).
playedBlockedStatement(t, S, "O") :- stateFullyExpandedStatementNotAssumption(t, S, "O"), not playedUnblockedStatement(t, S, "O"). 
unblockedCompleteStatement(t, S, "O") :- stateStatement(t, S, "O"), assumption(S), not culprit(t, S).
incompleteNonBlockedRule(t, RId, "O") :- playedNonBlockedRule(t, RId, "O"), body(RId, B), not unblockedCompleteStatement(t, B, "O").
unblockedCompleteRule(t, RId, "O") :- playedNonBlockedRule(t, RId, "O"), not incompleteNonBlockedRule(t, RId, "O").
unblockedCompleteStatement(t, H, "O") :- unblockedCompleteRule(t, RId, "O"), head(RId, H).
playedNonBlockedStatement(t, S, "O") :- stateStatement(t, S, "O"), not playedBlockedStatement(t, S, "O").
unblockedStatementSupportingDefenceContraries(t, S, "O") :- defenceContrary(t, S), playedNonBlockedStatement(t, S, "O").
unblockedStatementSupportingDefenceContraries(t, S, "O") :- playedNonBlockedStatement(t, S, "O"), unblockedRuleSupportingDefenceContraries(t, RId, "O"), body(RId, S).
unblockedRuleSupportingDefenceContraries(t, RId, "O") :- playedNonBlockedRule(t, RId, "O"), head(RId, H), unblockedStatementSupportingDefenceContraries(t, H, "O").
culpritCandidate(t, C) :- assumption(C), unblockedStatementSupportingDefenceContraries(t, C, "O").
possibleMove(t, "PB1", RId) :- remainingUnblockedRule(t, RId, "P"), head(RId, H), unexpandedStatement(t, H, "P").
culpritCandidateContrary(t, Ctr) :- culpritCandidate(t, Cul), contrary(Cul, Ctr).
possibleMove(t, "PB2", RId) :- remainingUnblockedRule(t, RId, "P"), head(RId, Ctr), culpritCandidateContrary(t, Ctr), not stateStatement(t, Ctr, "P"), not defenceContrary(t, Ctr).
notPossibleForwardRule(t, RId, "P") :- remainingUnblockedRule(t, RId, "P"), body(RId, B), incompleteStatement(t, B, "P").
possibleForwardRule(t, RId, "P") :- remainingUnblockedRule(t, RId, "P"), not notPossibleForwardRule(t, RId, "P"). 
possibleForwardRule(t, RId, "P") :- remainingUnblockedRule(t, RId, "P"), emptyBodyRule(RId).
possibleMove(t, "PF1", RId) :- possibleForwardRule(t, RId, "P").
possibleMove(t, "PF2", A) :- culpritCandidateContrary(t, A), assumption(A), not stateStatement(t, A, "P"), not inconsistentAssumption(A), not culprit(t, A), not defenceContrary(t, A).
possibleMove(t, "OB1", RId) :- remainingUnblockedRule(t, RId, "O"), head(RId, H), unblockedStatementSupportingDefenceContraries(t, H, "O").
possibleMove(t, "OB2", RId) :- remainingUnblockedRule(t, RId, "O"), head(RId, H), defenceContrary(t, H).
notPossibleForwardRule(t, RId, "O") :- remainingUnblockedRule(t, RId, "O"), body(RId, B), not unblockedCompleteStatement(t, B, "O").
possibleForwardRule(t, RId, "O") :- remainingUnblockedRule(t, RId, "O"), not notPossibleForwardRule(t, RId, "O").
possibleMove(t, "OF1", RId) :- possibleForwardRule(t, RId, "O").  
possibleMove(t, "OF2", A) :- defenceContrary(t, A), assumption(A), not stateStatement(t, A, "O"), not culprit(t, A).
stateStatement(t, S, P) :- move(t, Type, RId), ruleMoveType(Type), proponentMove(Type), body(RId, S), player(P).
stateStatement(t, S, P) :- move(t, Type, RId), ruleMoveType(Type), proponentMove(Type), head(RId, S), player(P).
stateStatement(t, A, P) :- move(t, Type, A), assMoveType(Type), proponentMove(Type), assumption(A), player(P).
stateRule(t, RId, P) :- move(t, Type, RId), ruleMoveType(Type), proponentMove(Type), player(P).
stateStatement(t, S, "O") :- move(t, Type, RId), ruleMoveType(Type), opponentMove(Type), body(RId, S).
stateStatement(t, S, "O") :- move(t, Type, RId), ruleMoveType(Type), opponentMove(Type), head(RId, S).
stateStatement(t, A, "O") :- move(t, Type, A), assMoveType(Type), opponentMove(Type), assumption(A).
stateRule(t, RId, "O") :- move(t, Type, RId), ruleMoveType(Type), opponentMove(Type).
incompleteGoal(t, G) :- goal(G), incompleteStateStatement(t, G, "P").
incompleteCulpritContrary(t, Ctr) :- culpritContrary(t, Ctr), incompleteStateStatement(t, Ctr, "P").
taCondition1Violated1(t) :- incompleteGoal(t, _).
taCondition1Violated2(t) :- incompleteCulpritContrary(t, _).
taCondition1(t) :- not taCondition1Violated1(t), not taCondition1Violated2(t).
taCondition2Violated(t) :- defenceContrary(t, C), unblockedCompleteStatement(t, C, "O").
taCondition2(t) :- not taCondition2Violated(t).
taCondition(t) :- taCondition1(t), taCondition2(t).
nonBranchingMovePossible(t) :- possibleMove(t, Type, _), nonBranchingMove(Type).
onlyBranchingMovesPossible(t) :- not nonBranchingMovePossible(t).
oppCanMoveTermination(t) :- possibleMove(t, "OB1", _).
oppCanMoveTermination(t) :- possibleMove(t, "OB2", _).
oppCanMoveTermination(t) :- possibleMove(t, "OF2", _).
propCanMoveTermination(t) :- possibleMove(t, "PB1", _).
propCanMoveTermination(t) :- possibleMove(t, "PB2", _).
propCanMoveTermination(t) :- possibleMove(t, "PF2", _).
proponentWon(t) :- taCondition(t), not oppCanMoveTermination(t).
opponentWon(t) :- not taCondition(t), not propCanMoveTermination(t).
moveAss(t, Type, A) :- move(t, Type, A), assMoveType(Type).
moveRuleHead(t, Type, H) :- move(t, Type, RId), ruleMoveType(Type), head(RId, H).
moveRuleBody(t, Type, B) :- move(t, Type, RId), ruleMoveType(Type), body(RId, B).
remainingPropRule(t, H) :- remainingRule(t, RId, "P"), head(RId, H).
propRuleHead(t, H) :- ruleHead(t, H, "P").
pf1Possible(t) :- possibleMove(t, "PF1", _).
pf1NotPossible(t) :- not pf1Possible(t).
propRule(t, RId) :- move(_, Type, RId), ruleMoveType(Type), proponentMove(Type).
propAss(t, A) :- move(_, Type, A), assMoveType(Type), proponentMove(Type).
#program step(t).
move(t, Type, X) :- possibleMove(t-1, Type, X), nonBranchingMove(Type).
{ move(t, Type, X) : possibleMove(t-1, Type, X),  advancementMoveType(Type), branchingMove(Type)  } = 1 :- onlyBranchingMovesPossible(t-1). 
#show move/3.
#show propAss/2.
#show propRule/2.
