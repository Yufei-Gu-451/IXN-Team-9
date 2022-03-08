import pyodbc
server = 'uclcs-ixn-9-2122.database.windows.net'
database = 'database2'
username = 'yufei.gu.20@ucl.ac.uk'
password = '{Uclcsixn9}'   
driver= '/usr/local/lib/libmsodbcsql.17.dylib'

# Server=tcp:uclcs-ixn-9-2122.database.windows.net,1433;Initial Catalog=database2;
# Persist Security Info=False;User ID=yufei.gu.20@ucl.ac.uk@uclcs-ixn-9-2122;Password={your_password};
# MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()