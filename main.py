from fastapi import FastAPI, Request, status, HTTPException
import psycopg2
from psycopg2.extras import DictCursor
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel    # to define the schema of our data
from random import randrange

from starlette.responses import Response
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

@app.post("/check_users", status_code=status.HTTP_201_CREATED)
def put_posts(id):
    print(id)
    cursor.execute(f'select * from accounts where id = {id};')
    result = cursor.fetchall()
    cursor.close()
    con.commit()
    return result

@app.get("/accounts/{id}")
def get_accounts(id: int):

    cursor.execute(f'select * from accounts where user_id = {id};')
    result = cursor.fetchall()
    con.commit()
    print(result)

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found in accounts!!")
    else:
        return f"{result[0][1]} User with id {id} is present in accounts!!"