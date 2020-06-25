from io import StringIO
from decimal import Decimal
from datetime import datetime, date, time

class SQL:
    def __init__(self):
        self.buffer = StringIO()

    def __len__(self):
        return self.buffer.tell()

    def __str__(self):
        return self.buffer.getvalue()

    def __bool__(self):
        return len(self)>0

    def sql(self, sql):
        self.buffer.write(sql)
        return self

    def quoted(self, name):
        return self.sql('`'+name.replace('`','``')+'`')

    def arg(self):
        return self.sql('%s')

    def kwarg(self, name):
        return self.sql(f'%({name})s')

    def literal(self, *args):
        for i, value in enumerate(args):
            self.sql(',' if i else '')
            if value is None:
                self.sql('NULL')
            elif isinstance(value,bool):
                self.sql('1' if value else '0')
            elif isinstance(value,(int,float,Decimal)):
                self.sql(str(value))
            elif isinstance(value,(datetime,date,time)):
                self.sql("'").sql(str(value)).sql("'")
            elif isinstance(value,str):
                value = value.replace("'","''")
                self.sql("'").sql(value).sql("'")
            elif isinstance(value,tuple):
                self.sql("(").literal(*value).sql(")")
            else:
                raise NotImplementedError()
        return self

    def _list(self, func, iterable, separator=','):
        for i, x in enumerate(iterable):
            self.sql(separator if i else '')
            func(x)

    def SELECT(self, *args):
        self.sql('SELECT ')
        if not args:
            self.sql('* ')
        else:
            self._list(self.quoted, args)
            self.sql(' ')
        return self

    def FROM(self, table):
        self.sql('FROM ')
        self.quoted(table)
        self.sql(' ')
        return self

    def WHERE(self, **kwargs):
        self.sql(' WHERE ')
        for i, (k,v) in enumerate(kwargs.items()):
            self.sql(',' if i else '')
            self.quoted(k).sql('=').literal(v)
        return self

    def _indexInSet(self, index, keys):
        self.sql('(')
        self._list(self.quoted, index)
        self.sql(') IN (' )
        self._list(self.literal, keys)
        self.sql(') ')

    def WHERE_INDEX_IN(self, index, keys):
        self.sql('WHERE ')
        self._indexInSet(index, keys)
        return self

    def WHERE_INDEX_KEY(self, index, key):
        self.sql(' WHERE (')
        self._list(self.quoted, index)
        self.sql(')=(' )
        self.literal(key)
        self.sql(') ')
        return self

    def INSERT_ARGS(self, table, columns):
        self.sql('INSERT INTO ')
        self.quoted(table)
        self.sql('(')
        self._list(self.quoted, columns)
        self.sql(') VALUES (' )
        self._list(self.arg, columns)
        self.sql(')')
        return self

    def INSERT(self, table, columns, values):
        self.sql('INSERT INTO ')
        self.quoted(table)
        self.sql(' (')
        self._list(self.quoted, columns)
        self.sql(') VALUES (' )
        self._list(self.literal, values)
        self.sql(')')
        return self

    def UPDATE(self, table):
        self.sql('UPDATE ')
        self.quoted(table)
        self.sql(' ')
        return self

    def SET(self, **kwargs):
        def setPair(x):
            self.quoted(x[0])
            self.sql('=')
            self.literal(x[1])
        self.sql('SET ')
        self._list( setPair, kwargs.items())
        return self

    def SET_CV(self, columns, values):
        def setPair(x):
            self.quoted(x[0])
            self.sql('=')
            self.literal(x[1])
        self.sql('SET ')
        self._list( setPair, zip(columns,values))
        return self

