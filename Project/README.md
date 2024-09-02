# Compiler-Construction-Project

The bug is that the non-void functions were not given their necessary return statement. (Void-functions obviously do not need any such return statement.)

The bugfix is as follows: Into the project grammar you simply insert this one additional production rule:

COMMAND ::= return ATOMIC

Thereby, return is now a new terminal token (in fact a reserved keyword) for which your Lexer must also be prepared and adjusted.

This simple bugfix allows us now to write a return-statement into the final line of the ALGO of a non-void function :)

Comment: Obviously this simple bugfix now also allows us to write the most silly return statements everywhere into an ALGO - even in the middle of the main program where does not make any sense at all - but we can still deal with this semantic problem in the semantic analysis phase of the compiler after the parser has produces a syntax tree.
"Normally" a function without return - or a return in the middle of main - would (should) be regarded as a syntax problem to be picked up already by the parser; but to follow that route I would be forced to completely rewrite the project grammar on which students have already started working; that would not be good. Therefore we will deal with wrongly placed return-commands as "semantic" problems in the semantic analysis phases after the parsing.