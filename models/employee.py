from extensions import db

class Employee(db.Model):
    __tablename__ = 'employee_form'
    id = db.Column(db.Integer, primary_key=True)
    date2 = db.Column(db.Date)

    emp_code1 = db.Column(db.String(255))
    reviewer_email = db.Column(db.String(255))

    signaturepath1 = db.Column(db.String(255))

    IP_addr = db.Column(db.String(255))
    Location = db.Column(db.String(255))
    UserAgent = db.Column(db.String(255))
    OperatingSystem = db.Column(db.String(255))
    Time = db.Column(db.DateTime)