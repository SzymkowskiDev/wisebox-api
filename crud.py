from database import engine
from fastapi import APIRouter
import models
from sqlalchemy import text

magazine = APIRouter()


@magazine.get('/showall')
def show_all():
    list_of_data = []
    with engine.connect() as conn:
        result = conn.execute(text('''SELECT * from MAGAZINES'''))
        for i in result:
            list_of_data.append(i)
    return list_of_data


@magazine.post('/showone')
def show_one(data: models.Id):
    with engine.connect() as conn:
        result = list(conn.execute(text(f'''SELECT * from MAGAZINES WHERE ROWID={data.user_id}''')))
    return result


@magazine.post('/add')
def add_data(column: models.Columns):
    with engine.connect() as conn:
        result = conn.execute(text(
            f'''INSERT INTO MAGAZINES VALUES('{column.USER_ID}', '{column.MAG_ID}', '{column.NAME}', '{column.DESCRIPTION}', '{column.AVATAR}', '{column.LOCATION}', '{column.DATE_OF_CREATION}')'''))
    return 'Data correctly added.'


@magazine.post('/update')
def data_update(data: models.UserUpdate):
    with engine.connect() as conn:
        result = conn.execute(
            text(f'''UPDATE MAGAZINES SET {data.column_name}='{data.new_data}' WHERE ROWID={data.user_id}'''))
    return 'Data correctly updated.'


@magazine.delete('/delete')
def delete_item(data: models.Id):
    with engine.connect() as conn:
        result = conn.execute(text(f'''DELETE from MAGAZINES WHERE ROWID={data.user_id}'''))
    return 'Data correctly deleted.'

