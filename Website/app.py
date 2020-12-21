"""
import pyodbc
server = 'harshita11.database.windows.net'
database = 'AirlineBooking'
username = 'harshita'
password = '2048035Db'   
driver= '{ODBC Driver 17 for SQL Server}'
with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Flight")
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()
"""



from flask import Flask, request, render_template
import pyodbc

app = Flask(__name__) #creating the Flask class object   
 
server = 'harshita11.database.windows.net'
database = 'AirlineBooking'
username = 'harshita'
password = '2048035Db'   
driver= '{ODBC Driver 17 for SQL Server}'
 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

@app.route("/")  
def indexPage():
    return render_template("index.html")

@app.route("/contactPage", methods=['POST', 'GET'])  
def contactPage(): 
    if request.method == "POST":
        nme = request.form['name']
        eml = request.form['email']
        msg = request.form['message']
        with cnxn as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO Contact(name, email, message) VALUES (?, ?, ?)", (nme, eml, msg))
                #det = cursor.fetchall()
            return render_template("contact.html")
    else:
        return render_template('contact.html')  

@app.route("/showFlights", methods=['POST', 'GET'])
def showFlights():
    if request.method == "POST":
        src = request.form['source']
        dest = request.form['destination']
        
        with cnxn as conn:
            with conn.cursor() as cursor:
                cursor.execute( "SELECT * FROM flight WHERE source = '" + src + "' AND destination = '" + dest +"'")
                data = cursor.fetchall()
            return render_template("showFlights.html", data=data)
    else:
        return render_template("index.html")

@app.route("/bookingInfo")
def bookingInfo():
    return render_template('bookingInfo.html')
    
@app.route("/bookingInfoResult", methods=['POST', 'GET'])
def bookingInfoResult():
    if request.method == "POST":
        pn = request.form['pnr']
        with cnxn as conn:
            with conn.cursor() as cursor:
                cursor.execute( "SELECT * FROM Ticket WHERE PNR = '" + pn + "'")
                data1 = cursor.fetchall()
            return render_template('bookingInfoResult.html', data1=data1)
    else:
        return render_template('bookingInfo.html')

if __name__ == '__main__':
    app.debug = True
    app.run()