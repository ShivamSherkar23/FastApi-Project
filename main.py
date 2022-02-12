from fastapi import FastAPI, Request
import psycopg2
from psycopg2.extras import DictCursor

app = FastAPI()

try:
    con = psycopg2.connect(host='localhost',database='postgres',user='postgres',password='admin123')
    cursor = con.cursor(cursor_factory=DictCursor)
    print("database connection successful")
except Exception as ex:
    print(ex)

def get_table_data(cursor):
  cursor.execute('select * from accounts;')
  result = cursor.fetchall()
  output = []
  for x in result:
    op_dict = {
      "id":x[0],
      "username":x[1],
      "password":x[2],
      "email":x[3],
      "created_on":x[4],
      "last_login":x[5],
    }
    output.append(op_dict)
#   cursor.close()
#   con.close()
  con.commit()
  return output


@app.get("/")
def read_root():
    accounts_data = get_table_data(cursor)
    return accounts_data