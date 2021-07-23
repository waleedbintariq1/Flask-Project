from logging import NullHandler, debug
from sys import meta_path
from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'fyp'

app.config['UPLOAD_FOLDER'] = "K:\Study\Semester 8\FYP 2\Flask Project\outputImages"

mysql = MySQL(app)

class doctor:
    email = ""
    firstName = ""
    lastName = ""
    password = ""

class patient:
    email = ""
    firstName = ""
    lastName = ""
    xrayPath = ""
    disease = ""
    doctorEmail = ""

d = doctor()


@app.route('/', methods=['GET', 'POST'])
def mainPage():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":      
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        email = details['email']
        password = details['password']
        cur = mysql.connection.cursor()

        # first argument is query
        # second argument is data
        cur.execute("INSERT INTO doctors values (%s, %s, %s, %s)", [email, firstName, lastName, password])
        mysql.connection.commit()
        cur.close()

    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        details = request.form
        email = details['email']
        password = details['password']
        cur = mysql.connection.cursor()

        # first argument is query
        # second argument is data
        rowsReturned = cur.execute("SELECT * FROM doctors WHERE email = %s AND password = %s", [email, password])
        data = cur.fetchone()

        d.email = data[0]
        d.firstName = data[1]
        d.lastName = data[2]
        d.password = data[3]

        mysql.connection.commit()
        cur.close()

        if rowsReturned >= 1:
            return redirect("/homepage")
        
    return render_template("login.html")

@app.route('/homepage', methods=["GET", "POST"])
def homepage():
    return render_template("homepage.html", doctor=d)

@app.route('/newPatient', methods=['GET', 'POST'])
def newPatient():
    if request.method == "POST":
        details = request.form
        email = details['email']
        firstName = details['fname']
        lastName = details['lname']
        doctorEmail = d.email

        if "img" not in request.files:
            return "image not uploaded!"
        
        xrayImage = request.files['img']
        filename = xrayImage.filename

        xrayPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        print("xray path: " + xrayPath)

        xrayImage.save(xrayPath)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patients values (%s, %s, %s, %s, %s, %s)", [email, firstName, lastName, xrayPath, "COVID-19", doctorEmail])
        
        mysql.connection.commit()
        cur.close()

    return render_template("newPatient.html")

@app.route('/results', methods=['GET', 'POST'])
def results():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patients WHERE doctorEmail = %s", [d.email])
    results = cur.fetchall()

    patientList = []

    for row in results:
        p = patient()
        p.email = row[0]
        p.firstName = row[1]
        p.lastName = row[2]
        p.xrayPath = row[3]
        p.disease = row[4]
        patientList.append(p)
    
    mysql.connection.commit()
    cur.close()


    return render_template("results.html", patientList=patientList)

@app.route('/deletePatient', methods=["GET", "POST"])
def deletePatient():
    if request.method == 'POST':
        cur = mysql.connection.cursor()

        patientEmailList = request.form.getlist("checkbox")

      

        for patientEmail in patientEmailList:
            cur.execute("SELECT * FROM patients WHERE email = %s", [patientEmail])
            result = cur.fetchone()

            # deleting xray image
            xrayPath = result[3]
            os.remove(xrayPath)

            cur.execute("DELETE FROM patients WHERE email = %s", [patientEmail])
            mysql.connection.commit()

        cur.close()
    
    return render_template('deletePatient.html', emailList=patientEmailList)

if __name__ == "__main__":
    app.run(debug=True)
