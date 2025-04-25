% pseudo encoding

% initialise
% maxStep(N). N = 0, 1, ... 
#program maxStep(t).

step(1..t) :- maxStep(t).

{ move(T, X) : possible(X) } = 1 :- step(T) . 
:- move(T, X), not incorrectMove(T, X). 

end(p) :- proponentWon(X), maxStep(X).
end(o) :- opponentWon(X), maxStep(X).