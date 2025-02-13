atoms(a;b;c;d).

goodAtoms(a;c).

betterAtoms(c;d).


on.

{ chosen(X) : atoms(X), goodAtoms(X), betterAtoms(X) } = 1 :- on.

#show chosen/1.