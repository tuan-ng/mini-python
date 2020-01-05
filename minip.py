import sys
import pprint


class Token:
    def __init__(self, line, column, value=None):
        self.line = line
        self.column = column
        self.value = value

    def __repr__(self):
        return 't: {}, line: {}, column: {}'.format(self.value, self.line, self.column)


class UnsignedInt(Token):
    pass


class UnsignedFloat(Token):
    pass


class Name(Token):
    pass


class Print(Token):
    pass


class Assign(Token):
    pass


class LeftParen(Token):
    pass


class RightParen(Token):
    pass


class Plus(Token):
    pass


class Minus(Token):
    pass


class Times(Token):
    pass


class Divide(Token):
    pass


class NewLine(Token):
    pass


class Pass(Token):
    pass


class If(Token):
    pass


class Else(Token):
    pass


class While(Token):
    pass


class T(Token):
    pass


class F(Token):
    pass


class N(Token):
    pass


class Equal(Token):
    pass


class NEqual(Token):
    pass


class Less(Token):
    pass


class LessEqual(Token):
    pass


class Greater(Token):
    pass


class GreaterEqual(Token):
    pass


class String(Token):
    pass


class Colon(Token):
    pass


class Indent(Token):
    pass


class Dedent(Token):
    pass


class Def(Token):
    pass


def split(s):
    try:
        return (s[0], s[1:])
    except IndexError:
        return ('', '')


operators = ['=', '(', ')', '+', '-', '*', '/',
             '==', '!=', '<', '<=', '>', '>=', ':']


def get_operator_token(k, line, column):
    if k == '=':
        return Assign(line, column, 'ASSIGN')
    elif k == '(':
        return LeftParen(line, column, 'LPAREN')
    elif k == ')':
        return RightParen(line, column, 'RPAREN')
    elif k == '+':
        return Plus(line, column, 'PLUS')
    elif k == '-':
        return Minus(line, column, 'MINUS')
    elif k == '*':
        return Times(line, column, 'TIMES')
    elif k == '/':
        return Divide(line, column, 'DIVIDES')
    elif k == '==':
        return Equal(line, column, 'EQUAL')
    elif k == '!=':
        return NEqual(line, column, 'NEQUAL')
    elif k == '<':
        return Less(line, column, 'LESS')
    elif k == '<=':
        return LessEqual(line, column, 'LEQUAL')
    elif k == '>':
        return Greater(line, column, 'GREATER')
    elif k == '>=':
        return GreaterEqual(line, column, 'GEQUAL')
    elif k == ':':
        return Colon(line, column, 'COLON')
    else:
        raise RuntimeError('Unknown operator')


keywords = ['print', 'pass', 'if', 'else',
            'while', 'True', 'False', 'None', 'def']


def get_keyword_token(k, line, column):
    if k == 'print':
        return Print(line, column, 'PRINT')
    elif k == 'pass':
        return Pass(line, column, 'PASS')
    elif k == 'if':
        return If(line, column, 'IF')
    elif k == 'else':
        return Else(line, column, 'ELSE')
    elif k == 'while':
        return While(line, column, 'WHILE')
    elif k == 'True':
        return T(line, column, 'TRUE')
    elif k == 'False':
        return F(line, column, 'FALSE')
    elif k == 'None':
        return N(line, column, 'NONE')
    elif k == 'def':
        return Def(line, column, 'DEF')
    else:
        raise RuntimeError('Unknown keyword')


def tokenize(s):
    '''
      src is a string
    '''

    tokens = []
    line = 1
    column = 0
    indent_stack = [0]
    indent = 0

    def adjust_indent_stack(indent):
        if indent > indent_stack[-1]:
            indent_stack.append(indent)
            tokens.append(Indent(line, column, 'INDENT'))
        elif indent < indent_stack[-1]:
            while (indent < indent_stack[-1]):
                indent_stack.pop()
                tokens.append(Dedent(line, column, 'DEDENT'))
        else:
            pass

    def fill_tokens(t, s):
        nonlocal line, column, indent
        column += 1

        if t == '\n':
            tokens.append(NewLine(line, column, 'NEWLINE'))
            line += 1
            column = 0
            c, s = split(s)
            if c != '\n' and not c.isspace():
                adjust_indent_stack(indent)
            fill_tokens(c, s)
        elif t.isspace():
            if isinstance(tokens[-1], NewLine):
                indent += 1
                column += 1
                b, s = split(s)
                while b.isspace():
                    indent += 1
                    column += 1
                    b, s = split(s)
                adjust_indent_stack(indent)
                indent = 0
                fill_tokens(b, s)
            else:
                fill_tokens(*split(s))
        elif t == '#':
            b, s = split(s)
            while b != '\n':
                b, s = split(s)
            fill_tokens(b, s)
        elif t == '\'':
            string = ''
            c, s = split(s)
            while c != '\'':
                if c == '\\':
                    cc, s = split(s)
                    if cc == 'n':
                        string += '\n'
                    elif cc == 't':
                        string += '\t'
                    else:
                        string += cc
                else:
                    string += c
                c, s = split(s)
            tokens.append(String(line, column, string))
            c, s = split(s)
            fill_tokens(c, s)
        elif t.isdigit() or t == '.':
            c = column
            d, s = split(s)
            if t.isdigit():
                if d == '.':
                    t += d
                    d, s = split(s)
            else:
                if not d.isdigit():
                    raise RuntimeError('. alone is invalid')
            while d.isdigit():
                column += 1
                t += d
                d, s = split(s)
            if '.' in t:
                tokens.append(UnsignedInt(line, c, float(t)))
            else:
                tokens.append(UnsignedInt(line, c, int(t)))
            fill_tokens(d, s)
        elif t.isalpha():
            c = column
            l, s = split(s)
            while l.isalnum():
                column += 1
                t += l
                l, s = split(s)
            if t in keywords:
                tokens.append(get_keyword_token(t, line, c))
            else:
                tokens.append(Name(line, c, t))
            fill_tokens(l, s)
        elif t in operators or t == '!':
            o, s = split(s)
            tt = t + o
            if (tt in operators):
                tokens.append(get_operator_token(tt, line, column))
                fill_tokens(*split(s))
            elif (t in operators):
                tokens.append(get_operator_token(t, line, column))
                fill_tokens(o, s)
            else:
                raise RuntimeError('! alone is invalid')
        elif not t:
            return
        else:
            raise RuntimeError('Invalid character %s' % t)

    pp = pprint.PrettyPrinter(indent=4)
    try:
        fill_tokens(*split(s))
        pp.pprint(tokens)
    except RuntimeError as emsg:
        pp.pprint(tokens)
        print('Error on line {} and column {}'.format(line, column))
        print(emsg)


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as infile:
        code = infile.read()
    tokenize(code)
