import sqlite3

def create_db():
    con=sqlite3.connect(database=r'pntb.db')#creating connection, r is used to avoid path issue
    cur=con.cursor() #to execute queries
    #cur.execute("DROP TABLE IF EXISTS employee")
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,"
                "name TEXT,email TEXT,gender TEXT,contact TEXT,dob TEXT,doj TEXT,pass TEXT,utype TEXT,"
                "address TEXT,salary TEXT)")#to create table
    con.commit()#commit to commit the query

    #cur.execute("DROP TABLE IF EXISTS supplier")
    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,"
                "name TEXT,contact TEXT,description TEXT)")
    con.commit()  # commit to commit the query

    # cur.execute("DROP TABLE IF EXISTS category")
    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT)")
    con.commit()  # commit to commit the query

    # cur.execute("DROP TABLE IF EXISTS supplier")
    cur.execute("CREATE TABLE IF NOT EXISTS products(pid INTEGER PRIMARY KEY AUTOINCREMENT,"
                "product TEXT UNIQUE,category TEXT ,supplier TEXT,price TEXT,quantity TEXT,status TEXT)")
    con.commit()  # commit to commit the query

    #cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE IF NOT EXISTS users(uid INTEGER PRIMARY KEY AUTOINCREMENT,"
                "fname TEXT, lname TEXT, contact INT UNIQUE, email TEXT UNIQUE, securityque VARCHAR(100), securityans TEXT,"
                "username TEXT UNIQUE, password TEXT)")
    con.commit()  # commit to commit the query


if __name__=="__main__":
    create_db()
