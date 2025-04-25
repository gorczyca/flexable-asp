#program base.
propMT(pb1;pb2;pf1;pf2). % proponent's move types
rMT(pb1;pb2;pf1;ob1;ob2;of1). % rule move types
branchMT(pb1;pb2;pf2). % branching (br.) move types
plr(p;o). % players; proponent (p) and opponent (o)
rS(R,S) :- h(R,S) ; b(R, S). % rule's statements
stS(0,S,p) :- goal(S). % proponent's initial statement 
remBloR(0,R,H,p) :- h(R,H), rS(R,S1), rS(R,S2), ctr(S1,S2). % blocked, inconsistent rules
#program updateState(t).
stS(t,S,o) :- stS(_,S,p). % allow the opponent to access proponent statements
stR(t,R,H,o) :- stR(_,R,H,p).  % allow the opponent to access proponent rules
def(t,D) :- stS(_,D,p), a(D). % defence
cul(t,C) :- stS(_,S,p), ctr(C,S). % culprit
culCtr(t,CC) :- cul(_,C), ctr(C,CC). % culprit contrary
defCtr(t,DC) :- def(_,D), ctr(D,DC). % defence contrary
remR(t,R,H,o) :- not stR(_,R,o), h(R,H). % remaining opponent's rule 
remR(t,R1,H,p) :- h(R1,H), not stR(_,R2,H,p). % remaining proponent's rule
remBloR(t,R,H,P) :- remR(t,R,H,P), b(R,B), cul(_,B), plr(P). % blocked remaining player P's rule                
remBloR(t,R,H,p) :- remR(t,R,H,p), rS(R,S), defCtr(_,S). % block remaining proponent's rule                                                                                
unexpS(t,S,p) :- stS(_,S,p), not stR(t,R,p), h(R,S). % unexpanded statement
stExpS(t,S,o) :- stS(_,S,o), remBloR(t,R,S,o) : remR(t,R,S,o). % fully expanded statement 
stBloS(t,S,p) :- stS(_,S,p), cul(_,S). % state blocked statement
stBloS(t,S,p) :- stExpS(t,S,p), stBloR(t,R,S,p) : stR(t,R,S,p).
stBloR(t,R,H,p) :- stR(t,R,p), h(R,H), b(R,B), stBloS(t,B, _). % state blocked rule
comS(t,S,P) :- stS(t,S,P), a(S).  % complete statement
comS(t,H,P) :- stR(t,R,H,P), comS(t,S,P) : b(R, S).
unbloComS(t,S,p) :- stS(t,S,p), a(S), not cul(t,S). % unblocked complete (com.) statement
unbloComS(t,S,p) :- stS(t,S,p), not stBloS(t,S,p), unbloComR(t,_, S,p).
unbloComR(t,R,H,p) :-  stR(t,R, _,p), not stBloR(t,R, _,p), unbloComS(t,B,p) : b(R, B). % unblocked com. rule
unbloSupSS(t,S,p) :- stS(t,S,p), ctr(D, S), def(t,D), not stBloS(t,S,p). % unblocked statement supporting S 
unbloSupSS(t,S,p) :- stS(t,S,p), not stBloS(t,S,p), unbloSupSR(t,R, _,p), b(R, S).
unbloSupSR(t,R,H,p) :- stR(t,R,H,p), not stBloR(t,R,H,p), unbloSupSS(t,H,p). % unblocked rules supporting S
culCan(t,C) :- a(C), unbloSupSS(t,C,p). % culprit candidate
pm(t,p,pb1,R) :- remR(t,R,H,p), not remBloR(t,R,H,p), unexpS(t,H,p). % possible move "PB1"
pm(t,p,pb2,R) :- remR(t,R,H,p), not remBloR(t,R,H,p), culCan(t,C), ctr(C, H), not stS(t,H,p),                  not ctr(D, H) : def(t,D). % possible move "PB2"
pm(t,p,pf1,R) :- remR(t,R,H,p), not remBloR(t,R,H,p), comS(t,B,p) : b(R, B). % possible move "PF1"
pm(t,p,pf2,A) :- culCan(t,C), ctr(C,A), a(A), not stS(t,A,p), not ctr(A,A), not cul(t,A),                      not ctr(D,A) : def(t,D). % possible move "PF2"
pm(t,o,ob1,R) :- remR(t,R,H,o), not remBloR(t,R,H,o), unbloSupSS(t,H,o). % possible move "OB1"
pm(t,o,ob2,R) :- remR(t,R,H,o), not remBloR(t,R,H,o), ctr(D, H), def(t,D). % possible move "OB2"
pm(t,o,of1,R) :- remR(t,R,H,o), not remBloR(t,R,H,o), unbloComS(t,B,o) : b(R, B). % possible move "OF1"
pm(t,o,of2,A) :- ctr(D,A), def(t,D), a(A), not stS(t,A,o). % possible move "OF2"
stS(t,S,P) :- m(_,T,R), rMT(T), propMT(T), rS(R,S), plr(P). % new state statement
stS(t,A,P) :- m(_,T,A), not rMT(T), propMT(T), plr(P).
stS(t,S,p) :- m(_,T,R), rMT(T), not propMT(T), rS(R, S).
stS(t,A,p) :- m(_,T,A), not rMT(T), not propMT(T).
stR(t,R,H,P) :- m(_,T,R), h(R,H), rMT(T), propMT(T), plr(P). % new state rule
stR(t,R,H,p) :- m(_,T,R), h(R,H), rMT(T), not propMT(T). 
term(t) :-  g(G), comS(t,G,p), comS(t,CC,p) : culCtr(t,CC), not unbloComS(t,DC,p) : defCtr(t,DC). % termination condition
end(t,p) :- term(t), not pm(t,o,_,_). % proponent won; termination condition satisfied and opponent cannot move
end(t,o) :- not term(t), not pm(t,p,_,_). % opponent won; term. cond. not satisfied and proponent cannot move
#program step(t).
m(t,T, X) :- pm(t-1, T, X), not branchMT(T), t > 0. % proceed with non-br. move type
{ m(t,T, X) : pm(t-1, T, X),  branchMT(T)  } = 1 :- branchMT(T) : pm(t-1, T, _), t > 0. % choose one br. move