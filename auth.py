# from threading import current_thread
from flask import Blueprint, render_template, request, session, logging, url_for, redirect, flash
from models import Student, Teacher, Users,  db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.get("/")
def home():
	return render_template("auth.html")


@auth.route("/register_student", methods=["POST"])
def register_post_student():
    if request.method == "POST":
        name = request.form.get("form_name")
        email = request.form.get("form_email")
        univroll = request.form.get("form_univ_roll")
        classroll = request.form.get("form_class_roll")
        sem = request.form.get("form_sem")
        mobno = request.form.get("form_mob_no")
        password1 = request.form.get("form_passw")
        password2 = request.form.get("form_conf_passw")
        dob = request.form.get("dateofbirth")

        if Users.query.filter_by(email=email).first():
            flash('Email id already exists! Try a new email id','danger')
            return redirect("/")

        if Student.query.filter_by(university_roll=univroll).first():
            flash('University Roll Number already exists! Try a new email id','danger')
            return redirect("/")

        if not password1 == password2:
            flash("Password does not match","danger")
            return redirect("/")
        
        user = Users(email=email, 
                    password=generate_password_hash(password1), 
                    occupation = "student"
                    )
        db.session.add(user)
        n_classroll = int(classroll.rsplit("/", 1)[1])
        dept = classroll.rsplit("/", 1)[0][:-4]
        batch = classroll.rsplit("/", 1)[0][len(dept):]
        student = Student(name = name, 
                        department = dept, 
                        university_roll = univroll, 
                        class_role = n_classroll, 
                        semester = sem, 
                        mobile = mobno,
                        batch=batch,
                        dob =  datetime.strptime(dob, '%Y-%m-%d'),
                        user = user
                        )
        db.session.add(student)
        db.session.commit()
        return render_template("registrationsuccess.html")


@auth.route("/register_teacher", methods=["POST"])
def register_post_teacher():
    if request.method == "POST":
        name = request.form.get("teacher_name")
        email = request.form.get("teacher_email")
        dept = request.form.get("teacher_dept")
        passw1 = request.form.get("teacher_passw")
        passw2 = request.form.get("teacher_passw_conf")

        if Users.query.filter_by(email=email).first():
            flash('Email id already exists! Try a new email id','danger')
            return render_template("auth.html")
        if not passw1 == passw2:
            flash("Password does not match","danger")
            return render_template("auth.html")

        user = Users(email=email, 
                    password=generate_password_hash(passw1), 
                    occupation = "teacher"
                    )
        db.session.add(user)
        teacher = Teacher(name = name,  
                department = dept, 
                user=user
                )
        db.session.add(teacher)
        db.session.commit()
        return render_template("registrationsuccess.html")

@auth.route("/login", methods=["POST"])
def loginuser():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    if request.method == "POST":
        email = request.form.get("form-username")
        password = request.form.get("form-password")
        user = Users.query.filter_by(email=email).first()
        if not user:
            flash('Email id does not exist!! Please check your login details and try again.','danger')
            return render_template("auth.html")
        if not check_password_hash(user.password, password):
            flash('Incorrect password!! Please check your login details and try again.','danger')
            return render_template("auth.html")

        login_user(user)
        return redirect('/dashboard')     

@auth.get("/logout")
@login_required
def logout_get():
    flash("successfully logged out", "success")  
    logout_user()
    return redirect('/') 

@auth.get("/change-password")
@login_required
def change_password_get():
    return
    return render_template("")

@auth.post("/change-password")
@login_required
def change_password_post():
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_new_password = request.form.get("confirm_new_password")
    if not new_password == confirm_new_password:
        flash("password mismatch", "error")
    if not check_password_hash(current_user.password, current_password):
        flash("invalid current password", "error")
    current_user.set_password(new_password)
    return render_template("")