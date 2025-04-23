% change GOAL to actual goal

goal(argGoal).

:- not supported(X), goal(X).


#show supported/1.

% run with


% clingo /home/piotr/Dresden/multishot/flexable-asp/test_instances/asp_for_aba_instances/exp_acyclic_depvary_step10_batch_yyy01.pl admissible.lp goal.lp -c argGoal=w2 

% clingo easy.lp admissible.lp goal.lp -c argGoal=x1

% /home/piotr/Dresden/multishot/flexable-asp/create_potential/instance.lp

% clingo /home/piotr/Dresden/multishot/flexable-asp/create_potential/instance.lp admissible.lp goal.lp -c argGoal=f1_s1