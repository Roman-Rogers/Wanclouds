from flask import Flask, request
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    priority = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.priority = False

    def __repr__(self):
        return '<Content %s>' % self.content


db.create_all()


@app.route('/')
def tasks_list():
    tasks = Task.query.all()
    return render_template('list.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'No data entered'

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get(task_id)
    
    newcontent = request.form['content']
    if not newcontent:
        return 'No data entered'
    task.content=newcontent

    db.session.commit()
    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/')


@app.route('/priority/<int:task_id>')
def prioritize_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/')
    if task.priority:
        task.priority = False
    else:
        task.priority = True

    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
