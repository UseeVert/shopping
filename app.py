from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="shopping_db"
)
cursor = db.cursor()

# Rute untuk landing page
@app.route('/')
def landing():
    return render_template('landing.html')

# Rute untuk halaman manajemen daftar belanjaan
@app.route('/manage')
def manage():
    cursor.execute("SELECT * FROM shopping_list")
    items = cursor.fetchall()
    total = sum(item[4] for item in items)  # Menghitung total dari subtotal
    return render_template('index.html', items=items, total=total)

# Rute untuk menambahkan item
@app.route('/add', methods=['POST'])
def add():
    try:
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        if price <= 0 or quantity <= 0:
            return "Harga dan jumlah harus lebih dari 0", 400

        subtotal = price * quantity
        cursor.execute("INSERT INTO shopping_list (name, price, quantity, subtotal) VALUES (%s, %s, %s, %s)", (name, price, quantity, subtotal))
        db.commit()
        return "Item telah ditambahkan", 200

    except ValueError:
        return "Input tidak valid", 400

# Rute untuk menghapus semua item setelah pembayaran
@app.route('/pay', methods=['POST'])
def pay():
    try:
        amount = float(request.form['amount'])
        cursor.execute("SELECT * FROM shopping_list")
        items = cursor.fetchall()
        total = sum(item[4] for item in items)

        if amount < total:
            return "Jumlah uang tidak mencukupi untuk membayar total", 400

        for item in items:
            name, price, quantity, subtotal = item[1], item[2], item[3], item[4]
            cursor.execute("INSERT INTO shopping_history (name, price, quantity, subtotal) VALUES (%s, %s, %s, %s)", (name, price, quantity, subtotal))

        cursor.execute("DELETE FROM shopping_list")
        db.commit()
        return "Pembayaran berhasil, daftar belanjaan telah direset", 200

    except ValueError:
        return "Jumlah uang tidak valid", 400

if __name__ == '__main__':
    app.run(debug=True)