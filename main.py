from fastapi import Body, FastAPI, status, HTTPException
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime

app = FastAPI()

try:
    con = psycopg2.connect(
        host='localhost', database='postgres', user='postgres', password='admin123')
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
            "id": x[0],
            "username": x[1],
            "password": x[2],
            "email": x[3],
            "created_on": x[4],
            "last_login": x[5],
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

# def put_posts(id,name,password)
@app.put("/add_accounts", status_code=status.HTTP_201_CREATED)
def put_posts(account: str = Body(..., embed=True)):
    # query = f"""insert into accounts values({id},'{name}','{password}',"{name}@mail.com",datetime.now(),datetime.now());"""
    # cursor.execute(query)
    # result = cursor.fetchall()
    # cursor.close()
    # con.commit()
    return account


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
