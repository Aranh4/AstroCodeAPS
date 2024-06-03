from abc import abstractmethod
import sys

class linecounter:
    def __init__(self):
        self.linha= 1

    def increment(self):
        self.linha += 1

    def get(self):
        return str(self.linha)
    

linha = linecounter()


class SymbolTable:
    def __init__(self):
        self.symbols = {}
    
    def set(self, symbol, value, type):
        if symbol in self.symbols.keys():
            self.symbols[symbol] = [value, type]
        else:
            sys.stderr.write("linha:"+ linha.get()+ ": Variavel nao declarada\n")

    def create(self, symbol):   
        if symbol not in self.symbols.keys():     
            self.symbols[symbol] = None
        else:
            sys.stderr.write("linha:"+ linha.get()+ ": Variavel ja declarada\n")
    
    def get(self, symbol):
        return self.symbols[symbol]

class PrePro:
    @staticmethod
    def filter(code):
        res = code
        for i in range(len(code)):
            if i < len(code) and code[i] =='-':     # rest of the code
                if code[i+1] == '-':
                    for j in range(i, len(code)):
                        if code[j] == '\n':
                            code = code[:i] + code[j:]
                            break
        return code
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source, position=0, next=None):
        self.source = source
        self.position = position
        self.next = next
        self.keywords = [
            "launch", "module", "set", "transmit", "orbit", "do", "end",
            "check", "then", "increase", "decrease", "multiply by", "divide by",
            "negate", "also", "either", "exceeds", "below", "matches"
        ]

    def selectNext(self):
        if self.position >= len(self.source):
            self.next = Token("EOF", "")
        else:
            if self.source[self.position] in [" ", "\t"]:
                self.position += 1
                self.selectNext()
            elif self.source[self.position] == "\n":
                self.position += 1
                self.next = Token("NEWLINE", "\n")
                linha.increment()
            elif self.source[self.position].isdigit():
                start = self.position
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    self.position += 1
                self.next = Token("INT", self.source[start:self.position])
            elif self.source[self.position:self.position + 10] == "multiply by":
                self.position += 10
                self.next = Token("MULTIPLY_BY", "multiply by")
            elif self.source[self.position:self.position + 8] == "divide by":
                self.position += 8
                self.next = Token("DIVIDE_BY", "divide by")
            elif self.source[self.position:self.position + 6] == "negate":
                self.position += 6
                self.next = Token("NEGATE", "negate")
            elif self.source[self.position:self.position + 8] == "increase":
                self.position += 8
                self.next = Token("INCREASE", "increase")
            elif self.source[self.position:self.position + 8] == "decrease":
                self.position += 8
                self.next = Token("DECREASE", "decrease")
            elif self.source[self.position:self.position + 7] == "exceeds":
                self.position += 7
                self.next = Token("EXCEEDS", "exceeds")
            elif self.source[self.position:self.position + 5] == "below":
                self.position += 5
                self.next = Token("BELOW", "below")
            elif self.source[self.position:self.position + 7] == "matches":
                self.position += 7
                self.next = Token("MATCHES", "matches")
            elif self.source[self.position:self.position + 4] == "also":
                self.position += 4
                self.next = Token("ALSO", "also")
            elif self.source[self.position:self.position + 6] == "either":
                self.position += 6
                self.next = Token("EITHER", "either")
            elif self.source[self.position].isalpha():
                start = self.position
                while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_"):
                    self.position += 1
                value = self.source[start:self.position]
                if value in self.keywords:
                    self.next = Token(value.upper(), value)
                else:
                    self.next = Token("IDENT", value)
            elif self.source[self.position] == "(":
                self.position += 1
                self.next = Token("LPAREN", "(")
            elif self.source[self.position] == ")":
                self.position += 1
                self.next = Token("RPAREN", ")")
            else:
                sys.stderr.write("linha:"+ linha.get()+  ": Invalid token at position {self.position}: {self.source[self.position]}\n")
                self.position += 1
                self.selectNext()
            
