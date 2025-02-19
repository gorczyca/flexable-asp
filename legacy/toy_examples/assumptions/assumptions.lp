#program base.

atoms(a;b).
% { x(A): atoms(A) }.
{ x(A): atoms(A) }.

a :- x(a).
b :- x(b).

% #show x/1.