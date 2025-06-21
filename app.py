print("📦 app.py is being executed")

from flask import Flask, render_template, request, redirect, flash
from sheets import append_task, get_tasks
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form['task'].strip()
        description = request.form['description'].strip()
        due_date = request.form['due_date'].strip()
        status = request.form['status'].strip()

        if not task or not status:
            flash('❌ Task and Status are required.')
            return redirect('/')

        append_task(task, description, due_date, status)
        flash('✅ Task submitted successfully!')
        return redirect('/')

    tasks = get_tasks()

    # 🧠 Filter by status or due_date
    filter_status = request.args.get('status')
    if filter_status:
        tasks = [row for row in tasks if len(row) > 3 and row[3] == filter_status]

    return render_template('index.html', tasks=tasks, filter_status=filter_status)

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(debug=True)
