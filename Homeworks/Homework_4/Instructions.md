# Question 1
	
Take the context-free grammar from our Semester Project. Simplify its representation (however not its structure!) in the following manner:

Replace every terminal multi-letter-token (that comes from the Lexer) by one single terminal character; for example:

you could replace the multi-letter-token if by the single letter terminal x
you could replace the multi-letter-token else by the single terminal letter y
etc..., as you wish.
As a result of this textual simplification, the "style" of the grammar now looks much more similar to all those familiar grammars which you typically find in the theory books, with their typical terminal symbols a, b, c, etc.

After this preparation, you shall now analyse whether the Semester Project's context-free grammar is suitable for LL(1) parsing?

IF "yes", then demonstrate [in the answer box provided below] that there are no overlapping Look-ahead Sets for those production rules that have the same Non-terminal symbol on their left-hand-sides!
IF "no", then demonstrate [in the answer box provided below] that there are overlapping Look-ahead Sets for at least two production rules that have the same Non-terminal symbol on their left-hand-sides!
For clarification: if grammar G contains some production rule X→α  (with α ∈A*), then such a rule's Look-ahead set is = FIRST(α)
