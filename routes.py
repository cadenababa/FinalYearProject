from flask import (Blueprint, 
                request, 
                render_template
                )
from flask_login import (login_required,
                    current_user
                    )

from utils import *

routes = Blueprint('routes', __name__)

@routes.get('/dashboard')
@login_required
def dashboard_get():
    if current_user.is_teacher:
        return render_template("teacher/dashboard.html")
    else:
        return render_template("student/dashboard.html", sem_to_year=sem_to_year)