% Maze things

nonmember(X,L) :- nmem(L,X).
nmem([],_).
nmem([H|T],X) :- dif(H,X),nmem(T,X).


solve(X,Y,P,N) :- solve(X,Y,P,N,[X,Y]).
solve(X,Y,P,N,_) :- (pway(X,Y,L);pway(Y,X,L)),P=[X,Y],N is L.
solve(X,Y,P,N,S) :- (pway(X,Z,L);pway(Z,X,L)),nonmember(Z,S),solve(Z,Y,NP,NL,[Z|S]),P=[X|NP],N is L + NL.


solveSorted(X,Y,_,N) :- setof([N,S],solve(X,Y,S,N),P),popResult(P).

popResult([]).
popResult([[H1|[H2|_]]|T3]) :- write('N = '), write(H1),nl,write('P = '),write(H2),nl,popResult(T3).

splitlist([H|T],H,T).
