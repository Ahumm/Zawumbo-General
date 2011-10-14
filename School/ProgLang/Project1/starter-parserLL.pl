% Representation of grammar. Nonterminals E, T, E', and T' are
% represented by non(e,_), non(t,_), non(eprime,_), and non(tprime,_).
% Terminals num, -, and * are represented by term(num,_), term(minus,_)
% and term(mul,_). Special terminal term(eps,_) denotes the epsilon
% symbol. 
% 
% Productions are represented with prod(N,[H|T]) --- that is,
% arguments are the production index N and a list [H|T] where the head
% of the list H is the left-hand-side of the production, and the tail of
% the list T is the right-hand-side of the production. For example,
% production E -> TE' is represented as
% prod(1,[non(e,_),non(t,_),non(eprime,_)]).

prod(1,[non(e,_),non(t,_),non(eprime,_)]). 
prod(2,[non(eprime,_),term(minus,_),non(t,_),non(eprime,_)]).
prod(3,[non(eprime,_),term(eps,_)]).
prod(4,[non(t,_),term(num,_),non(tprime,_)]).
prod(5,[non(tprime,_),term(mul,_),term(num,_),non(tprime,_)]).
prod(6,[non(tprime,_),term(eps,_)]).


% LL(1) Parsing table.
% expand(non(e,_),term(num,_),1) stands for expand nonterminal E by
% production E -> TE' on terminal num.

% YOUR CODE HERE. 
% Complete the LL(1) parsing table for the grammar.

expand(non(e,_),term(num,_),1).
expand(non(eprime,_),term(minus,_),2).
expand(non(eprime,_),term(end,_),3).
expand(non(t,_),term(num,_),4).
expand(non(tprime,_),term(mul,_),5).
expand(non(tprime,_),term(minus,_),6).
expand(non(tprime,_),term(end,_),6).

% sample inputs
input0([3,-,5]).
input1([3,-,5,*,7,-,18]).


% YOUR CODE HERE.
% Write transform(L,R): it takes input list L and transforms it into a
% list where terminals are represented with term(...), as well
% as adds the end-of-input marker. The transformed list is given 
% in unbound variable R.
% E.g., transform([3,-,5],R). 
% R = [term(num,3),term(minus,_),term(num,5),term(end,_)]

transform([],R) :- append([term(end,_)],[],R).
transform([-|Tail],R) :- transform(Tail, S), append([term(minus,_)],S,R).
transform([*|Tail],R) :- transform(Tail, S), append([term(mul,_)],S,R).
transform([A|Tail],R) :- transform(Tail, S), append([term(num,A)],S,R).


% Write parseLL(L,ProdSeq): it takes input list L and produces the
% production sequence applied by the predictive parser
% E.g., input0(L),parseLL(L,ProdSeq).
% ProdSeq = [1, 4, 6, 2, 4, 6, 3].

parseLL([H|T],ProdSeq) :- .

















