# courses_sqlite
一个借助chatgpt使用python配合sqlite开发的较为简陋的web课程表
首先，需要安装sqlite3和flask库。

创建数据库表：

python

import sqlite3

conn = sqlite3.connect('course.db')
c = conn.cursor()

c.execute('''CREATE TABLE courses
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             course_name TEXT NOT NULL,
             teacher TEXT NOT NULL,
             time TEXT NOT NULL,
             location TEXT NOT NULL)''')

conn.commit()
conn.close()
接下来，创建一个Flask应用程序，包括以下路由：

/：显示课程表
/add：添加课程
/edit/int:id：编辑课程
/delete/int:id：删除课程
python

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
在templates文件夹中创建以下HTML模板：

show_courses.html：

html

<!DOCTYPE html>
<html>
<head>
    <title>课程表</title>
</head>
<body>
    <h1>课程表</h1>
    <table>
        <tr>
            <th>课程名称</th>
            <th>教师</th>
            <th>时间</th>
            <th>地点</th>
            <th>操作</th>
        </tr>
        {% for course in courses %}
        <tr>
            <td>{{ course[1] }}</td>
            <td>{{ course[2] }}</td>
            <td>{{ course[3] }}</td>
            <td>{{ course[4] }}</td>
            <td>
                <a href="{{ url_for('edit_course', id=course[0]) }}">编辑</a>
                <a href="{{ url_for('delete_course', id=course[0]) }}">删除</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    <a href="{{ url_for('add_course') }}">添加课程</a>
</body>
</html>
add_course.html：

html

<!DOCTYPE html>
<html>
<head>
    <title>添加课程</title>
</head>
<body>
    <h1>添加课程</h1>
    <form method="post">
        <label>课程名称：</label>
        <input type="text" name="course_name"><br>
        <label>教师：</label>
        <input type="text" name="teacher"><br>
        <label>时间：</label>
        <input type="text" name="time"><br>
        <label>地点：</label>
        <input type="text" name="location"><br>
        <input type="submit" value="添加">
    </form>
</body>
</html>
edit_course.html：

html

<!DOCTYPE html>
<html>
<head>
    <title>编辑课程</title>
</head>
<body>
    <h1>编辑课程</h1>
    <form method="post">
        <label>课程名称：</label>
        <input type="text" name="course_name" value="{{ course[1] }}"><br>
        <label>教师：</label>
        <input type="text" name="teacher" value="{{ course[2] }}"><br>
        <label>时间：</label>
        <input type="text" name="time" value="{{ course[3] }}"><br>
        <label>地点：</label>
        <input type="text" name="location" value="{{ course[4] }}"><br>
        <input type="submit" value="保存">
    </form>
</body>
</html>
最后，运行应用程序：

SQL

python app.py
在浏览器中访问http://localhost:5000/即可查看课程表，点击“添加课程”按钮可以添加课程，点击“编辑”按钮可以编辑课程，点击“删除”按钮可以删除课程。
