from etlx.sql.parse.lexer import SQLLexer

class SQLParser:
    def __init__(self, sql):
        self.lexer = SQLLexer(sql, whitespaces=False, comments=False)

    def __iter__(self):
        tokens = []
        i = iter(self.lexer)
        x = next(i,None)
        while x:
            if x.ttype==self.lexer.DELIMITER:
                if tokens:
                    yield tokens
                tokens = []
            else:
                tokens.append(x)
            x = next(i,None)
        if tokens:
            yield tokens

