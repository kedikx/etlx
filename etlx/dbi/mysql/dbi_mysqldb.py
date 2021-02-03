import MySQLdb
from etlx.dbi.abc import DBI
from etlx.sql import SQL

class SQL_MySQL(SQL):
    
    def quoted(self, *args):
        for i, name in enumerate(args):
            self.sql("," if i else "")
            self.sql('`' + name.replace('`', '``') + '`')
        return self


class DBI_MySQL_MySQLdb(DBI):

    def connect_factory(self, **kwargs):
        return MySQLdb.connect(**kwargs)

    @property
    def sql(self):
        return SQL_MySQL(self)

    
