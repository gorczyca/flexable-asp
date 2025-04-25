% pseudo encoding

% initialise
% maxStep(N). N = 0, 1, ... 

#program updateState(t).

end(t, p) :- proponentWon(X), maxStep(X).
end(t, o) :- opponentWon(X), maxStep(X).

:- move(t, X), not incorrectMove(t, X). 

{ move(t, X) : possible(t-1,X) } = 1. 

possible(t, X) :- "[check which moves are possible]" 