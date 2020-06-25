from .dbi import MySQL_DBI_MySQLdb
from .metadata import MySQL_MetadataMixIn

class MySQL_DBI(MySQL_MetadataMixIn, MySQL_DBI_MySQLdb):
    pass

DBI = MySQL_DBI