%  run with:
%%%  clingo /home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances/exp_acyclic_depvary_step1_batch_yyy01.pl relevant.lp 0

rulesNo(N) :- N = #count { Id: head(Id, _) } .
assumptionsNo(N) :- N = #count { A: assumption(A) } .

worstCase(X) :- X=2*(R+A), rulesNo(R), assumptionsNo(A).

%  calculate relevant statements
relevantStatement(S) :- goal(S).
relevantStatement(S) :- contrary(_, S).

relevantRule(Id) :- head(Id, H), relevantStatement(H).
relevantStatement(S) :- relevantRule(Id), body(Id, S).


relevantRulesNo(N) :- N = #count { Id: relevantRule(Id) } .

worstCaseRelevant(X) :- X=2*(R+A), relevantRulesNo(R), assumptionsNo(A).


#show rulesNo/1.
#show relevantRulesNo/1.
#show assumptionsNo/1.
#show worstCase/1.
#show worstCaseRelevant/1.