from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from utils import generate_employee_id

db = SQLAlchemy()


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    occupation = db.Column(db.String(15))
    student = db.relationship("Student", backref="user", uselist=False)
    teacher = db.relationship("Teacher", backref="user", uselist=False)

    @property
    def is_teacher(self) -> bool:
        if self.occupation == "teacher":
            return True
        else:
            return False

    @property
    def is_student(self) -> bool:
        if self.occupation == "student":
            return True
        else:
            return False

    def set_password(self, new_password):
        self.password = generate_password_hash(new_password)
        db.session.commit()

    def __repr__(self):
        if self.is_teacher:
            return f'"{self.teacher.name}"--ptr-user-<{self.id}>'
        else:
            return f'"{self.student.name}"--ptr-user-<{self.id}>'

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    department = db.Column(db.String(80))
    university_roll = db.Column(db.String(15), unique=True)
    class_role = db.Column(db.String(15))
    semester = db.Column(db.String(15))
    mobile = db.Column(db.String(15))
    dob = db.Column(db.DateTime, nullable=False)
    batch = db.Column(db.Integer, nullable=False)
    profile_image = db.Column(db.String(255), default="https://www.w3schools.com/howto/img_avatar.png")
    ca_marks = db.relationship("CAMarks", backref="student", uselist=True)
    user_ptr_id  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    def __repr__(self):
        return f"<{self.university_roll} {self.name}>"


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, unique=True, default=generate_employee_id)
    name = db.Column(db.String(80))
    department = db.Column(db.String(80))
    mobile = db.Column(db.String(15))
    profile_image = db.Column(db.String(255), default="https://www.w3schools.com/howto/img_avatar.png")
    user_ptr_id  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    subject = db.relationship("Subject", backref="teacher", uselist=True)

    # def __init__(self, *args, **kwargs):
        

    def __repr__(self):
        return f"{self.name} <{self.emp_id}>"


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    teacher_ptr_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))
    course_ptr_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    ca_marks_ptr_id = db.Column(db.Integer, db.ForeignKey('ca_marks.id'), unique=True)
    # notes_ptr_id = db.Column(db.Integer, db.ForeignKey('notes.id'))

    def __repr__(self):
        return self.name
    
# subject_course_con = db.Table("group_user_con", 
#                     db.Column('subject_id', db.Integer, db.ForeignKey("subject.id")),
#                     db.Column('course_id', db.Integer, db.ForeignKey("course.id"))
#                     )

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    stream = db.Column(db.String(80))
    semester = db.Column(db.Integer, nullable=False)
    # subject = db.Column(db.String(80))
    subject = db.relationship("Subject", backref="courses", uselist=True)

    def __repr__(self):
        return self.name

class Routines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(80))
    semester = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255))
    

class CAMarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ca1 = db.Column(db.Integer, default=0)
    ca2 = db.Column(db.Integer, default=0)
    ca3 = db.Column(db.Integer, default=0)
    ca4 = db.Column(db.Integer, default=0)
    subject = db.relationship("Subject", backref="ca_marks", uselist=False)
    student_ptr_id = db.Column(db.Integer, db.ForeignKey("student.id"))

# class Notes(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     semester = db.Column(db.String(80), nullable=False)
#     department = db.Column(db.String(80), nullable=False)
#     subject = db.relationship("Subject", backref="notes", uselist=True)
#     teacher = db.relationship("Teacher", backref="notes", uselist=True)
