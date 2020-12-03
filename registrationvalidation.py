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

    
def validation(new_fname,new_lname,new_password,new_email,new_mobileno):
    if not new_fname or not new_lname or not new_password or not new_email or not new_mobileno :
        return "Please enter all values"
    if not re.match  (r'[A-Za-z]+',new_fname):
        return "First name only string."
    elif not re.match  (r'[A-Za-z]+',new_lname):
        return "Last name only string"
    elif not re.match  (r'[A-Za-z0-9]+',new_password):
        return "Passwod name only string"
    elif not re.match  (r'[^@]+@[^@]+\.[^@]+',new_email):   
        return "Invalid Email address " 
    elif not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),new_mobileno):    
        return"Mobile no must contain only numbers"        

    return ''

def select(new_email,new_password):
   
    a,b=exe_quer('conn','cursor') 
    se="""SELECT * FROM login WHERE email=%s AND password=%s"""
    b.execute(se,(new_email,new_password))
    account=b.fetchone()
    a.commit()
    return account
    

    
@app.route("/signup",methods=['POST'])
def signup():
    if request.method!="POST" :
        return jsonify({"message":"only post method is  allowed"}),400
              
   
    
    new_fname=request.form['fname']
    new_lname=request.form['lname']
    new_password=request.form['password'] 
    new_email  =request.form['email'] 
    new_mobileno=request.form['mobileno']
    

    error_msg=validation(new_fname,new_lname,new_password,new_email,new_mobileno)
    if error_msg:
        return jsonify({"message":error_msg}),400
       
    a,b=exe_quer('conn','cursor')    
    b.execute('SELECT * FROM login WHERE fname=%s' ,(new_fname,))      
    acc=b.fetchone()
    if acc:
        return jsonify({"message":"Account already exist!"}),200             
    else:
        sq="""INSERT INTO login (fname,lname,password,email,mobileno) 
                        VALUES (%s,%s,%s,%s,%s)"""
                            
        b.execute(sq,(new_fname,new_lname,new_password,new_email,new_mobileno))
        a.commit()
        return jsonify({"message":"You have successfully registered"}) ,201            
        
        
@app.route('/signin',methods=["POST","DELETE"])
def signin():
        a,b=exe_quer('conn','cursor')
        new_email  =request.form['email'] 
        new_password=request.form['password'] 

        val=select(new_email,new_password)

        if request.method == 'POST':
                      
            if val:
                return jsonify({"message":"Logged in successfully!"}),202            
              
            else:
                return jsonify({"message":"Enter correct email or password"}),401

        if request.method=='DELETE': 
            
            if val:
                sql_del="""DELETE FROM login WHERE email=%s AND password=%s """ 
                b.execute(sql_del,(new_email,new_password,))
                a.commit()
            
                return jsonify({"message":"You account  has been deleted  successfully!."}),200
            else:    
                return jsonify({"message":"Please enter correct email or password "}),401     

if __name__=='__main__':
    app.run(debug=True)

          