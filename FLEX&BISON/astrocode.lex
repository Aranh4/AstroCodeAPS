%{
#include "astrocode.tab.h"
%}

%option noyywrap
%%
"launch"                { printf("Debug: Returning LAUNCH\n"); return LAUNCH; }
"module"                { printf("Debug: Returning MODULE\n"); return MODULE; }
"set"                   { printf("Debug: Returning SET\n"); return SET; }
"transmit"              { printf("Debug: Returning TRANSMIT\n"); return TRANSMIT; }
"orbit"                 { printf("Debug: Returning ORBIT\n"); return ORBIT; }
"do"                    { printf("Debug: Returning DO\n"); return DO; }
"end"                   { printf("Debug: Returning END\n"); return END; }
"check"                 { printf("Debug: Returning CHECK\n"); return CHECK; }
"else"                  { printf("Debug: Returning ELSE\n"); return ELSE; }
"then"                  { printf("Debug: Returning THEN\n"); return THEN; }
"either"                { printf("Debug: Returning EITHER\n"); return EITHER; }
"also"                  { printf("Debug: Returning ALSO\n"); return ALSO; }
"matches"               { printf("Debug: Returning MATCHES\n"); return MATCHES; }
"exceeds"               { printf("Debug: Returning EXCEEDS\n"); return EXCEEDS; }
"below"                 { printf("Debug: Returning BELOW\n"); return BELOW; }
"increase"              { printf("Debug: Returning INCREASE\n"); return INCREASE; }
"decrease"              { printf("Debug: Returning DECREASE\n"); return DECREASE; }
"multiply by"           { printf("Debug: Returning MULTIPLY_BY\n"); return MULTIPLY_BY; }
"divide by"             { printf("Debug: Returning DIVIDE_BY\n"); return DIVIDE_BY; }
"negate"                { printf("Debug: Returning NEGATE\n"); return NEGATE; }
"positive"              { return POSITIVE;}
"negative"              { return NEGATIVE;}
[a-zA-Z_][a-zA-Z0-9_]*  { printf("Debug: Returning IDENTIFIER '%s'\n", yytext); yylval.str = strdup(yytext); return IDENTIFIER; }
[0-9]+                  { printf("Debug: Returning INTEGER '%s'\n", yytext); yylval.integer = atoi(yytext); return INTEGER; }
\"([^"]|\\.)*\"         { printf("Debug: Returning STRING_LITERAL '%s'\n", yytext); yylval.str = strdup(yytext); return STRING_LITERAL; }

[ \t\r]+                ; // Ignore whitespace
"\n"                    { printf("Debug: Returning NEWLINE\n"); return NEWLINE; }
.                       { printf("Debug: Returning '%c'\n", yytext[0]); return yytext[0]; }
<<EOF>>                 { printf("Debug: Returning END_OF_FILE\n"); return END_OF_FILE; }
%%

