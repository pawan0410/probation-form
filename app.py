from flask import Flask
from flask import render_template
from extensions import db
import base64
import os
from flask import request
from flask import redirect
import datetime
from models.manager import Manager
from models.employee import Employee
from flask_mail import Message
from extensions import mail
from ftp import upload_file
import utils

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/aig_probation_form'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = r'kmt.aigbusiness@gmail.com'
app.config['MAIL_PASSWORD'] = r'atul123@#'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


db.init_app(app)
mail.init_app(app)

with app.app_context():
    db.create_all()

def save_signature(base64_str, emp_name, frm_name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', emp_name)
    file_name = '{}_{}.png'.format(path, frm_name)
    image = base64.b64decode(base64_str.split(',')[1])
    with open(file_name, 'wb') as f:
        f.write(image)
        f.close()
    return file_name

def send_document(**kwargs):
    msg = Message('Probation Form', sender='reset@aigbusiness.in', recipients=[
        'pkaur@aigbusiness.com'
    ])
    msg.html = render_template(
        'employee.html',
        signature=kwargs['signature'],
        signature1=kwargs['signature1'],

        date=kwargs['date'],

        emp_name=kwargs['emp_name'],
        authority_name=kwargs['authority_name']
    )
    mail.send(msg)


@app.route("/")
def main():
    return render_template('main.html')


@app.route("/manager" , methods=['POST'])
def save_data():
    emp_code = request.form.get('emp_code')
    emp_name = request.form.get('emp_name')
    department = request.form.get('department')
    period_of_review = request.form.get('period_of_review')
    reviewer = request.form.get('reviewer')
    reviewers_title = request.form.get('reviewers_title')
    job_Knowledge = request.form.get('job_Knowledge')
    productivity = request.form.get('productivity')
    work_quality = request.form.get('work_quality')
    technical_skills = request.form.get('technical_skills')
    work_consistency = request.form.get('work_consistency')
    enthusiasm = request.form.get('enthusiasm')
    cooperation = request.form.get('cooperation')
    attitude = request.form.get('attitude')
    initiative = request.form.get('initiative')
    work_relations = request.form.get('work_relations')
    creativity = request.form.get('creativity')
    punctuality = request.form.get('punctuality')
    attendance = request.form.get('attendance')
    dependability = request.form.get('dependability')
    communication_skills = request.form.get('communication_skills')
    overall_rating = request.form.get('overall_rating')
    opportunities = request.form.get('opportunities')
    reviewers_comments = request.form.get('reviewers_comments')
    job_Knowledge_comments = request.form.get('job_Knowledge_comments')
    productivity_comments = request.form.get('productivity_comments')
    work_quality_comments = request.form.get('work_quality_comments')
    technical_skills_comments = request.form.get('technical_skills_comments')
    work_consistency_comments = request.form.get('work_consistency_comments')
    enthusiasm_comments = request.form.get('enthusiasm_comments')
    cooperation_comments = request.form.get('cooperation_comments')
    attitude_comments = request.form.get('attitude_comments')
    initiative_comments = request.form.get('initiative_comments')
    work_relations_comments = request.form.get('work_relations_comments')
    creativity_comments = request.form.get('creativity_comments')
    punctuality_comments = request.form.get('punctuality_comments')
    attendance_comments = request.form.get('attendance_comments')
    dependability_comments = request.form.get('dependability_comments')
    communication_skills_comments = request.form.get('communication_skills_comments')
    overall_rating_comments = request.form.get('overall_rating_comments')

    signature = save_signature(request.form.get('signature'), request.form.get('reviewer'), 'signature')
    date = request.form.get('date')
    date1 = request.form.get('date1')

    manager_form = Manager(
        emp_code=emp_code,
        emp_name=emp_name,
        department = department,
        period_of_review = period_of_review,
        reviewer = reviewer,
        reviewers_title = reviewers_title,
        job_Knowledge = job_Knowledge,
        productivity = productivity,
        work_quality = work_quality,
        technical_skills = technical_skills,
        work_consistency = work_consistency,
        enthusiasm = enthusiasm,
        cooperation = cooperation,
        attitude = attitude,
        initiative = initiative,
        work_relations = work_relations,
        creativity = creativity,
        punctuality = punctuality,
        attendance = attendance,
        dependability = dependability,
        communication_skills = communication_skills,
        overall_rating = overall_rating,
        opportunities = opportunities,
        reviewers_comments = reviewers_comments,
        job_Knowledge_comments = job_Knowledge_comments,
        productivity_comments = productivity_comments,
        work_quality_comments = work_quality_comments,
        technical_skills_comments = technical_skills_comments,
        work_consistency_comments = work_consistency_comments,
        enthusiasm_comments = enthusiasm_comments,
        cooperation_comments = cooperation_comments,
        attitude_comments = attitude_comments,
        initiative_comments = initiative_comments,
        work_relations_comments = work_relations_comments,
        creativity_comments = creativity_comments,
        punctuality_comments = punctuality_comments,
        attendance_comments = attendance_comments,
        dependability_comments = dependability_comments,
        communication_skills_comments = communication_skills_comments,
        overall_rating_comments = overall_rating_comments,

        date = date,
        date1 = date1,

        IP_addr = request.remote_addr,
        Location = request.form.get('location'),
        UserAgent = request.user_agent.browser,
        OperatingSystem = request.user_agent.platform,
        Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        signaturepath = signature
    )

    db.session.add(manager_form)
    db.session.commit()
    return redirect('/document/{}/{}'.format(reviewer,emp_code))


@app.route("/thankyou")
def thankyou():
    return render_template('thankyou.html')


@app.route("/document/<string:reviewer>/<string:emp_code>")
def document(reviewer,emp_code):
    the_document = Manager.query.filter(Manager.reviewer == reviewer,Manager.emp_code==emp_code).order_by("id desc").first()

    BASE_DIR = os.path.dirname(__file__)

    return render_template('document.html', the_document=the_document, base_dir=BASE_DIR)


# @app.route("/employee", methods=['POST'])
# def save_empdata():
#     emp_code1 = request.form.get('emp_code1')
#     reviewer_email = request.form.get('reviewer_email')
#     signature1 = save_signature(request.form.get('signature1'), request.form.get('emp_code1'), 'signature1')
#     date2 = request.form.get('date2')
#
#     emp_form = Employee(
#         emp_code1=emp_code1,
#         reviewer_email=reviewer_email,
#         date2=date2,
#         IP_addr=request.remote_addr,
#         Location=request.form.get('location'),
#         UserAgent=request.user_agent.browser,
#         OperatingSystem=request.user_agent.platform,
#         Time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         signaturepath1=signature1
#     )
#
#     db.session.add(emp_form)
#     db.session.commit()
#     return redirect('/employee/{}'.format(emp_code1))


@app.route("/employee/<string:emp_code>", methods=['POST'])
def send_mail(emp_code):

    BASE_DIR = os.path.dirname(__file__)

    emp_code1 = request.form.get('emp_code1')
    reviewer_email = request.form.get('reviewer_email')
    signature1 = save_signature(request.form.get('signature1'), request.form.get('emp_code1'), 'signature1')
    date2 = request.form.get('date2')

    emp_form = Employee(
        emp_code1=emp_code1,
        reviewer_email=reviewer_email,
        date2=date2,
        IP_addr=request.remote_addr,
        Location=request.form.get('location'),
        UserAgent=request.user_agent.browser,
        OperatingSystem=request.user_agent.platform,
        Time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        signaturepath1=signature1
    )

    db.session.add(emp_form)
    db.session.commit()

    the_empdocument = Employee.query.filter(Employee.emp_code1 == emp_code).order_by("id desc").first()
    the_document = Manager.query.filter(Manager.emp_code == emp_code).order_by("id desc").first()

    file_name = utils.save_document_as_docx(
        emp_name=the_document.emp_name,
        emp_code=the_document.emp_code,
        date=the_document.date,
        department=the_document.department,
        period_of_review=the_document.period_of_review,
        reviewer=the_document.reviewer,
        reviewers_title=the_document.reviewers_title,
        job_Knowledge=the_document.job_Knowledge,
        job_Knowledge_comments=the_document.job_Knowledge_comments,
        productivity = the_document.productivity,
        productivity_comments=the_document.productivity_comments,
        work_quality=the_document.work_quality,
        work_quality_comments=the_document.work_quality_comments,
        technical_skills=the_document.technical_skills,
        technical_skills_comments=the_document.technical_skills_comments,
        work_consistency = the_document.work_consistency,
        work_consistency_comments=the_document.work_consistency_comments,
        enthusiasm=the_document.enthusiasm,
        enthusiasm_comments=the_document.enthusiasm_comments,
        cooperation=the_document.cooperation,
        cooperation_comments=the_document.cooperation_comments,
        attitude=the_document.attitude,
        attitude_comments=the_document.attitude_comments,
        initiative=the_document.initiative,
        initiative_comments=the_document.initiative_comments,
        work_relations=the_document.work_relations,
        work_relations_comments=the_document.work_relations_comments,
        creativity=the_document.creativity,
        creativity_comments=the_document.creativity_comments,
        punctuality=the_document.punctuality,
        punctuality_comments=the_document.punctuality_comments,
        attendance=the_document.attendance,
        attendance_comments=the_document.attendance_comments,
        dependability=the_document.dependability,
        dependability_comments=the_document.dependability_comments,
        communication_skills=the_document.communication_skills,
        communication_skills_comments=the_document.communication_skills_comments,
        overall_rating=the_document.overall_rating,
        overall_rating_comments=the_document.overall_rating_comments,
        opportunities=the_document.opportunities,
        reviewers_comments=the_document.reviewers_comments,
        signature1=the_empdocument.signaturepath1,
        signature=the_document.signaturepath,
        date2=the_empdocument.date2,
        date1=the_document.date1

    )
    utils.send_document_as_mail(emp_name=the_document.emp_name, file_name=file_name)

    return render_template('employee.html', the_empdocument=the_empdocument,the_document= the_document, base_dir=BASE_DIR)



