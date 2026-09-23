import os
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ.get("DB_PASSWORD", "password"),  
    database="banking_system"
)

@app.route('/')
def home():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()
    cursor.close()
    return render_template('index.html', customers=customers)

@app.route('/customer/<int:id>')
def customer(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Customers WHERE id = %s", (id,))
    customer = cursor.fetchone()
    cursor.close()
    return render_template('customer.html', customer=customer)

@app.route('/transfer', methods=['POST'])
def transfer():
    sender_id = request.form['sender_id']
    receiver_id = request.form['receiver_id']
    amount = float(request.form['amount'])

    cursor = db.cursor()
    cursor.execute("UPDATE Customers SET current_balance = current_balance - %s WHERE id = %s", (amount, sender_id))
    cursor.execute("UPDATE Customers SET current_balance = current_balance + %s WHERE id = %s", (amount, receiver_id))
    cursor.execute("INSERT INTO Transfers (sender_id, receiver_id, amount) VALUES (%s, %s, %s)", (sender_id, receiver_id, amount))
    db.commit()
    cursor.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

