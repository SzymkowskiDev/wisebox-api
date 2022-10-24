from fastapi import APIRouter
import sqlite3
import models

magazine = APIRouter()


# @app.post('/create_table')
# def create_table(column: models.Columns):
#     db = sqlite3.connect('wisebox_database.db', check_same_thread=False)
#     cursor = db.cursor()
#     cursor.execute(f'''CREATE TABLE MAGAZINES(...)''')
#     db.commit()
#     db.close()
#     return 'ok'


@magazine.post('/add')
def add_data(column: models.Columns):
    db = sqlite3.connect('wisebox_database.db', check_same_thread=False)
    cursor = db.cursor()
    cursor.execute(
        f'''INSERT INTO MAGAZINES VALUES('{column.USER_ID}', '{column.MAG_ID}', '{column.NAME}', '{column.DESCRIPTION}', '{column.AVATAR}', '{column.LOCATION}', '{column.DATE_OF_CREATION}')''')
    db.commit()
    db.close()
    return 'ok'


@magazine.post('/updating_data')
def add_data(data: models.UserUpdate):
    db = sqlite3.connect('wisebox_database.db', check_same_thread=False)
    cursor = db.cursor()
    cursor.execute(f'''UPDATE MAGAZINES SET {data.column_name}='{data.new_data}' WHERE ROWID={data.user_id}''')
    db.commit()
    db.close()
    return 'ok'


@magazine.get('/showall')
def show_all():
    db = sqlite3.connect('wisebox_database.db', check_same_thread=False)
    cursor = db.cursor()
    list_of_data = []
    for i in cursor.execute('''SELECT * from MAGAZINES'''):
        list_of_data.append(i)
    db.commit()
    db.close()
    return list_of_data


@magazine.post('/showone')
def show_one(data: models.Id):
    db = sqlite3.connect('wisebox_database.db', check_same_thread=False)
    cursor = db.cursor()
    one = list(cursor.execute(f'''SELECT * from MAGAZINES WHERE ROWID={data.user_id}'''))
    db.commit()
    db.close()
    return one


@magazine.delete('/delete')
def delete_item(data: models.Id):
    db = sqlite3.connect('wisebox_database.db', check_same_thread=False)
    cursor = db.cursor()
    cursor.execute(f'''DELETE from MAGAZINES WHERE ROWID={data.user_id}''')
    db.commit()
    db.close()
































# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
#
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
#
#
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
#
#
# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
#
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
