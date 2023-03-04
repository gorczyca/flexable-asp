#program base.
player("P1";"P2").

turn(0, "P1").
playerToWin("P1").

% auxiliary
piece(Id) :- piece(Id,_,_).

% exactly one piece gets chosen randomly to be the first one
{ playedPiece(0, P, Id) : piece(Id), turn(0, P) } = 1.
% for debugging I just fixed one - this could also come from the instance
% playedPiece(0, "P1", "03").

% initial state
state(0, l, L) :- playedPiece(0, _, Id), piece(Id, l, L).
state(0, r, R) :- playedPiece(0, _, Id), piece(Id, r, R).

% --------------------------------
% update the game after every move
% --------------------------------

#program updateMoves(t).
usedPiece(t, Id) :- playedPiece(_, _, Id).
remainingPiece(t, Id) :- piece(Id), not usedPiece(t, Id).
possibleMove(t, Id) :- state(t,_,X), remainingPiece(t, Id), piece(Id, _, X).
playerWon(t, P1) :- turn(t, P1), not possibleMove(t, _).
playerLost(t, P1) :- playerWon(t, P2), player(P1), P1 != P2.

% display
pPlayedPiece(t, Id, L, R) :- playedPiece(t, _, Id), piece(Id, l, L), piece(Id, r, R).
pState(t,L,R) :- state(t, l, L), state(t, r, R).  % to display nicely


% --------------------------------
% perform the next move
% --------------------------------
#program step(t).
turn(t, P1) :-  playedPiece(t-1, P2, _), player(P1), P1 != P2.

{ playedPiece(t, P, Id) : possibleMove(t-1, Id), turn(t, P) } = 1.
{ updatedState(t, Side, X) : playedPiece(t, _, Id), piece(Id, PSide1, X), piece(Id, PSide2, Y), PSide1 != PSide2, state(t-1, Side, Y) } = 1.

% copy untouched state
state(t, Side1, X) :- state(t-1, Side1, X), updatedState(t, Side2, _), Side1 != Side2.
% update the updated state
state(t, Side, X) :- updatedState(t, Side, X).


% ---------------------------------------
% check if still next moves are possible
% ---------------------------------------
#program checkIfNotOver(t).
#external notOver(t).
:- notOver(t), playerLost(t, P), playerToWin(P).


% --------------------------------
% check if P1 won
% --------------------------------
#program checkIfWon(t).
#external winning(t).
:- winning(t), not playerWon(t, P), playerToWin(P).

%------------------------
% Display

#show pPlayedPiece/4.
#show pState/3.
#show playerWon/2.
