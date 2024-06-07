# AstroCode - APSLogComp

AstroCode é uma linguagem de programação desenvolvida para simplificar a criação de programas através de uma sintaxe intuitiva e estruturas claras. Inspirada por conceitos de engenharia espacial e missões astronauticas, esta linguagem visa facilitar o aprendizado de programação e a implementação de algoritmos básicos de controle e decisão em contextos espaciais. AstroCodeAPS é ideal para iniciantes e para aqueles que desejam uma abordagem mais visual e estruturada na codificação, especialmente em simulações e operações espaciais.

### Motivação

A criação de AstroCodeAPS foi motivada pela necessidade de uma linguagem que combinasse simplicidade e funcionalidade, especialmente voltada para contextos de engenharia espacial e missões de astronautas. A linguagem utiliza terminologias e estruturas familiares ao ambiente espacial, tornando o processo de aprendizagem mais contextualizado e relevante para profissionais e entusiastas da área. Com AstroCodeAPS, é possível simular algoritmos de controle de naves, monitoramento de condições e decisões críticas de maneira intuitiva e acessível.

### EBNF:

``` ebnf
PROGRAM = "launch", "\n", BLOCK ;

BLOCK = { STATEMENT } ;

STATEMENT = ( MODULE_DECLARATION | ASSIGNMENT | TRANSMIT_PRINT | ORBIT_WHILE | CHECK_IF ), "\n" ;

MODULE_DECLARATION = "module", IDENTIFIER, ["set", BOOL_EXP] ;

ASSIGNMENT = IDENTIFIER, "set", BOOL_EXP ;

BOOL_EXP = BOOL_TERM, { "either", BOOL_TERM } ;

BOOL_TERM = REL_EXP, { "also", REL_EXP } ;

REL_EXP = EXP, { ("matches" | "exceeds" | "below"), EXP } ;

EXP = TERM, { ("increase" | "decrease"), TERM } ;

FACTOR = INTEGER | IDENTIFIER | "(", BOOL_EXP, ")" | UNARY_OP, FACTOR ;

TRANSMIT_PRINT = "transmit", "(", BOOL_EXP, ")" ;

ORBIT_WHILE = "orbit", BOOL_EXP, "do", "\n", { STATEMENT }, "end" ;

CHECK_IF = "check", BOOL_EXP, "then", "\n", { STATEMENT }, "end" ;

UNARY_OP = "negative" | "positive" | "negate" ;

INTEGER = DIGIT, { DIGIT } ;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;

DIGIT = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

LETTER = "A...Z" | "a...z" ;

```

Diagrama
Abaixo está o diagrama da estrutura da linguagem AstroCodeAPS:

<img src='diagrama.jpg'>
