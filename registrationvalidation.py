from flask import Flask, request,jsonify,session
import json
from flask_mysqldb import MySQL 
import pymysql
import re


app=Flask(__name__)


def db_connection():    

    conn=None

    try:
        conn=pymysql.connect(   host='sql12.freemysqlhosting.net',
                                database='sql12375682',
                                user='sql12375682',
                                password='nL9hwqHpV7',
                                cursorclass=pymysql.cursors.DictCursor
                            )
    except pymysql.Error as e :
        print(e)    
    return conn   


def exe_quer(conn,cursor):
    conn=db_connection()
    cursor=conn.cursor()
    return conn,cursor

    
def validation(new_fname,new_lname):
    if not re.match  (r'[A-Za-z]+',new_fname):
        return "only string first name",400
    if not re.match  (r'[A-Za-z]+',new_lname):
        return "only string last name",400

@app.route("/signup",methods=["POST"])
def signup():
    a,b=exe_quer('conn','cursor')
    

   
    new_fname=request.form['fname']
    new_lname=request.form['lname']
    new_password=request.form['password']  
    new_email  =request.form['email'] 
    new_mobileno=request.form['mobileno']
    c,d=validation('new_fname','new_lname')
    if new_fname and new_lname and new_password and new_email and new_mobileno and  request.method=="POST" :
        
        b.execute('SELECT * FROM login WHERE fname=%s' ,(new_fname,))
            
        acc=b.fetchone()
        if acc:
            return "Account already exist!"            
        elif not re.match  (r'[^@]+@[^@]+\.[^@]+',new_email):   
            return "Invalid Email address " ,400 
        elif new_fname:    
            return c
        elif new_lname:    
            return d
        
        elif not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),new_mobileno):    
            return "Mobile no must contain only numbers",400    
        
        else:
            sq="""INSERT INTO login (fname,lname,password,email,mobileno) 
                            VALUES (%s,%s,%s,%s,%s)"""
                                
            b.execute(sq,(new_fname,new_lname,new_password,new_email,new_mobileno))
            a.commit()
            return "You have successfully registered" ,201            
    elif not new_fname  or not new_lname or not new_email or not new_mobileno or not new_password:
        return "pls enter all the details" ,400        
                            
                         


              
        
@app.route('/signin',methods=["POST","DELETE"])
def signin():
        a,b=exe_quer('conn','cursor')

        
        
        if request.method == 'POST':
            new_email  =request.form['email'] 
            new_password=request.form['password']  
        
            se="""SELECT * FROM login WHERE email=%s AND password=%s"""
            b.execute(se,(new_email,new_password))
            account=b.fetchone()
            a.commit()
            
            if account:
                
                new_email=account['new_email']
                new_password=account['new_password']
                return 'Logged in successfully!',202
                
                
            else:
                return "Enter correct email or password ",401

        if request.method=='DELETE': 
            new_email  =request.form['email'] 
            new_password=request.form['password'] 
            sql_del="""DELETE FROM login WHERE email=%s AND password=%s """ 
            b=b.execute(sql_del,(new_email,new_password,))
            a.commit()
            return "The email id: {} and password : {}   has been deleted  successfully!. ".format(new_email,new_password),200
        return "Please enter correct email or password ",401     

if __name__=='__main__':
    app.run(debug=True)

