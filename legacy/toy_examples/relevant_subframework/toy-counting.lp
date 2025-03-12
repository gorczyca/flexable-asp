% Facts
fact(1).
fact(2).
fact(3).
fact(4).

% Rule to count facts where X > 2
asd(N) :- N = #count { X : fact(X), X > 2 }.
dsa(N) :- N = #count { X : fact(X) }.

% Display only N
% #show N/0.

#show.
#show X : asd(A), dsa(B), X=A+B.