# Note :
# Untuk saat ini DBTemp tidak akan menggunakan DBMS
# tetapi akan menggunakan data log

import pyorient
client = pyorient.OrientDB("localhost", 2424)

# Connect to OrientDB Server
session_id = client.connect("admin", "admin")
print("Server Connect with 'root' Account")

# Get Database List
database_list = client.db_list().__getattr__('databases')

# Database List
for i in database_list:
    try:
        client.db_open(i, "root", "123456")
        print("Default Credentials found on: %s" % i)
        client.db_close()
    except:
        print("Non-defaut Credentials found on: %s" % i)

# Close Connection
client.shutdown('root', '123456')
print("Connection Closed")