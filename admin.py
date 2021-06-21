from flask_admin import Admin
from models import *
from flask_admin.contrib.sqla import ModelView

admin = Admin(name='RCC Admin', template_mode='bootstrap4')

admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Subject, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(CAMarks, db.session))
admin.add_view(ModelView(Notes, db.session))