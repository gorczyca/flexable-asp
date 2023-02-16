#include <incmode>.


#program base.
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

turn(0, P1) :-  playedPiece(0, P2, _), player(P1), P1 != P2.
usedPiece(0, Id) :- playedPiece(0, _, Id).
remainingPiece(0, Id) :- piece(Id), not usedPiece(0, Id).
possibleMove(0, Id) :- state(0,_,X), remainingPiece(0, Id), piece(Id, _, X).

% display
pPlayedPiece(0, Id, L, R) :- playedPiece(0, _, Id), piece(Id, l, L), piece(Id, r, R).
pState(0,L,R) :- state(0, l, L), state(0, r, R).  % to display nicely

#program step(t).
{ playedPiece(t, P, Id) : possibleMove(t-1, Id), turn(t-1, P) } = 1.

usedPiece(t, Id) :- playedPiece(t, _, Id).
usedPiece(t, Id) :- usedPiece(t-1, Id).

remainingPiece(t, Id) :- piece(Id), not usedPiece(t, Id).
turn(t, P1) :-  playedPiece(t, P2, _), player(P1), P1 != P2.

possibleMove(t, Id) :- state(t,_,X), remainingPiece(t, Id), piece(Id,_,X).

{ updatedState(t, Side, X) : playedPiece(t, _, Id), piece(Id, PSide1, X), piece(Id, PSide2, Y), PSide1 != PSide2, state(t-1, Side, Y) } = 1.

% copy untouched state
state(t, Side1, X) :- state(t-1, Side1, X), updatedState(t, Side2, _), Side1 != Side2.
% update the updated state
state(t, Side, X) :- updatedState(t, Side, X).

playerWon(t, P1) :- turn(t, P2), P1 != P2, player(P1), not possibleMove(t, _).

% only to display
pPlayedPiece(t, Id, L, R) :- playedPiece(t, _, Id), piece(Id, l, L), piece(Id, r, R).
pState(t,L,R) :- state(t, l, L), state(t, r, R).  


#program check(t).
:- query(t), not playerWon(t, "P1").

%------------------------
% Display
% #show playedPiece/3.
#show pPlayedPiece/4.
#show pState/3.
#show playerWon/2.
% #show state/3.
% #show usedPiece/2.
% #show moveStep/1.
% #show turn/2.
% #show possibleMove/2.
% #show updatedState/3.
% #show remainingPiece/2.
% #show gameOver/1.