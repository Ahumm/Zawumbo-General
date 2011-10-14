% Representation for production is analogous to that
% in Problem 1. 

prod(1,[non(e,_),non(e,_),term(minus,_),non(t,_)]).
prod(2,[non(e,_),non(t,_)]).
prod(3,[non(t,_),non(t,_),term(mul,_),term(num,_)]).
prod(4,[non(t,_),term(num,_)]).

% YOUR CODE HERE.
% Complete the SLR(1) parsing table. Predicates action() encode the
% parsing actions. E.g., action(0,term(num,_),shift,3)
% stands for "on state 0 and terminal num, shift to state 3". Similarly,
% action(2,term(minus,_),reduce,2) stands for "on state 2 and terminal 
% minus, reduce by production 2". Predicates goto() encode goto
% transitions. E.g., goto(0,non(e,_),1) encodes that on state 0
% and nonterminal E, the parser moves to state 1. 

action(0,term(num,_),shift,3).
action(1,term(minus,_),shift,4).
%%%%%%%%%%%%%%%%%%%%%%%action(1,term(end,_),
action(2,term(minus,_),reduce,2)
action(2,term(mul,_),shift,5)
action(2,term(end,_),reduce,2)
%
action(3,term(minus,_),reduce,4)
action(3,term(mul,_),reduce,4)
action(3,term(end,_),reduce,4)
%
action(4,term(num,_),shift,3)
%
action(5,term(num,_),shift,5)
%
action(6,term(minus,_),reduce,1)
action(6,term(mul,_),shift,5)
action(6,term(end,_),reduce,1)
%
action(7,term(minus,_),reduce,3)
action(7,term(mul,_),reduce,3)
action(7,term(end,_),reduce,3)

goto(0,non(e,_),1).
goto(0,non(t,_),2).
goto(4,non(t,_),6).


% Complete the attribute table. Predicates attribute() encode the
% extension of the grammar which computes the value of the expression.

attribute(1,[non(e,A),non(e,A1),term(minus,_),non(t,A2)]):- % YOUR CODE HERE
attribute(2,[non(e,A),non(t,A1)]).
attribute(3,[non(t,A),non(t,A1),term(mul,_),term(num,A2)]).
attribute(4,[non(t,A),term(num,A1)]).

% YOUR CODE HERE.
% As with the LL(1) parser, begin with transform(L,R).

transform([],R) :- append([term(end,_)],[],R).
transform([-|Tail],R) :- transform(Tail, S), append([term(minus,_)],S,R).
transform([*|Tail],R) :- transform(Tail, S), append([term(mul,_)],S,R).
transform([A|Tail],R) :- transform(Tail, S), append([term(num,A)],S,R).

% Write parseLR(L,ProdSeq,V): it takes input list L and produces the
% production sequence applied by the shift-reduce parser in reverse.
% E.g., if input0([3,-,5], 
% input0(L),parseLR(L,ProdSeq, V).
% ProdSeq = [1, 4, 2, 4]
% V = -2.

