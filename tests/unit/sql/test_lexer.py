import unittest
from etlx.sql.parse.lexer import SQLLexer

class Test_sql_SQLLexer(unittest.TestCase):

    def test0_name(self):
        sql="SELECT AbcZ_109"
        lexer = SQLLexer(sql)
        tokens = list(lexer)
        self.assertEqual( len(tokens), 3)
        x = tokens[0]
        self.assertEqual( x.ttype,  'NAME')
        self.assertEqual( x.value, 'SELECT')
        self.assertEqual( x.line,  1)
        self.assertEqual( x.col,  1)

        x = tokens[1]
        self.assertEqual( x.ttype,  'WHITESPACE')
        self.assertEqual( x.value, ' ')
        self.assertEqual( x.line,  1)
        self.assertEqual( x.col,  7)

        x = tokens[2]
        self.assertEqual( x.ttype,  'NAME')
        self.assertEqual( x.value, 'AbcZ_109')
        self.assertEqual( x.line,  1)
        self.assertEqual( x.col,  8)

    def test1_num(self):
        sql="""12 
        3.14 987654321"""
        lexer = SQLLexer(sql)
        tokens = list(lexer)
        self.assertEqual( len(tokens), 5)
        x = tokens[0]
        self.assertEqual( x.ttype,  'INT')
        self.assertEqual( x.value, '12')
        self.assertEqual( x.line,  1)
        self.assertEqual( x.col,  1)

        x = tokens[1]
        self.assertEqual( x.ttype,  'WHITESPACE')
        self.assertEqual( x.line,  1)
        self.assertEqual( x.col,  3)

        x = tokens[2]
        self.assertEqual( x.ttype,  'FLOAT')
        self.assertEqual( x.value, '3.14')
        self.assertEqual( x.line,  2)
        self.assertEqual( x.col,  9)

