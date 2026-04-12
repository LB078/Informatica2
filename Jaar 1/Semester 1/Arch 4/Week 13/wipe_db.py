import sqlite3
import os 
import sys


connection = sqlite3.connect(
            os.path.join(sys.path[0], "carparkingmachine.db")
        )
cursor = connection.cursor()

cursor.execute("""
DROP TABLE parkings
""")