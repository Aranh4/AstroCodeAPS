# AstroCodeAPS
EBNF:

PROGRAM = "launch", "\n", BLOCK ;

BLOCK = { STATEMENT } ;

STATEMENT = ( MODULE_DECLARATION | ASSIGNMENT | TRANSMIT_PRINT | ORBIT_WHILE | CHECK_IF ), "\n" ;

<<<<<<< HEAD
MODULE_DECLARATION = "module", IDENTIFIER, ["set", EXP] ;

ASSIGNMENT = IDENTIFIER, "set", EXP ;

EXP = BOOL_TERM, { ("either"), BOOL_TERM } ;
=======
MODULE_DECLARATION = "module", IDENTIFIER, ["set", BOOL_EXP] ;

ASSIGNMENT = IDENTIFIER, "set", BOOL_EXP ;

BOOL_EXP = BOOL_TERM,{("either"),BOOL_TERM};

BOOL_TERM = REL_EXP,{("also"), REL_EXP};

REL_EXP = EXP,{("matches"|"exceeds"|"below"),EXP}

EXP = TERM, { ("increase" | "decrease","join with"), TERM } ;
>>>>>>> 411ae5f39e769b301a9bec39083e62a404845bf0

BOOL_TERM = REL_EXPRESSION, { ("also"), REL_EXPRESSION } ;

<<<<<<< HEAD
REL_EXPRESSION = TERM, { ("exceeds" | "below" | "matches"), TERM } ;

TERM = FACTOR, { ("increase" | "decrease"), FACTOR } ;

FACTOR = UNARY_OP | INTEGER | IDENTIFIER | "(" , EXP , ")" | UNARY_OP, FACTOR ;

TRANSMIT_PRINT = "transmit", "(", EXP, ")" ;
=======
FACTOR = INTEGER | IDENTIFIER | "(" , BOOL_EXP , ")" | UNARY_OP, FACTOR ;

TRANSMIT_PRINT = "transmit", "(", BOOL_EXP, ")" ;

ORBIT_WHILE = "orbit", BOOL_EXP, "do", "\n", { STATEMENT }, "end" ;

CHECK_IF = "check", BOOL_EXP, "then", "\n", { STATEMENT }, "end" ;
>>>>>>> 411ae5f39e769b301a9bec39083e62a404845bf0

ORBIT_WHILE = "orbit", EXP, "do", "\n", BLOCK, "end" ;

<<<<<<< HEAD
CHECK_IF = "check", EXP, "then", "\n", BLOCK, "end" ;
=======
>>>>>>> 411ae5f39e769b301a9bec39083e62a404845bf0

UNARY_OP = "negate" | "-" ;

INTEGER = DIGIT, { DIGIT } ;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;

<<<<<<< HEAD
=======
UNARY_OP = "negative" | "positive" | "negate"  ;

>>>>>>> 411ae5f39e769b301a9bec39083e62a404845bf0
DIGIT = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

LETTER = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" ;


DIAGRAMA:
<img src='diagrama.jpg'>
