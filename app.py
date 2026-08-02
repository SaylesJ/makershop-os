import os
from flask import send_file, flash

@app.route('/backup')
def download_backup():
    # Sends the current SQLite database file straight to your browser as a download
    if os.path.exists(DB_NAME):
        return send_file(DB_NAME, as_attachment=True, download_name='whittlewoodys_backup.db')
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
        # Overwrite the active database with the uploaded backup file
        file.save(DB_NAME)
        return redirect(url_for('settings'))