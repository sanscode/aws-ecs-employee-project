from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


import os, urllib

app = Flask(__name__)


DBHOST = os.environ.get("DB_HOST")
DBPORT = os.environ.get("DB_PORT")
DBUSER = os.environ.get("DB_USERNAME")
DBPWD = os.environ.get("DB_PASSWORD")
DATABASE = os.environ.get("DB_NAME")

DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus(DBPWD)

# MySQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DBUSER}:{DATABASE_PASSWORD_UPDATED}@{DBHOST}:{DBPORT}/{DATABASE}'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://admin:Test@123456@localhost/employeedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Example Model
class Employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80),nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    pri_skill = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"<Todo {self.emp_id}>"


# # Create tables (run this once)
# def init_db():
#     with app.app_context():
#         db.create_all()


@app.route("/getemp", methods=['GET','POST'])
def get_employee_info():
    return render_template('getemp.html')

@app.route("/findemp", methods=['GET', 'POST'])
def find_employee():

    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    print(emp_id)

    try:
        employee_details = Employee.query.get_or_404(emp_id)
        print(employee_details)       
       

        return render_template("getempoutput.html",id=employee_details.emp_id,fname=employee_details.first_name,
                               lname=employee_details.last_name,interest=employee_details.pri_skill,location=employee_details.location)
    

    except Exception as e:
        print(e)
        return render_template("error.html",error="Employee Not Found")

if (__name__) == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


    
