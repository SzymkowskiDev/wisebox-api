from random import randint,choice
import sqlite3
import string

con = sqlite3.connect("test.db")
cur = con.cursor()

cur.execute("SELECT name,no,price,description,pictures FROM magazine")
result = cur.fetchall()


cur.close()
con.close()

def radom_data() -> int:
    mounth = randint(1,12)
    if mounth < 10:
        mounth = "0" + str(mounth)
    
    return f"{randint(2010,2022)}-{mounth}-{randint(10,30)}"

def upadate_products():
    for i in result:
        con_wisebox = sqlite3.connect("wisebox_database.db")
        cur_wisebox = con_wisebox.cursor()
        

        cur_wisebox.execute(f"""INSERT INTO PRODUCTS(MAG_ID,NAME,STATUS,QUANTITY,PRICE,DESCRIPTION,IMAGE,LOCATION,EXPIRY_DATE) 
        VALUES (?,?,?,?,?,?,?,?,?); """,(int(randint(1,5)),str(i[0]),str(choice(['In stock','Sold','Damaged','Lost'])),str(i[1]),float(i[2]),str(i[3]),str(i[4]).split(',')[0],str(choice(string.ascii_letters))+str(randint(100,999)),str(radom_data())))
        
        con_wisebox.commit()
        cur_wisebox.close()
        con_wisebox.close()

upadate_products()