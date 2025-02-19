#program base.

initialAtom(i).
atom(a;b;c;d;e;i).

availAtom(0, A) :- atom(A), not initialAtom(A).
at(0, A) :- initialAtom(A).

% :- at(X, e), at(Y, i), at(Z, b), step(X), step(Y), step(Z).

#program updateState(t).
step(t).

used(t, A) :- atom(A), not availAtom(t, A).

% :- at(_, i), at(_, a).
% :- used(2, i), used(2, a).

{ at(t, A) :  availAtom(t-1, A) } = 1.
availAtom(t, A) :- availAtom(t-1, A), not at(t, A).

% { chosen(A): atom(A) } = 1.



#show at/2.
% #show used/2.
% #show step/1.
% #show availableAtom/2.
% #show availableAtom

% #show chosen/1.

