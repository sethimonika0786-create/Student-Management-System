from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)



# Student Model
class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100))

    course = db.Column(db.String(100))





# Dashboard
@app.route("/")
def home():

    total_students = Student.query.count()

    return render_template(
        "index.html",
        total_students=total_students
    )





# Add Student
@app.route("/add", methods=["GET","POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        course = request.form["course"]


        student = Student(

            name=name,

            email=email,

            course=course

        )


        db.session.add(student)

        db.session.commit()


        return redirect("/students")


    return render_template("add.html")






# Students List + Search
@app.route("/students")
def students():

    search = request.args.get("search")


    if search:

        all_students = Student.query.filter(
            Student.name.contains(search)
        ).all()


    else:

        all_students = Student.query.all()



    return render_template(

        "students.html",

        students=all_students

    )






# View Student
@app.route("/view/<int:id>")
def view_student(id):

    student = Student.query.get(id)

    return render_template(

        "view.html",

        student=student

    )







# Delete Student
@app.route("/delete/<int:id>")
def delete_student(id):

    student = Student.query.get(id)


    db.session.delete(student)

    db.session.commit()


    return redirect("/students")







# Edit Student
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit_student(id):

    student = Student.query.get(id)


    if request.method == "POST":


        student.name = request.form["name"]

        student.email = request.form["email"]

        student.course = request.form["course"]



        db.session.commit()


        return redirect("/students")



    return render_template(

        "edit.html",

        student=student

    )






if __name__ == "__main__":


    with app.app_context():

        db.create_all()


    app.run(debug=True)