horizon(5).
step(0).
step(X) :- step(X-1), horizon(Y), Y > X.

{ i(X) : step(X) }.

#show i/1.