from fastapi import Body, FastAPI, status, HTTPException
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from pydantic import BaseModel    # to define the schema of our data
from random import randrange
from typing import Optional

app = FastAPI()

try:
    con = psycopg2.connect(
        host='localhost', database='postgres', user='postgres', password='admin123')
    cursor = con.cursor(cursor_factory=DictCursor)
    print("database connection successful")
except Exception as ex:
    print(ex)


class Account(BaseModel):
    id: int
    name: str
    password: str      # default is True
    email: str      # Optional field, default None
    created_on: Optional[datetime] = datetime.now()
    last_modified: Optional[datetime] = datetime.now()


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
def home():
    accounts_list = get_table_data(cursor)
    return accounts_list


@app.post("/add_account/", status_code=status.HTTP_201_CREATED)
def add_account(account: Account):

    query = f"""insert into accounts values({account.id},
					'{account.name}',
					'{account.password}',
					'{account.email}',
					'{account.created_on}',
					'{account.last_modified}');
				"""
    cursor.execute(query)
    con.commit()

    return {"status": "SUCCESS", "data": f"{account.id} inserted"}


@app.get("/check_account/{id}")
def check_account_exists(id: int):

    query = f'select * from accounts where user_id = {id};'
    cursor.execute(query)
    result = cursor.fetchall()
    con.commit()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found in accounts!!")
    else:
        return f"{result[0][1]} User with id {id} is present in accounts!!"


@app.post("/update_detail", status_code=status.HTTP_201_CREATED)
def update_account_info(account: Account):

    query = f""" UPDATE accounts
                    SET email = '{account.email}',
                        username = '{account.name}',
                        password = '{account.password}'
                    WHERE user_id = {account.id};
                """
    cursor.execute(query)
    con.commit()
    return {"status": "SUCCESS", "data": f"{account.id} updated with {account.email}"}

@app.delete("/delete_account/{id}", status_code=status.HTTP_200_OK)
def delete_account(id: int):

    query = f""" DELETE FROM accounts
                    WHERE user_id = {int(id)};
                """
    cursor.execute(query)
    con.commit()
    return {"status": "SUCCESS", "data": f"account with id {id} deleted"}
