# PropositionSolver
These are two projects I made in Python. One detects if a logical proposition is a tautology and the other one parses logical propositions.

## Tautology Detector
> Use the Parser.py file to use the program.

The Tautology Detector detects tautologies using a truth table-like approach. Besides printing the result it also prints its deduction process.

**Examples:**
```
Enter proposition: p & (p <=> q)
1/4
p = False
q = False

False & ( False <=> False )
False <=> False
True
False & True
False
It is not a tautology
```
```
Enter proposition: (p => q) | (q => p)
1/4
p = False
q = False

( False => False ) | ( False => False )
False => False
True
True | ( False => False )
False => False
True
True | True
True

2/4
p = False
q = True

( False => True ) | ( True => False )
False => True 
True
True | ( True => False )
True => False
False
True | False
True

3/4
p = True
q = False

( True => False ) | ( False => True )
True => False
False
False | ( False => True )
False => True
True
False | True
True 

4/4
p = True
q = True

( True => True ) | ( True => True )
True => True
True
True | ( True => True )
True => True
True
True | True
True

It is a tautology
```

## Proposition Parser
> Use the Parser.py file to use the program.

The Proposition Parser, as the name suggests, parses propositions. It uses a slightly modified version of the Lexer used in the Tautology Detector. As output, it prints the proposition with parentheses to indicate the seperate nodes in the parse tree. The printed object is a Node object which can have at most two children, which are both Node objects.

**Examples:**
```
Enter logical proposition: a => a & b => b
((a => (a & b)) => b)
```
```
Enter logical proposition: ~a & (b => c) | d
((~a & (b => c)) | d)
```