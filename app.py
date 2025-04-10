### Mohammad Bayuomi 
from flask import Flask , request , render_template , url_for , Request , flash , redirect , get_flashed_messages
from flask_wtf import FlaskForm 
import sqlite3
import os
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import input_required , length , ValidationError
from pymongo import MongoClient
#from flask_sqlalchemy import SQLAlchemy 
#from flask_login import UserMixin 

from flask_bcrypt import Bcrypt

client =MongoClient('mongodb://localhost:27017')
db = client['Resturants_Info']
collections = db['Resturants']

##all_collection = collection.find()
## just to test the connection with mongoDB
# for x in all_collection:
#     print(x)

app = Flask(__name__)
#db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'Youare_not_allowed'
bcrypt = Bcrypt


#
#   Connecting the code to the database
import sqlite3 ## To create the conniction between database & the code

##conn=sqlite3.Connection("database.db")
location=os.path

## To call the pages
@app.route('/') ## Name of the page
def home():
        return render_template("Home.html" )

@app.route('/' , methods=["POST" , "GET"])
def login():
    if request.method=="POST":
       
        try:
             userlog= request.form['username']
             pwd= request.form['password']
             conn=sqlite3.Connection("database.db")
             cursor = conn.cursor()
             query1='SELECT Username, Passwords FROM users_data WHERE Username = ? AND Passwords = ?' 
             rows =cursor.execute(query1 ,(userlog , pwd))
             rows=rows.fetchall()
             if len(rows)==1:
                
                 flash('You logged in successfuly' , category='success')
                #  return render_template("search.html" , messages=messages )
                 return redirect('/Search')

             else:##massage flash
                  
                  flash("You do not have an account or you entered wrong password" , category="error")
                #   return render_template("Home.html", messages=messages )
                  return redirect('/')
        except Exception as e:
                  
                  flash("You do not have an account or you entered wrong password" , category="error")
                #   return render_template("Home.html", messages=messages )
                  return redirect('/')
    else :
      flash("You do not have an account or you entered wrong password" , category="error")
    # return render_template("Home.html", messages=messages )
      return redirect(url_for('/'))
         
####        
@app.route('/Register')
def Register():
       return render_template("register.html" )

@app.route('/Register' , methods=["POST" , "GET"])
def Signup():
    
    if request.method=="POST":
        try:
            
            new_user = request.form['username']
            pwd = request.form['password']
            conn =sqlite3.Connection("database.db")
            cursor=conn.cursor()
           
            cursor.execute("INSERT INTO users_data VALUES (? , ?)" , [new_user , pwd])
            conn.commit()
            conn.close()
            flash("You have created an account successfuly " ,category='success' )
            return redirect('/')
        except Exception as e:
             ## Then write Flash
            # messages = get_flashed_messages(with_categories=True)
            flash("This username already exists " , category='error')
            return redirect('/Register')
    else :
            # messages = get_flashed_messages(with_categories=True)
            flash("This username already exists " , category='error')
            return redirect('/Register')
         
          
####
@app.route('/Search')
def enter():
      
      return render_template("search.html")
     
@app.route('/Search' , methods=["GET " , "POST"])
def searching():
      if request.method == "POST":
        try :
          resturant_name =request.form['restaurant']
          
          all_names = collections.find({'borough': resturant_name})
        
          restaurants = list(all_names)
         

          return render_template("search.html" , restaurants=restaurants)
          
        except Exception as e :
            flash("This resturant does not exist" , category='error')
            return redirect('/Search')

    
        else :
            return redirect('/Search')
            

if __name__=='__main__':
    app.run(debug=True)