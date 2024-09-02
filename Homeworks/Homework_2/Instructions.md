# Question 1

Does a Lexer have any chance of dis-entangling Carl Clumsy's mess with a strictly "First Match" strategy of re-setting the DFA?

If "yes", then briefly explain: how?
If "no", then briefly explain: why not?

# Question 2

Does a Lexer have any chance of dis-entangling Carl Clumsy's mess with a strictly "Longest Match" strategy of re-setting the DFA?

If "yes", then briefly explain: how?
If "no", then briefly explain: why not?

# Question 3

Does a Lexer have any chance of dis-entangling Carl Clumsy's mess with a combined (mixed) "First or Longest Match" strategy of re-setting the DFA, whereby the case-based decition between "First" or "Longest" is governed by additional program code in the Lexer's software?

If "no", then briefly explain: why not?
If "yes", then outline (as an informal sketch) the additional governing rules in the form: IF the DFA is in such-and-such an Accept-State AND there are such-and-such additional circumstances THEN create the token and re-set the DFA to its start state; OTHERWISE continue lexing.

# Question 4

Would the Lexer have had a better chance of correctly tokenizing Car Clumsy's input with a "Mixed Strategy" if Carl Clumsy had provided some helpful blank spaces within the input stream, such as:

if  a==0  then  elsen=2  else n=3

If "no", then briefly explain: why not?
If "yes", then outline (as an informal sketch) the additional governing rules in the form: IF the DFA is in such-and-such an Accept-State AND there are such-and-such additional circumstances THEN create the token and re-set the DFA to its start state; OTHERWISE continue lexing, whereby the occurrence of blank spaces can be taken into account in those "additional circumstances".
