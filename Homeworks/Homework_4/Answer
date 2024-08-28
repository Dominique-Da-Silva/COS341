No.


The Semester Project's context free grammar is not suitable for LL(1) parsing.

In order for a CFG to be suitable for LL(1) parsing, the look ahead sets of the same production rule should be disjoint, such as LA(3) and LA(4) for example.

However, we can clearly see without completing the entire table that:
         LA(19) = FIRST(VNAME) = {V}
                      &
         LA(20) = FIRST(VNAME) = {V}

That is under the assumption given in the specification that VNAME ::= *token from Class V* and given that "Token-Class V for user-defined variable names: V_[a‒z]([a‒z]|[0‒9])*", i.e. variables start with the terminal V_ in order to distinguish them from the reserved keywords.


They are not disjoint sets and therefore the grammar is not in LL(1).




Multiletter Tokens and replacements:

Other tokens: = { } ( ) , ; <

Token	Single Terminal Replacement
main	      m
num	        n
text	      x
begin	      b
end	        z
skip	      s
halt	      h
print	      p
input	      a
if	        i
then	      t
else	      e
not	        o
sqrt	      q
or	        r
and	        w
eq	        k
grt	        g
add	        l
sub	        c
mul	        u
div	        d
void	      v

#	Grammar Production Rule (Adapted)	                    Look Ahead
0	PROG ::= m GLOBVARS ALGO FUNCTIONS	                  LA(0) = FIRST(m) = {m}
1	GLOBVARS ::= //nullable	                              LA(1) = FOLLOW(GLOBVARS) = {b}
2	GLOBVARS :: VTYPE VNAME , GLOBVARS	                  LA(2) = FIRST(VTYPE) = {n , x}
3	VTYP ::=  n	                                          LA(3) = FIRST(n) = {n}
4	VTYP ::= x	                                          LA(4) = FIRST(x) = {x}
5	VNAME ::= *token from Class V*	                      LA(5) = FIRST(V_[a‒z]([a‒z]|[0‒9])*) = {V}
6	ALGO ::= b INSTRUC  z	                                LA(6) = FIRST(b) = {b}
7	INSTRUC ::= //nullable	                              LA(7) = FOLLOW(INTRUC) = {z}
8	INSTRUC ::= COMMAND ; INSTRUC	                        LA(8) = FIRST(COMMAND) = {}
9	COMMAND ::= s	                                        LA(9) = FIRST(s) = {s}
10	COMMAND ::= h	                                      LA(10) = FIRST(h) = {h}
11	COMMAND ::= p ATOMIC	                              LA(11) = FIRST(p) = {p}
12	COMMAND ::= ASSIGN	 
13	COMMAND ::= CALL	 
14	COMMAND ::= BRANCH	                                LA(14) = FIRST(BRANCH) = {i}
15	ATOMIC ::= VNAME	 
16	ATOMIC ::= CONST	 
17	CONST ::= *token from Class N*	 
18	CONST ::= *token from Class T*	 
19	ASSIGN ::= VNAME < a	                              LA(19) = FIRST(VNAME) = {V}
20	ASSIGN ::= VNAME = TERM	                            LA(20) = FIRST(VNAME) = {V}
21	CALL ::= FNAME(ATOMIC,ATOMIC,ATOMIC)	 
22	BRANCH ::= i COND t ALGO e ALGO	                    LA(21) = FIRST(i) = {i}
23	TERM ::= ATOMIC	 
24	TERM ::= CALL	 
25	TERM ::= OP	                                        LA(25) = FIRST(OP) = {o,q,r,w,k,g,l,c,u,d}
26	OP ::= UNOP (ARG)	                                  LA(26) = FIRST(UNOP) = {o,q}
27	OP ::= BINOP (ARG , ARG)	                          LA(27) = FIRST(BINOP) = {r,w,k,g,l,c,u,d}
28	ARG ::= ATOMIC	 
29	ARG ::= OP	                                        LA(29) = FIRST(OP) = {o,q,r,w,k,g,l,c,u,d}
30	COND ::= SIMPLE	 
31	COND ::= COMPOSIT	 
32	SIMPLE ::= BINOP (ATOMIC , ATOMIC)	                LA(32) = FIRST(BINOP) = {r,w,k,g,l,c,u,d}
33	COMPOSIT ::= BINOP (SIMPLE , SIMPLE)	              LA(33) = FIRST(BINOP) = {r,w,k,g,l,c,u,d}
34	COMPOSIT ::= UNOP (SIMPLE)	                        LA(34) = FIRST(UNOP) = {o,q}
35	UNOP ::= o	                                        LA(35) = FIRST(o) = {o}
36	UNOP ::= q	                                        LA(36) = FIRST(q) = {q}
37	BINOP ::= r	                                        LA(37) = FIRST(r) = {r}
38	BINOP ::= w	                                        LA(38) = FIRST(w) = {w}
39	BINOP ::= k	                                        LA(39) = FIRST(k) = {k}
40	BINOP ::= g	                                        LA(40) = FIRST(g) = {g}
41	BINOP ::= l	                                        LA(41) = FIRST(l) = {l}
42	BINOP ::= c	                                        LA(42) = FIRST(c) = {c}
43	BINOP ::= u	                                        LA(43) = FIRST(u) = {u}
44	BINOP ::= d	                                        LA(44) = FIRST(d) = {d}
45	FNAME ::= *token from Class F*	 
46	FUNCTIONS ::= //nullable	                          LA(46) = FOLLOW(FUNCTIONS) = {}
47	FUNCTIONS ::= DECL FUNCTIONS	                      LA(47) = FIRST(DECL) = {n,v}
48	DECL ::= HEADER BODY	                              LA(48) = FIRST(HEADER) = {n,v}
49	HEADER ::= FTYP FNAME (VNAME , VNAME , VNAME )	    LA(49) = FIRST(FTYP) = {n, v}
50	FTYP ::= n	                                        LA(50) = FIRST(n) = {n}
51	FTYP ::= v	                                        LA(51) = FIRST(v) = {v}
52	BODY ::= PROLOG LOCVARS ALGO EPILOG SUBFUNCS z	    LA(52) = FIRST(PROLOG) = {{}
53	PROLOG ::= { 	                                      LA(53) = FIRST({) = {{}
54	EPILOG ::= }	                                      LA(54) = FIRST(}) = {}}
55	LOCVARS ::= VTYP VNAME , VTYP VNAME , VTYP VNAME ,	LA(55) = FIRST(VTYP) = {n,x}
56	SUBFUNCS ::= FUNCTIONS	                            LA(56) = FIRST(FUNCTIONS) = {}


Response Feedback:	
Correct 😀 ! Additional advice for the implementation of your semester project: You may decide for yourself whether you would like to try to "transform" the given grammar (without guarantee for certain success) into a new form that is suitable for LL(1), or whether you would like to implement a non-LL(1) parser from the very beginning.
