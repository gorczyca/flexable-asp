assumption(p).
head(1, r).
body(1, a).

goal(s).
trivial :- goal(s), not head(_, s), not assumption(s).    
:- not trivial.