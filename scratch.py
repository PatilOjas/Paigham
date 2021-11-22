from math import ceil
from typing import Counter
import psycopg2
from datetime import datetime


# Database connector
dbConn = psycopg2.connect(database="scratch", user="postgres", password="12345678", host="localhost", port=5432)
dbConn.autocommit = True
dbCursor = dbConn.cursor()

##############################         DO NOT DELETE FOLLOWING CONTENT              ###############################


# try: 
# 	dbCursor.execute("""
# 	CREATE TABLE mediafiles (
# 		timestamp TIMESTAMP,
# 		extension text,
# 		media bytea
# 	);
# 	""")
# except:
# 	pass

# path =  "C:/Users/ojasp/Pictures/a.png"
# file_ext = path.split('.')[-1]
# f = open("C:/Users/ojasp/Pictures/a.png", 'rb').read()
# dbCursor.execute(f"""INSERT INTO mediafiles (timestamp, extension, media) VALUES( LOCALTIMESTAMP, %s, %s)""", (file_ext, psycopg2.Binary(f)))
# dbConn.commit()

# dbCursor.execute("SELECT media, extension FROM mediafiles")
# blob = dbCursor.fetchall()[-1]
# print(blob)
# open(f'fetched.png', 'wb').write(blob[0])

#################################################################################################################

