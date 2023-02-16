# flexable-asp

### Standard version, with specifying the max number of moves.

Run with: 

`clingo encoding.lp <INSTANCE> --const maxMove=<MAX NUMBER OF MOVES> --const goal=<GOAL>`

e.g.

`clingo encoding.lp ./instances/th_ex.lp --const maxMove=15 --const goal=p 1`

Output:
```
Reading from encoding.lp ...
Solving...
Answer: 1
move(1,"PB1",p1) move(2,"OB2",xa1) move(3,"OB1",v2) move(4,"PB2",xe1) move(5,"PF1",r1) move(6,"OB2",xa2) move(7,"PF1",q1) move(8,"PF1",xf1)
SATISFIABLE

Models       : 1+
Calls        : 1
Time         : 0.061s (Solving: 0.02s 1st Model: 0.02s Unsat: 0.00s)
CPU Time     : 0.061s
```

### Iterative version

`clingo ./incremental/encodingInc.lp ./instances/th_ex.lp  --const goal=p 1`

Output:
```
clingo version 5.6.2
Reading from ./incremental/encodingInc.lp ...
./incremental/encodingInc.lp:97:78-113: info: atom does not occur in any rule head:
  notPossibleForwardRule(t,RId,"P")

./incremental/encodingInc.lp:105:83-104: info: atom does not occur in any rule head:
  defenceContrary(t,H)

./incremental/encodingInc.lp:126:19-34: info: atom does not occur in any rule head:
  taCondition1(t)

./incremental/encodingInc.lp:131:29-54: info: atom does not occur in any rule head:
  possibleMove(0,"OB1",#Anon0)

./incremental/encodingInc.lp:137:30-55: info: atom does not occur in any rule head:
  possibleMove(0,"PB2",#Anon0)

./incremental/encodingInc.lp:138:30-55: info: atom does not occur in any rule head:
  possibleMove(0,"PF2",#Anon0)

./incremental/encodingInc.lp:259:73-104: info: atom does not occur in any rule head:
  playedBlockedStatement(#X0,#X1,#P2)

./incremental/encodingInc.lp:412:1-14: info: no atoms over signature occur in program:
  move/3

Solving...
Solving...
Solving...
Solving...
Solving...
Solving...
Solving...
Answer: 1
move(1,"PF1",p1) move(2,"PB1",q1) move(3,"PB1",xe1) move(4,"PB1",r1) move(5,"OB2",xa2) move(6,"PF1",xf1)
SATISFIABLE

Models       : 1+
Calls        : 7
Time         : 0.039s (Solving: 0.01s 1st Model: 0.00s Unsat: 0.01s)
CPU Time     : 0.039s
```

