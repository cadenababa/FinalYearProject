from flask import (Blueprint, 
                request, 
                render_template,
                jsonify
                )
from flask_login import (login_required,
                    current_user
                    )

from utils import *
from base64 import b64decode
from models import *
import xlrd
from time import time
from os import remove

routes = Blueprint('routes', __name__)


@routes.get('/dashboard')
@login_required
def dashboard_get():
    if current_user.is_teacher:
        return render_template("teacher/dashboard.html")
    else:
        return render_template("student/dashboard.html", create_roll=create_roll)

@routes.get('/course')
@login_required
def course_get():
    student = current_user.student
    # course_stream = Course.stream
    av_course = Course.query.filter_by(semester=student.semester).all()
    o_course = None
    for course in av_course:
        if course.stream.lower() == student.department.lower():
            o_course = course
        print(o_course.subject)
    return render_template("student/course.html", course=o_course)

@routes.post("/student-profile-pic-upload")
@login_required
def image_upload_post():
    image_enc_data = request.get_json().get("image_enc_data").split(",")[1]
    with open(f"static/uploads/{current_user.email}.jpg", "wb") as f:
        f.write(b64decode(image_enc_data))
        student = Student.query.get(current_user.student.id)
        student.profile_image = f"static/uploads/{current_user.email}.jpg"
        db.session.commit()
        return jsonify(message="image added successfully", status=True), 200

@routes.get("/student-routine")
@login_required
def student_routine_get():
    semester = request.args.get("semester")
    department = request.args.get("department")
    routine = Routines.query.filter(Routines.department == department, Routines.semester == semester).first()
    return

# @routes.post("student-routine")
# @login_required
# def student_routine_post():
#     image_enc_data = request.get_json().get("image_enc_data").split(",")[1]
#     with open(f"static/uploads/{current_user.email}.jpg", "wb") as f:
#         f.write(b64decode(image_enc_data))
#         student = Student.query.get(current_user.student.id)
#         student.profile_image = f"static/uploads/{current_user.email}.jpg"
#         db.session.commit()
#         return jsonify(message="image added successfully", status=True), 200

@routes.post("/add-ca-marks-from-teacher")
# @login_required
def add_ca_marks_from_teacher_post():
    flag:bool = False
    excel_enc_data = request.get_json().get("excel_enc_data").split(",")[1]

    filename = f"{str(time())}.xlsx"

    with open(f"static/temp/{filename}", "wb") as f:
        f.write(b64decode(excel_enc_data))

    try: xlrd.open_workbook(f"static/temp/{filename}")
    except:
        new_filename = xlsx_to_xls(f"static/temp/{filename}")
        print (new_filename)
        xlrd.open_workbook(new_filename)

    sheet = xlrd.sheet_by_index(0)

    db_header = ["Student_University_Roll", "Subject", "ca1", "ca2", "ca3", "ca4"]
    excel_header:list = sheet.row_values(0)

    if not excel_header == db_header:
        return jsonify(message="Invalid excel sheet", status=False)

    for i in range(1, sheet.nrows):
        excel_student:list = sheet.row_values(i)
        excel_student_u_roll = excel_student[0]
        excel_student_subject = excel_student[1]
        excel_student_ca1 = excel_student[2]
        excel_student_ca2 = excel_student[3]
        excel_student_ca3 = excel_student[4]
        excel_student_ca4 = excel_student[5]

        student = Student.query.filter_by(university_roll=excel_student_u_roll).first()
        
        if student is not None:
            if student.ca_marks is None:
                new_mark = CAMarks(ca1=excel_student_ca1,
                                ca2 = excel_student_ca2,
                                ca3 = excel_student_ca3,
                                ca4 = excel_student_ca4,
                                subject = excel_student_subject,
                                student=student)
                db.session.add(new_mark)

            elif student.ca_marks is not None:
                for ca_mark in student.ca_marks:
                    if ca_mark.subject == excel_student_subject:
                        ca_mark.ca1 = excel_student_ca1
                        ca_mark.ca2 = excel_student_ca2
                        ca_mark.ca3 = excel_student_ca3
                        ca_mark.ca4 = excel_student_ca4
                        flag = True
                if not flag:
                    new_mark = CAMarks(ca1=excel_student_ca1,
                            ca2 = excel_student_ca2,
                            ca3 = excel_student_ca3,
                            ca4 = excel_student_ca4,
                            subject = excel_student_subject,
                            student=student)
                    db.session.add(new_mark)

        else:
            return jsonify(message="invalid student university roll number present", status=False)
        
    db.session.commit()
    remove("static/temp/"+filename)
    return jsonify(message="successfully added CAMarks from excel sheet.", status=True)