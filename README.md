# AstroCodeAPS
EBNF:


PROGRAM = "launch","\n", BLOCK ;

BLOCK = { STATEMENT } ;

STATEMENT = ( MODULE_DECLARATION | ASSIGNMENT | TRANSMIT_PRINT | ORBIT_WHILE | CHECK_IF ), "\n" ;

MODULE_DECLARATION = "module", IDENTIFIER, ["set", SPACE_EXP] ;

ASSIGNMENT = IDENTIFIER, "set", SPACE_EXP ;

SPACE_EXP = EXP ;

EXP = TERM, { ("increase" | "decrease"), TERM } ;

TERM = FACTOR, { ("multiply by" | "divide by"), FACTOR } ;

FACTOR = INTEGER | IDENTIFIER | "(" , EXP , ")" | UNARY_OP, FACTOR ;

TRANSMIT_PRINT = "transmit", "(", SPACE_EXP, ")" ;

ORBIT_WHILE = "orbit", SPACE_EXP, "do", "\n", { STATEMENT }, "end" ;

CHECK_IF = "check", SPACE_EXP, "then", "\n", { STATEMENT }, "end" ;

TYPE = "int" | "string" | "coordinates" | "velocity" ;

LOGIC_OP = "also" | "either" | "negate" ;

COMPARE_OP = "exceeds" | "below" | "matches" ;

INTEGER = DIGIT, { DIGIT } ;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;

UNARY_OP = "negate" | "-" ;

DIGIT = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

LETTER = "A..Z" | "a..z" ;


DIAGRAMA:
<img src='diagrama.jpg'>
