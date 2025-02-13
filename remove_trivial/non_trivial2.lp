assumption(s).

goal(s).
trivial :- goal(s), not head(_, s), not assumption(s).    
:- not trivial.