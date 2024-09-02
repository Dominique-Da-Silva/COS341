# Requirements 

### Understanding the Lexer:
A lexer (or lexical analyzer) is the first phase of a compiler. Its primary role is to take the raw source code input and break it down into a series of tokens. Tokens are the smallest units of meaning in the language, such as keywords, operators, identifiers, literals, etc.

### Steps to Implement the Lexer:
1. **Token Identification**:
   - You need to identify and define all possible tokens in the language. These tokens are outlined in the specification:
     - **Keywords**: `main`, `begin`, `end`, `num`, `text`, `skip`, `halt`, `print`, `if`, `then`, `else`, `not`, `sqrt`, etc.
     - **Identifiers**: For variable names (Token-Class V) and function names (Token-Class F).
     - **Constants**: Numbers (Token-Class N) and strings (Token-Class T).
     - **Operators**: `=`, `<`, `+`, `-`, `*`, `/`, `or`, `and`, `eq`, `grt`, etc.
     - **Punctuation**: `;`, `,`, `(`, `)`, `{`, `}`.

2. **Regular Expressions**:
   - Use regular expressions to define the patterns for each type of token. These patterns are partially provided in the Appendix:
     - **Variable Names (Token-Class V)**: `V_[a-z]([a-z]|[0-9])*`
     - **Function Names (Token-Class F)**: `F_[a-z]([a-z]|[0-9])*`
     - **Strings (Token-Class T)**: Various patterns for short snippets of text.
     - **Numbers (Token-Class N)**: Various patterns for integers and real numbers.

3. **Lexical Analysis**:
   - Implement a function (or a set of functions) that reads the source code character by character, matches sequences of characters against the regular expressions, and outputs the corresponding tokens.
   - Handle whitespace and line breaks appropriately, as they can help the lexer determine when a token ends.

4. **Error Handling**:
   - Implement error handling to manage unrecognized sequences of characters or illegal tokens.

### How to Go About It in C++:
1. **Define Token Classes**:
   - Create an enum or a set of constants to represent the different token types.

2. **Regular Expression Matching**:
   - Use C++ regex libraries (e.g., `<regex>`) or custom matching logic to identify tokens.

3. **Lexer Function**:
   - Implement a `Lexer` class with a method that takes source code as input and returns a list (or stream) of tokens.

4. **Testing**:
   - Test your lexer with various input programs to ensure it correctly identifies and categorizes each token.

### Summary:
Your task is to build a lexer that can take source code written in the RecSPL 2024 language and produce a sequence of tokens according to the grammar specified in the document. The lexer needs to recognize different types of tokens, including keywords, identifiers, constants, and operators, and handle errors gracefully. 

