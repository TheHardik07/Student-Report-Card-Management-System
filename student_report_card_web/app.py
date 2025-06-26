from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)
FILENAME = 'students.csv'

def load_students():
    students = []
    try:
        with open(FILENAME, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['Python'] = int(row['Python'])
                row['Java Script'] = int(row['Java Script'])
                row['Adv. Java'] = int(row['Adv. Java'])
                students.append(row)
    except FileNotFoundError:
        pass
    return students

def save_students(students):
    with open(FILENAME, 'w', newline='') as csvfile:
        fieldnames = ['Roll', 'Name', 'Python', 'Java Script', 'Adv. Java']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)

@app.route('/')
def index():
    students = load_students()
    for s in students:
        total = s['Python'] + s['Java Script'] + s['Adv. Java']
        avg = total / 3
        s['Total'] = total
        s['Average'] = round(avg, 2)
        s['Grade'] = get_grade(avg)
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        students = load_students()
        new_student = {
            'Roll': request.form['roll'],
            'Name': request.form['name'],
            'Python': int(request.form['python']),
            'Java Script': int(request.form['java_script']),
            'Adv. Java': int(request.form['adv_java'])
        }
        students.append(new_student)
        save_students(students)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<roll>')
def delete(roll):
    students = load_students()
    students = [s for s in students if s['Roll'] != roll]
    save_students(students)
    return redirect(url_for('index'))

def get_grade(avg):
    if avg >= 90:
        return 'A+'
    elif avg >= 75:
        return 'A'
    elif avg >= 60:
        return 'B'
    elif avg >= 50:
        return 'C'
    else:
        return 'Fail'

if __name__ == '__main__':
    app.run(debug=True)
