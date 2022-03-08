from sqlalchemy import create_engine, exc

params = urllib.parse.quote_plus(r'Driver=/usr/local/lib/libmsodbcsql.17.dylib;Server=tcp:uclcs-ixn-9-2122.database.windows.net,1433;Database=database2;Uid=yufei.gu.20@ucl.ac.uk;Pwd=Uclcsixn9;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
e = create_engine(conn_str)
c = e.connect()

try:
    # suppose the database has been restarted.
    c.execute("SELECT * FROM table")
    c.close()
except exc.DBAPIError, e:
    # an exception is raised, Connection is invalidated.
    if e.connection_invalidated:
        print("Connection was invalidated!")

# after the invalidate event, a new connection
# starts with a new Pool
c = e.connect()
c.execute("SELECT * FROM table")