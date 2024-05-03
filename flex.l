%{
#include "y.tab.h"
%}

DIGIT       [0-9]
LETTER      [a-zA-Z]
IDENTIFIER  {LETTER}({LETTER}|{DIGIT}|_)*
INTEGER     {DIGIT}+

%%

"launch"            { return LAUNCH; }
"set"               { return SET; }
"increase"          { return INCREASE; }
"decrease"          { return DECREASE; }
"multiply by"       { return MULTIPLY_BY; }
"divide by"         { return DIVIDE_BY; }
"transmit"          { return TRANSMIT; }
"orbit"             { return ORBIT; }
"do"                { return DO; }
"end"               { return END; }
"check"             { return CHECK; }
"then"              { return THEN; }
{INTEGER}           { yylval.integer = atoi(yytext); return INTEGER; }
{IDENTIFIER}        { yylval.str = strdup(yytext); return IDENTIFIER; }
\n                  { return NEWLINE; }
.                   { /* ignore unrecognized characters */ }

%%
