#program base.
end(0,"O") :- g(G), ctr(G,G).
m(0,"P",G) :- g(G). 
#program updateState(t).
cul(t, C) :- m(_, "P", P), ctr(C, P).
pm(t, "P", P) :- m(_, "O", O), ctr(O, P), not cul(_, P), not m(_, "P", P), not ctr(P,P), not ctr(D1, P) : m(_, "P", D1).
pm(t, "O", O) :- m(_, "P", P), ctr(P, O), not cul(_, O), not m(_, "O", O). 
end(t, "P") :- not pm(t, "O", _), cul(_, O1) : m(_, "O", O1). 
end(t, "O") :- not pm(t, "P", _), m(_, "O", O), not ctr(O, P1) : m(_, "P", P1) .
#program step(t).
m(t, "O", A) :- pm(t-1, "O", A), not pm(t-1, "P", _) .
{ m(t, "P", A) : pm(t-1, "P", A) } = 1 :- not pm(t-1, "O", _) .