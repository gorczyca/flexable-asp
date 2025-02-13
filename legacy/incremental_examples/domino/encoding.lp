% debugging only
#const maxMove = 15.

player("P1";"P2").

% auxiliary
piece(Id) :- piece(Id,_,_).

% exactly one piece gets chosen randomly to be the first one
% { playedPiece(0, "P1", Id) : piece(Id) } = 1.
% for debugging I just fixed one - this could also come from the instance
playedPiece(0, "P1", "03").

% initial state
state(0, l, L) :- playedPiece(0, _, Id), piece(Id, l, L).
state(0, r, R) :- playedPiece(0, _, Id), piece(Id, r, R).


moveStep(T) :- playedPiece(T, _, _).
usedPiece(T, Id) :- playedPiece(T, _, Id).
usedPiece(T, Id) :- moveStep(T), usedPiece(T-1, Id).

remainingPiece(T, Id) :- piece(Id), not usedPiece(T, Id), moveStep(T).
turn(T, P1) :-  playedPiece(T, P2, _), player(P1), P1 != P2.

possibleMove(T, Id) :- state(T,_,X), remainingPiece(T, Id), piece(Id,_,X).

gameOver(maxMove).
gameOver(T) :- moveStep(T), not possibleMove(T, _).

{ playedPiece(T+1, P, Id) : possibleMove(T, Id) } = 1 :- turn(T, P), moveStep(T), not gameOver(T).

{ updatedState(T, Side, X) : playedPiece(T, _, Id), piece(Id, PSide1, X), piece(Id, PSide2, Y), PSide1 != PSide2, state(T-1, Side, Y) } = 1 :- moveStep(T), T > 0.

% copy untouched state
state(T, Side1, X) :- state(T-1, Side1, X), updatedState(T, Side2, _), Side1 != Side2.
% update the updated state
state(T, Side, X) :- updatedState(T, Side, X).

playerWon(T, P1) :- turn(T, P2), P1 != P2, player(P1), not possibleMove(T, _).

haveGreater(X) :- moveStep(X), moveStep(Y), Y > X.
maxStep(T) :- moveStep(T), not haveGreater(T).

:- maxStep(T), not playerWon(T, "P2").



%------------------------
% Display

pPlayedPiece(T, Id, L, R) :- playedPiece(T, _, Id), piece(Id, l, L), piece(Id, r, R).
pState(T,L,R) :- state(T, l, L), state(T, r, R).  % to display nicely

% #show playedPiece/3.
#show pPlayedPiece/4.
#show pState/3.
% #show playerWon/2.
% #show state/3.
% #show usedPiece/2.
% #show moveStep/1.
% #show turn/2.
% #show possibleMove/2.
% #show updatedState/3.
% #show remainingPiece/2.
% #show gameOver/1.