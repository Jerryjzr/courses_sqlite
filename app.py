from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def show_courses():
    conn = sqlite3.connect('course.db')
    c = conn.cursor()
    c.execute("SELECT * FROM courses")
    courses = c.fetchall()
    conn.close()
    return render_template('show_courses.html', courses=courses)

@app.route('/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['course_name']
        teacher = request.form['teacher']
        time = request.form['time']
        location = request.form['location']
        conn = sqlite3.connect('course.db')
        c = conn.cursor()
        c.execute("INSERT INTO courses (course_name, teacher, time, location) VALUES (?, ?, ?, ?)",
                  (course_name, teacher, time, location))
        conn.commit()
        conn.close()
        return redirect(url_for('show_courses'))
    else:
        return render_template('add_course.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    if request.method == 'POST':
        course_name = request.form['course_name']
        teacher = request.form['teacher']
        time = request.form['time']
        location = request.form['location']
        conn = sqlite3.connect('course.db')
        c = conn.cursor()
        c.execute("UPDATE courses SET course_name=?, teacher=?, time=?, location=? WHERE id=?",
                  (course_name, teacher, time, location, id))
        conn.commit()
        conn.close()
        return redirect(url_for('show_courses'))
    else:
        conn = sqlite3.connect('course.db')
        c = conn.cursor()
        c.execute("SELECT * FROM courses WHERE id=?", (id,))
        course = c.fetchone()
        conn.close()
        return render_template('edit_course.html', course=course)

@app.route('/delete/<int:id>')
def delete_course(id):
    conn = sqlite3.connect('course.db')
    c = conn.cursor()
    c.execute("DELETE FROM courses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('show_courses'))

if __name__ == '__main__':
    app.run(debug=True)