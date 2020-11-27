import pymysql

conn=pymysql.connect(
                    host='sql12.freemysqlhosting.net',
                    database='sql12375682',
                    user='sql12375682',
                    password='nL9hwqHpV7',
                    cursorclass=pymysql.cursors.DictCursor
                    )  

cursor=conn.cursor()
query="""CREATE TABLE IF NOT EXISTS login(id integer AUTO_INCREMENT PRIMARY KEY,
                         fname VARCHAR(10) NOT NULL,
                         lname VARCHAR(10) NOT NULL,
                         password   INT NOT NULL,
                         email  VARCHAR(15) NOT NULL,
                         mobileno BIGINT NOT NULL 
) """                          

cursor.execute(query)       
conn.close()             
                
                
             