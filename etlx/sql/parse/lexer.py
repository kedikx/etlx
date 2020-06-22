from collections import deque

class SQLToken:
    def __init__(self, lexer, ttype, value=''):
        self.line = lexer.line
        self.col = lexer.col
        self.ttype = ttype
        self.value = value

class SQLLexer:

    WHITESPACE = 'WHITESPACE'
    COMMENT    = 'COMMENT'
    NAME       = 'NAME'
    QUOTED     = 'QUOTED'
    INT        = 'INT'
    FLOAT      = 'FLOAT'
    CHAR       = 'CHAR'
    COMMA      = 'COMMA'
    DOT        = 'DOT'
    COLON      = 'COLON'
    SEMICOLON  = 'SEMICOLON'
    DELIMITER  = 'DELIMITER'

    def __init__(self, sql, *, whitespaces=False, comments=False):
        self.buffer = str(sql)
        self.pos = 0
        self.line = 1
        self.col = 1
        self.delimiter = ';'
        self.whitespaces = whitespaces
        self.comments = comments

    def peek(self, n=1):
        s = self.buffer[self.pos:self.pos+n]
        return s if s else None

    def read(self, n=1):
        s = self.buffer[self.pos:self.pos+n]
        for c in s:
            self.pos += 1
            self.col +=1 
            if c=='\n':
                self.line += 1
                self.col = 1
        return s if s else None

    def read_line(self):
        value = ''
        c = self.peek()
        while c and c!='\n':
            value += self.read()
            c = self.peek()
        return value

    def is_whitespace(self, c):
        return c and c in (' ','\t','\n')

    def is_alpha(self, c):
        return c and ((c>='a' and c<='z') or (c>='A' and c<='Z') or c=='_')

    def is_digit(self, c):
        return c and c>='0' and c<='9'

    def read_whitespace(self):
        x = SQLToken(self,  self.WHITESPACE, '')
        while self.is_whitespace(self.peek()):
            x.value += self.read()
#        if not x.value:
#            return None
        return x

    def read_name(self):
        x = SQLToken(self,  self.NAME)
        c = self.peek()
        while self.is_alpha(c) or self.is_digit(c):
            x.value += self.read()
            c = self.peek()
        return x

    def read_number(self):
        x = SQLToken(self,  self.INT)
        while self.is_digit(self.peek()):
            x.value += self.read()
        if self.peek()!='.':
            return x
        x.ttype = self.FLOAT
        x.value += self.read()
        while self.is_digit(self.peek()):
            x.value += self.read()
        return x

    def read_comment_single(self):
        x = SQLToken(self,  self.COMMENT)
        x.value = self.read_line()
        return x

    def read_comment_multi(self):
        x = SQLToken(self,  self.COMMENT)
        c = self.peek()
        while c and x.value[-2:] != '*/':
            x.value += self.read()
            c = self.peek()
        return x
    
    def read_quoted(self):
        q = self.peek()
        x = SQLToken(self,self.CHAR if q=="'" else self.QUOTED)
        self.read()
        while True:
            c = self.read()
            if not c:
                break
            if c==q:
                if self.peek()!=q: 
                    break
                self.read()
            x.value += c
        return x

    def __iter__(self):
        while True:
            if self.peek() is None:
                break
            dlen = len(self.delimiter)
            if self.peek(dlen)==self.delimiter:
                x = SQLToken(self, 'DELIMITER')
                x.value = self.read(dlen)
                yield x
            elif self.is_whitespace(self.peek()):
                x = self.read_whitespace()
                if self.whitespaces:
                    yield x
            elif self.peek()=='#':
                x = self.read_comment_single()
                if self.comments:
                    yield x
            elif self.peek(2) == '--':
                x = self.read_comment_single()
                if self.comments:
                    yield x
            elif self.peek(2) == '/*':
                x = self.read_comment_multi()
                if self.comments:
                    yield x
            elif self.is_alpha(self.peek()):
                x = self.read_name()
                if x.value.upper()=='DELIMITER':
                    self.read_whitespace()
                    x = SQLToken(self,self.DELIMITER)
                    c = self.peek()
                    while c and not self.is_whitespace(c):
                        x.value += self.read()
                        c = self.peek()
                    self.delimiter = x.value
                yield x
            elif self.is_digit(self.peek()):
                yield self.read_number()
            elif self.peek() in ("'",'"','`'):
                yield self.read_quoted()
            elif self.peek()=='.':
                yield SQLToken(self, self.DOT, self.read())
            elif self.peek()==',':
                yield SQLToken(self, self.COMMA, self.read())
            elif self.peek()==':':
                yield SQLToken(self, self.COLON, self.read())
            elif self.peek()==';':
                yield SQLToken(self, self.SEMICOLON, self.read())
            elif self.peek() in ('(',')'):
                yield SQLToken(self, '()', self.read())
            elif self.peek(2) in ('!=','<>','<=','>=','+='):
                yield SQLToken(self, 'X2', self.read(2))
            elif self.peek() in ('=','+','-','*','/'):
                yield SQLToken(self, 'X1', self.read())
            else:
                x = SQLToken(self, '?')
                c = self.peek()
                while c and not self.is_whitespace(c):
                    x.value += self.read()
                    c = self.peek()
                yield x

