%{
#include <stdio.h>
#include <stdlib.h>

extern int yylex();
void yyerror(const char *s) {
  fprintf(stderr, "Error: %s\n", s);
}

%}

%union {
  int integer;
  char *str;
}

%token <str> IDENTIFIER
%token <integer> INTEGER
%token LAUNCH SET INCREASE DECREASE MULTIPLY_BY DIVIDE_BY TRANSMIT ORBIT DO END CHECK THEN NEWLINE
%type <str> SPACE_EXP EXP TERM FACTOR

%%

program:
    LAUNCH NEWLINE block
    ;

block:
    | block statement
    ;

statement:
    MODULE_DECLARATION NEWLINE
  | ASSIGNMENT NEWLINE
  | TRANSMIT_PRINT NEWLINE
  | ORBIT_WHILE NEWLINE
  | CHECK_IF NEWLINE
  ;

MODULE_DECLARATION:
    "module" IDENTIFIER { printf("Module declaration: %s\n", $2); }
  | "module" IDENTIFIER "set" SPACE_EXP { printf("Module declaration with initialization: %s = %s\n", $2, $4); }
  ;

ASSIGNMENT:
    IDENTIFIER "set" SPACE_EXP { printf("Assignment: %s = %s\n", $1, $3); }
  ;

SPACE_EXP:
    EXP
  ;

EXP:
    TERM { $$ = $1; }
  | EXP INCREASE TERM { printf("Increase: %s + %s\n", $1, $3); }
  | EXP DECREASE TERM { printf("Decrease: %s - %s\n", $1, $3); }
  ;

TERM:
    FACTOR { $$ = $1; }
  | TERM MULTIPLY_BY FACTOR { printf("Multiply: %s * %s\n", $1, $3); }
  | TERM DIVIDE_BY FACTOR { printf("Divide: %s / %s\n", $1, $3); }
  ;

FACTOR:
    INTEGER
  | IDENTIFIER
  | '(' EXP ')' { $$ = $2; }
  ;

TRANSMIT_PRINT:
    "transmit" '(' SPACE_EXP ')' { printf("Print: %s\n", $3); }
  ;

ORBIT_WHILE:
    "orbit" SPACE_EXP "do" NEWLINE block "end" { printf("While loop on %s\n", $2); }
  ;

CHECK_IF:
    "check" SPACE_EXP "then" NEWLINE block "end" { printf("If condition %s\n", $2); }
  ;

%%

int main() {
    return yyparse();
}
