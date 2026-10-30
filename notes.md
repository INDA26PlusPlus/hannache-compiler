
States
Starts och Expressions define a language.

BNF - Backus-Naur form

Lexical analysis...
Tokens -> parsing??? parsar alla tokens -> Asd -> semantic analysis, chekcs if its blanced?
-> intermediade representation, here are like types.
if a > b -> a -= 1 else a += 1

hoppa kostar -> loops hoppar, copy paste 5 times = cheaper.

olika assembely per dator.

### Reguljär uttryck:
Bro what is this?
[a-z]+ -> name
0 |

### grammar
bnf typ [a-z]...
Here you plan out your language define stuff. total freedom, everything but [a-z] is up to you i think
But remember: state only stores your pos now and can peek at one step in front of you. 
VAR :== [a-z]
FUN :== [A-Z]
NUM :== [0-9]
<adding stuff> :== VAR "=" "sum" NUM "+" NUM
i can chose anything like "=" can be "tina"
<adding thingies> :== VAR "tina" NUM "+" NUM

INe xample they have:

<statement> ::= <labeled-statement>
              | <expression-statement>
              | <compound-statement>
              | <selection-statement>
              | <iteration-statement>
              | <jump-statement>
and then deinfe everything.

### Lexical analysis
Reguljära uttryck bra
Looks through your grammar and creates tokens
"(" is a token VAR is a token if you have defined it. Everything is based upon the [a-z] like standeran definers

### Abstract Syntax Tree
Strukturen..

EE: 0 [1-9]

The onein parenthesis is further down the tree

Goal:
Fib tal ska kunna lösas
- Ha recursion..
- kan sätta values och göra addition.
- if else statements
- helst ha en print

Grammatik i BNF
lexer och parsing
kan printa ut syntaxträdet.
Dokumentera hur den används.

VAR :== [a-z]


adding values :== "sum" "(" VARIABLE "," VARIABLE ")"

i think the S and E is just logic/grammar

how to go from S to (()())?
S :== E
    (E)
    (E E)
    ((E)(E))
    (( ) ( ))
