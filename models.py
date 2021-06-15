from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

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

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    department = db.Column(db.String(80))
    university_roll = db.Column(db.String(15))
    class_role = db.Column(db.String(15))
    semester = db.Column(db.String(15))
    mobile = db.Column(db.String(15))
    dob = db.Column(db.DateTime, nullable=False)
    user_ptr_id  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    department = db.Column(db.String(80))
    user_ptr_id  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)