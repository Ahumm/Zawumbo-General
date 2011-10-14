% Maze things

pway(a, b, 10).
pway(b, c, 15).
pway(d, c, 5).
pway(d, b, 10).

pway(b, e, 7).
pway(e, c, 8).

pway(d, f, 5).
pway(c, f, 5). 

nonmember(X,L) :- nmem(L,X).
nmem([],_).
nmem([H|T],X) :- dif(H,X),nmem(T,X).


solve(X,Y,P,N) :- solve(X,Y,P,N,[X,Y]).
solve(X,Y,P,N,_) :- (pway(X,Y,L);pway(Y,X,L)),P=[X,Y],N is L.
solve(X,Y,P,N,S) :- (pway(X,Z,L);pway(Z,X,L)),nonmember(Z,S),solve(Z,Y,NP,NL,[Z|S]),P=[X|NP],N is L + NL.


solveSorted(X,Y,P,N) :- setof([N,S],solve(X,Y,S,N),F). 