class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.tokenizer.selectNext()

    @staticmethod
    def parseProgram(tokenizer):
        if tokenizer.next.type == "LAUNCH":
            tokenizer.selectNext()
            if tokenizer.next.type == "NEWLINE":
                tokenizer.selectNext()
                block = Parser.parseBlock(tokenizer)
                return Program("program", [block])
            else:
                sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected NEWLINE after LAUNCH\n")
        else:
            sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected LAUNCH\n")

    @staticmethod
    def parseBlock(tokenizer):
        statements = []
        while tokenizer.next.type not in ["EOF", "END"]:
            statements.append(Parser.parseStatement(tokenizer))
            if tokenizer.next.type == "NEWLINE":
                tokenizer.selectNext()
            else:
                sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected NEWLINE after statement and received:"+ tokenizer.next.type +"\n")
        return Block("block", statements)

    @staticmethod
    @staticmethod
    def parseStatement(tokenizer):
        if tokenizer.next.type == "MODULE":
            tokenizer.selectNext()
            if tokenizer.next.type == "IDENT":
                identifier = Identifier(tokenizer.next.value)
                tokenizer.selectNext()
                if tokenizer.next.type == "SET":
                    tokenizer.selectNext()
                    exp = Parser.parseBoolExpression(tokenizer)
                    if tokenizer.next.type != "NEWLINE":
                        sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected NEWLINE after statement\n")
                    return VarDecl("module", [identifier, exp])
                else:
                    if tokenizer.next.type != "NEWLINE":
                        sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected NEWLINE after statement\n")
                    return VarDecl("module", [identifier])
            else:
                sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected IDENT after MODULE\n")

        elif tokenizer.next.type == "IDENT":
            identifier = Identifier(tokenizer.next.value)
            tokenizer.selectNext()
            if tokenizer.next.type == "SET":
                tokenizer.selectNext()
                exp = Parser.parseBoolExpression(tokenizer)
                if tokenizer.next.type != "NEWLINE":
                    sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected NEWLINE after statement\n")
                return Assignment("set", [identifier, exp])
            else:
                sys.stderr.write("Syntax error: Expected SET after IDENT\n")

        elif tokenizer.next.type == "TRANSMIT":
            tokenizer.selectNext()
            if tokenizer.next.type == "LPAREN":
                tokenizer.selectNext()
                exp = Parser.parseBoolExpression(tokenizer)
                if tokenizer.next.type == "RPAREN":
                    tokenizer.selectNext()
                    if tokenizer.next.type != "NEWLINE":
                        sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected NEWLINE after statement\n")
                    return Print("transmit", [exp])
                else:
                    sys.stderr.write("Syntax error: Expected RPAREN after TRANSMIT expression\n")
            else:
                sys.stderr.write("Syntax error: Expected LPAREN after TRANSMIT\n")

        elif tokenizer.next.type == "ORBIT":
            tokenizer.selectNext()
            exp = Parser.parseBoolExpression(tokenizer)
            if tokenizer.next.type == "DO":
                tokenizer.selectNext()
                if tokenizer.next.type == "NEWLINE":
                    tokenizer.selectNext()
                    block = Parser.parseBlock(tokenizer)
                    if tokenizer.next.type == "END":
                        tokenizer.selectNext()
                        if tokenizer.next.type != "NEWLINE":
                            sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected NEWLINE after statement\n")
                        return While("orbit", [exp, block])
                    else:
                        sys.stderr.write("Syntax error: Expected END after ORBIT block\n")
                else:
                    sys.stderr.write("Syntax error: Expected NEWLINE after DO in ORBIT\n")
            else:
                sys.stderr.write("Syntax error: Expected DO after ORBIT expression\n")

        elif tokenizer.next.type == "CHECK":
            tokenizer.selectNext()
            exp = Parser.parseBoolExpression(tokenizer)
            if tokenizer.next.type == "THEN":
                tokenizer.selectNext()
                if tokenizer.next.type == "NEWLINE":
                    tokenizer.selectNext()
                    block = Parser.parseBlock(tokenizer)
                    if tokenizer.next.type == "END":
                        tokenizer.selectNext()
                        if tokenizer.next.type != "NEWLINE":
                            sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected NEWLINE after statement\n")
                        return If("check", [exp, block])
                    else:
                        sys.stderr.write("Syntax error: Expected END after CHECK block\n")
                else:
                    sys.stderr.write("Syntax error: Expected NEWLINE after THEN in CHECK\n")
            else:
                sys.stderr.write("Syntax error: Expected THEN after CHECK expression\n")

        else:
            sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Invalid statement\n")

        if tokenizer.next.type != "NEWLINE":
            sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected NEWLINE after statement\n")



    @staticmethod
    def parseBoolExpression(tokenizer):
        res = Parser.parseBoolTerm(tokenizer)
        while tokenizer.next.type == "EITHER":
            tokenizer.selectNext()
            res = BinOp("either", [res, Parser.parseBoolTerm(tokenizer)])
        return res

    @staticmethod
    def parseBoolTerm(tokenizer):
        res = Parser.parseRelExpression(tokenizer)
        while tokenizer.next.type == "ALSO":
            tokenizer.selectNext()
            res = BinOp("also", [res, Parser.parseRelExpression(tokenizer)])
        return res

    @staticmethod
    def parseRelExpression(tokenizer):
        res = Parser.parseExpression(tokenizer)
        while tokenizer.next.type in ["EXCEEDS", "BELOW", "MATCHES"]:
            if tokenizer.next.type == "EXCEEDS":
                tokenizer.selectNext()
                res = BinOp("exceeds", [res, Parser.parseTerm(tokenizer)])
            elif tokenizer.next.type == "BELOW":
                tokenizer.selectNext()
                res = BinOp("below", [res, Parser.parseTerm(tokenizer)])
            elif tokenizer.next.type == "MATCHES":
                tokenizer.selectNext()
                res = BinOp("matches", [res, Parser.parseTerm(tokenizer)])
        return res

    @staticmethod
    def parseExpression(tokenizer):
        res = Parser.parseTerm(tokenizer)
        while tokenizer.next.type in ["INCREASE", "DECREASE"]:
            if tokenizer.next.type == "INCREASE":
                tokenizer.selectNext()
                res = BinOp("increase", [res, Parser.parseTerm(tokenizer)])
            elif tokenizer.next.type == "DECREASE":
                tokenizer.selectNext()
                res = BinOp("decrease", [res, Parser.parseTerm(tokenizer)])
        return res

    @staticmethod
    def parseTerm(tokenizer):
        res = Parser.parseFactor(tokenizer)
        while tokenizer.next.type in ["MULTIPLY_BY", "DIVIDE_BY"]:
            if tokenizer.next.type == "MULTIPLY_BY":
                tokenizer.selectNext()
                res = BinOp("multiply by", [res, Parser.parseFactor(tokenizer)])
            elif tokenizer.next.type == "DIVIDE_BY":
                tokenizer.selectNext()
                res = BinOp("divide by", [res, Parser.parseFactor(tokenizer)])
        return res

    @staticmethod
    def parseFactor(tokenizer):
        if tokenizer.next.type == "INT":
            res = IntVal(tokenizer.next.value)
            tokenizer.selectNext()
            return res
        elif tokenizer.next.type == "IDENT":
            res = Identifier(tokenizer.next.value)
            tokenizer.selectNext()
            return res
        elif tokenizer.next.type == "LPAREN":
            tokenizer.selectNext()
            res = Parser.parseBoolExpression(tokenizer)
            if tokenizer.next.type == "RPAREN":
                tokenizer.selectNext()
                return res
            else:
                sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected RPAREN\n")
        elif tokenizer.next.type in ["NEGATE", "-"]:
            op = tokenizer.next.type
            tokenizer.selectNext()
            res = UnOp(op, [Parser.parseFactor(tokenizer)])
            return res
        else:
            sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Invalid factor\n")
            return NoOp()

    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        tokenizer = Tokenizer(code)
        parser = Parser(tokenizer)
        result = parser.parseProgram(tokenizer)
        if parser.tokenizer.next.type != "EOF":
            sys.stderr.write("linha:"+ linha.get()+ ": Syntax error: Expected EOF\n")
        else:
            return result


