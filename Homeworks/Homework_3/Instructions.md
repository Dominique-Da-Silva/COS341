# Question 1

Create and write your own context-free grammar, G, such that its language L(G) is the infinitely large set of all the words { anbncmdm }, whereby xi has the meaning that the token x is repeated i times, and whereby n>0 as well as also m>0.

For example: the word aaabbbccdd is in L(G) whereby, in this example, n=3 and m=2.
Let S be the start symbol of your context-free grammar G.

Attention: Please make sure that your own grammar here in sub-question a) G is neither in Chomsky Normal Form (CNF), nor in Greibach Normal Form (GNF), because we want to deal with CNF and GNF only later in sub-questions d) and e) of this homework.
Write your grammar G into the answer-box provided below:

# Question 2

Create and write another context-free grammar, G', such that its language L(G' ) is the infinitely large set of all the words { anbmcmdn }, whereby (again) xi has the meaning that the token x is repeated i times, and whereby (again) n>0 as well as also m>0.

For example: the word abbccd is in L(G' ) whereby, in this example, n=1 and m=2.
Let S' be the start symbol of your new context-free grammar G' .

Attention: Please make sure that your own grammar G' here in sub-question b) is neither in Chomsky Normal Form (CNF), nor in Greibach Normal Form (GNF), because we want to deal with CNF and GNF only later in sub-questions d) and e) of this homework.
Write your new grammar G' into the answer-box provided below:

# Question 3

On the basis of your two grammars G and G' from sub-questions a) and b) let us define a new union-language L(G'' ) := L(G) U L(G' ) whereby the union-grammar G'' is defined as follows:

All the rules of your grammar G from sub-question a) are included in G''
All the rules of your grammar G' from sub-question b) are included in G'', too
G'' has the start symbol S''
G'' has a new rule S'' ==> S, where S was the start symbol of your grammar G from sub-question a)
G'' also has a new rule S'' ==> S', where S' was the start symbol of your grammar G' from sub-question b)
Demonstrate that the new grammar G'' is ambiguous by showing that the simple example string abcd, which is included in the union-language L(G'' ), has two structurally different syntax trees under S'' 

Draw the pictures of those two different syntax trees onto one sheet of paper, make a digital photography your sheet of paper, and upload the photo file via the upload facility provided below:

# Question 4

Use the online tool https://mahshidhp.pythonanywhere.com/ to automatically transform the union-grammar G'' from sub-question c) into its Chomsky Normal Form, CNF(G'' ).

Demonstrate that the transformed CNF grammar (which you get as output from the online tool) is still ambigious, by showing (again) that the simple example string abcd has (again) two structurally different syntax trees under the start symbol of the transformed CNF-grammar.

In other words: the transformation of G'' into its Chomsky Normal Form did not eliminate the ambiguity!

Again: draw the pictures of those two syntax trees onto a sheet of paper, make a digital photography of the paper, and upload the photo file via tha upload facility provided below:

# Question 5

Use (again) the online tool https://mahshidhp.pythonanywhere.com/ to automatically transform the union-grammar G'' from sub-question c) into its Greibach Normal Form, GNF(G'' ).

Demonstrate that the transformed GNF grammar (which you get as output from the online tool) is still ambigious, by showing (again) that the simple example string abcd has (again) two structurally different syntax trees under the start symbol of the transformed GNF-grammar.

In other words: also the transformation of G'' into its Greibach Normal Form did not eliminate the ambiguity!

Again: draw the pictures of those two syntax trees onto a sheet of paper, make a digital photography of the paper, and upload the photo file via tha upload facility provided below:
