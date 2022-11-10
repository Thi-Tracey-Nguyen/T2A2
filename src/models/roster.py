from init import db, ma
from datetime import datetime, date as dt
from models.employee import Employee
from marshmallow import fields, validates, validates_schema
from marshmallow.exceptions import ValidationError

class Roster(db.Model):
    __tablename__ = 'rosters'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='SET NULL'))

    __table_args__ = (db.UniqueConstraint('employee_id', 'date'),)

    employee = db.relationship('Employee')

class RosterSchema(ma.Schema):
    employee = fields.Nested('EmployeeSchema', only = ['user'])

    #validate that input date 
    @validates('date')
    def validate_date(self, date):
        #checks if input date is a valid date and follows 'YYYY-MM-DD' format
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()

            #validate input date is in the future
            if date <= dt.today():
                raise ValidationError('Roster date must be in the future')

        #catch ValueError and raise ValidationError
        except ValueError:
            raise ValidationError("Input date is invalid or does not conform to 'YYYY-MM-DD' format")

    #validate employee_id
    @validates('employee_id')
    def validate_employee_id(self, employee_id):
        stmt = db.select(Employee).filter_by(id = employee_id)
        employee = db.session.scalar(stmt)

        if not employee:
            raise ValidationError('Employee id does not exist')


    class Meta:
        fields = ('date', 'employee', 'employee_id', 'id')
        ordered = True