import sqlite3
import os


if not os.path.exists('./data/database.db'):
    with open('./data/database.db', 'w'):
        pass


connection = sqlite3.connect('./data/database.db')
cursor = connection.cursor()

list_migrations = os.listdir('./migrations')

for migration in list_migrations:
    mig_path = f"./migrations/{migration}"
    with open(mig_path, 'r') as mig:
        sql_statements = mig.read().split(';')

        for sql_statement in sql_statements:
            if sql_statement.strip(): 
                cursor.execute(sql_statement)
connection.commit()
connection.close()

print('Migrations executed successfully')