class Node():
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

    @abstractmethod
    def evaluate(self, ST):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST):
        left = self.children[0].evaluate(ST)
        right = self.children[1].evaluate(ST)
        
        if self.value == 'increase':
            return [int(left[0]) + int(right[0]), "int"]
        elif self.value == 'decrease':
            return [int(left[0]) - int(right[0]), "int"]
        elif self.value == 'multiply by':
            return [int(left[0]) * int(right[0]), "int"]
        elif self.value == 'divide by':
            return [int(left[0]) / int(right[0]), "int"]
        elif self.value == 'exceeds':
            return [int(left[0] > right[0]), "int"]
        elif self.value == 'below':
            return [int(left[0] < right[0]), "int"]
        elif self.value == 'matches':
            return [int(left[0] == right[0]), "int"]
        elif self.value == 'either':
            return [left[0] or right[0], "int"]
        elif self.value == 'also':
            return [left[0] and right[0], "int"]
        else:
            sys.stderr.write("linha:"+ linha.get()+ ": Invalid operation\n")
            return 0

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST):
        child = self.children[0].evaluate(ST)
        if self.value == 'negate':
            return [int(not child[0]), "int"]
        elif self.value == '-':
            return [-int(child[0]), "int"]

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, ST):
        return [int(self.value), "int"]

class NoOp(Node):
    def __init__(self):
        super().__init__(None, None)

    def evaluate(self, ST):
        pass

class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST):
        value = self.children[0].evaluate(ST)
        print(value[0])

class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST):
        value = self.children[1].evaluate(ST)
        ST.set(self.children[0].value, value[0], value[1])

class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, ST):
        return ST.get(self.value)

class VarDecl(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST):
        ST.create(self.children[0].value)
        if len(self.children) == 2:
            value = self.children[1].evaluate(ST)
            ST.set(self.children[0].value, value[0], value[1])

class While(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST):
        while self.children[0].evaluate(ST)[0]:
            self.children[1].evaluate(ST)

class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST):
        if self.children[0].evaluate(ST)[0]:
            self.children[1].evaluate(ST)
        elif len(self.children) == 3:
            self.children[2].evaluate(ST)

class Program(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST):
        self.children[0].evaluate(ST)

class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST):
        for child in self.children:
            child.evaluate(ST)


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def create(self, symbol):
        self.symbols[symbol] = None

    def set(self, symbol, value, type):
        self.symbols[symbol] = [value, type]

    def get(self, symbol):
        return self.symbols[symbol]
    

def main():

    filename = sys.argv[1]

    if filename.endswith('.ac'):
        with open(filename, 'r') as file:
            code = file.read()
    
    parser = Parser.run(code)
    ST = SymbolTable()
    resultado = parser.evaluate(ST)
    

    

if __name__ == "__main__":
    main()


    