import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, send_file, flash

app = Flask(__name__)
app.secret_key = 'whittle_woodys_secret_key'
DB_NAME = 'inventory.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS router_bits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            size TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spindles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            is_default INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'filament_name' in request.form:
            f_name = request.form['filament_name']
            cursor.execute('INSERT INTO filaments (name) VALUES (?)', (f_name,))
        elif 'bit_name' in request.form:
            b_name = request.form['bit_name']
            b_size = request.form['bit_size']
            cursor.execute('INSERT INTO router_bits (name, size) VALUES (?, ?)', (b_name, b_size))
        elif 'spindle_name' in request.form:
            s_name = request.form['spindle_name']
            cursor.execute('INSERT INTO spindles (name) VALUES (?)', (s_name,))
        
        conn.commit()

    cursor.execute('SELECT * FROM filaments')
    filaments = cursor.fetchall()
    
    cursor.execute('SELECT * FROM router_bits')
    router_bits = cursor.fetchall()
    
    cursor.execute('SELECT * FROM spindles')
    spindles = cursor.fetchall()
    
    conn.close()

    disclaimer = "Note: If you are not using the DeWalt 611 trim router, please calculate your own speeds and feeds."
    
    return render_template('settings.html', 
                           filaments=filaments, 
                           router_bits=router_bits, 
                           spindles=spindles, 
                           disclaimer=disclaimer)

@app.route('/backup')
def download_backup():
    if os.path.exists(DB_NAME):
        return send_file(DB_NAME, as_attachment=True, download_name='whittle_woodys_backup.db')
    flash('Database file not found!')
    return redirect(url_for('settings'))

@app.route('/restore', methods=['POST'])
def restore_backup():
    if 'backup_file' not in request.files:
        return redirect(url_for('settings'))
    
    file = request.files['backup_file']
    if file.filename == '':
        return redirect(url_for('settings'))
        
    if file:
        file.save(DB_NAME)
        return redirect(url_for('settings'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
