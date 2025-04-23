#program base.
gameOver(0, "O") :- goal(G), contrary(G, G).
move(0, "P", G) :- goal(G). 
% self(X) :- contrary(X, X).

#program updateState(t).
culprit(t, C) :- move(_, "P", P), contrary(C, P).

% possibleMove(t, "P", P) :- move(_, "O", O), contrary(O, P), not culprit(_, P), not move(_, "P", P), not contrary(P, P), not contrary(D1, P) : move(_, "P", D1).
possibleMove(t, "P", P) :- move(_, "O", O), contrary(O, P), not culprit(_, P), not move(_, "P", P), not contrary(P,P), not contrary(D1, P) : move(_, "P", D1).
% possibleMove(t, "P", P) :- move(_, "O", O), contrary(O, P), not contrary(O, P1) : move(_, "P", P1), not contrary(P, P1) : move(_, "P", P1).
% possibleMove(t, "O", O) :- move(_, "P", P), contrary(P, O), not contrary(O, P1) : move(_, _, P1).
possibleMove(t, "O", O) :- move(_, "P", P), contrary(P, O), not culprit(_, O), not move(_, "O", O). % not contrary(O, O).


gameOver(t, "P") :- not possibleMove(t, "O", _), culprit(_, O1) : move(_, "O", O1). 
gameOver(t, "O") :- not possibleMove(t, "P", _), move(_, "O", O), not contrary(O, P1) : move(_, "P", P1) .

#program step(t).
move(t, "O", A) :- possibleMove(t-1, "O", A), not possibleMove(t-1, "P", _) .
{ move(t, "P", A) : possibleMove(t-1, "P", A) } = 1 :- not possibleMove(t-1, "O", _) .

#show move/3.
#show possibleMove/3.
#show self/1.