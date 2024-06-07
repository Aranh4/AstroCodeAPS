%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
extern int yylex();
void yyerror(const char *s);
%}

%union {
    char* str;
    int integer;
}

%token <integer> INTEGER  
%token <str> IDENTIFIER STRING_LITERAL
%token LAUNCH MODULE SET TRANSMIT ORBIT DO END CHECK THEN EITHER ALSO MATCHES EXCEEDS BELOW INCREASE DECREASE NEGATE MULTIPLY_BY DIVIDE_BY NEWLINE END_OF_FILE ELSE POSITIVE NEGATIVE
%type <integer> BOOL_EXP REL_EXP EXP TERM FACTOR BOOL_TERM integer
%type <str> PROGRAM BLOCK STATEMENT MODULE_DECLARATION ASSIGNMENT TRANSMIT_PRINT ORBIT_WHILE CHECK_IF 

%%

PROGRAM:
    LAUNCH NEWLINE BLOCK END_OF_FILE
    { printf("PROGRAM parsed successfully.\n"); return 0; }
    ;

BLOCK:
   // Simplified to avoid using strdup
  | BLOCK STATEMENT
  | BLOCK STATEMENT NEWLINE
    ;

STATEMENT:
    MODULE_DECLARATION NEWLINE
  | ASSIGNMENT NEWLINE
  | TRANSMIT_PRINT NEWLINE
  | ORBIT_WHILE NEWLINE
  | CHECK_IF NEWLINE
    ;

MODULE_DECLARATION:
    MODULE IDENTIFIER 
  | MODULE IDENTIFIER SET BOOL_EXP 
    ;

ASSIGNMENT:
    IDENTIFIER SET BOOL_EXP 
    ;

TRANSMIT_PRINT:
    TRANSMIT '(' BOOL_EXP ')' 
    ;

ORBIT_WHILE:
    ORBIT BOOL_EXP DO NEWLINE BLOCK END 
    ;

CHECK_IF:
    CHECK BOOL_EXP THEN NEWLINE BLOCK END 
  | CHECK BOOL_EXP THEN NEWLINE BLOCK ELSE NEWLINE BLOCK END 

BOOL_EXP:
    BOOL_TERM
  | BOOL_EXP EITHER BOOL_TERM 
    ;

BOOL_TERM:
    REL_EXP
  | BOOL_TERM ALSO REL_EXP 
    ;

REL_EXP:
    EXP
  | REL_EXP MATCHES EXP 
  | REL_EXP EXCEEDS EXP 
  | REL_EXP BELOW EXP 
    ;

EXP:
    TERM
  | EXP INCREASE TERM 
  | EXP DECREASE TERM 
    ;

TERM:
    FACTOR
  | TERM MULTIPLY_BY FACTOR 
  | TERM DIVIDE_BY FACTOR 
    ;

FACTOR:
    integer 
  | IDENTIFIER 
  | '(' BOOL_EXP ')' 
  | POSITIVE FACTOR 
  | NEGATIVE FACTOR 
  | NEGATE FACTOR 
  | STRING_LITERAL 
  ;

integer:
    INTEGER 
    ;

%%
void yyerror(const char *s) {
    fprintf(stderr, "Erro sintático: %s\n", s);
}

int main() {
    int result = yyparse();
    if (result == 0) {
        printf("Parsing completed successfully.\n");
        return 0;
    } else {
        printf("Parsing failed.\n");
        printf("Error code: %d\n", result);
        return 1;
    }
}
