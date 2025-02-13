head(0, s).
body(0, r).

goal(s).
trivial :- goal(s), not head(_, s), not assumption(s).    
:- not trivial.